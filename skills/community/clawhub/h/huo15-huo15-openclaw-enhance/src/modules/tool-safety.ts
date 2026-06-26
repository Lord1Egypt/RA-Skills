/**
 * 模块: 工具安全补充（非侵入）
 *
 * 设计原则：
 * - 龙虾自带 `tools.allow` / `tools.deny` / sandbox 权限模型。本模块**不**替代它。
 * - 本模块只补充龙虾原生规则无法表达的颗粒度（例如 glob pathPattern、命令子串模式）。
 * - 匹配到规则只走两种路径：
 *     hardblock → 直接拒绝（相当于龙虾 deny 的补充规则）
 *     block     → 通过龙虾 requireApproval 弹窗由用户决定（非阻塞）
 *   其它命中只写 safety_log 审计表，不阻塞，不复制龙虾已有的决定。
 * - after_tool_call 只做错误分类 + 指数退避建议，**不伪造重试**（龙虾主循环才有重试权）；
 *   分类结果写 safety_log 供仪表盘/工具检索。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { getDb, logSafetyEvent, getRecentSafetyEvents, getSafetyStats } from "../utils/sqlite-store.js";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { DEFAULT_AGENT_ID, type SafetyConfig, type SafetyRule } from "../types.js";

// ─────────────────────── 错误分类 ───────────────────────
export type ErrorCategory =
  | "rate_limit"
  | "server_error"
  | "network_error"
  | "auth_error"
  | "timeout_error"
  | "unknown_error";

interface ClassifiedError {
  category: ErrorCategory;
  retryable: boolean;
  statusCode?: number;
  retryAfterMs?: number;
  message: string;
}

function classifyError(errorMsg: string, statusCode?: number): ClassifiedError {
  const msg = errorMsg.toLowerCase();

  if (statusCode === 429 || msg.includes("429") || msg.includes("rate limit") || msg.includes("too many requests")) {
    const retryAfterMatch =
      errorMsg.match(/retry[- ]?after[:\s]*(\d+)/i) ||
      errorMsg.match(/retryafterms[:\s]*(\d+)/i);
    const retryAfterMs = retryAfterMatch ? parseInt(retryAfterMatch[1], 10) : undefined;
    return { category: "rate_limit", retryable: true, statusCode: statusCode ?? 429, retryAfterMs, message: errorMsg };
  }
  if (
    ((statusCode ?? 0) >= 500 && (statusCode ?? 0) < 600) ||
    msg.includes("500") || msg.includes("502") || msg.includes("503") ||
    msg.includes("internal server error") || msg.includes("bad gateway") ||
    msg.includes("service unavailable")
  ) {
    return { category: "server_error", retryable: true, statusCode, message: errorMsg };
  }
  if (
    statusCode === 401 || statusCode === 403 ||
    msg.includes("401") || msg.includes("403") ||
    msg.includes("unauthorized") || msg.includes("forbidden") ||
    msg.includes("invalid api key") || msg.includes("authentication failed")
  ) {
    return { category: "auth_error", retryable: false, statusCode, message: errorMsg };
  }
  if (
    msg.includes("timeout") || msg.includes("etimedout") || msg.includes("econnreset") ||
    msg.includes("econnrefused") || msg.includes("network error") ||
    msg.includes("enotfound") || msg.includes("socket hang up") ||
    msg.includes("getaddrinfo") || msg.includes("eai_again")
  ) {
    return { category: "network_error", retryable: true, statusCode, message: errorMsg };
  }
  if (msg.includes("timed out") || msg.includes("deadline exceeded")) {
    return { category: "timeout_error", retryable: true, statusCode, message: errorMsg };
  }
  return { category: "unknown_error", retryable: false, statusCode, message: errorMsg };
}

interface RetryAdvice {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
}

const RETRY_ADVICE: Record<ErrorCategory, RetryAdvice> = {
  rate_limit:    { maxAttempts: 5, baseDelayMs: 1000, maxDelayMs: 60000, backoffMultiplier: 2 },
  server_error:  { maxAttempts: 3, baseDelayMs: 2000, maxDelayMs: 30000, backoffMultiplier: 2 },
  network_error: { maxAttempts: 3, baseDelayMs: 1000, maxDelayMs: 15000, backoffMultiplier: 2 },
  timeout_error: { maxAttempts: 2, baseDelayMs: 2000, maxDelayMs: 10000, backoffMultiplier: 2 },
  auth_error:    { maxAttempts: 1, baseDelayMs: 0,    maxDelayMs: 0,     backoffMultiplier: 1 },
  unknown_error: { maxAttempts: 1, baseDelayMs: 0,    maxDelayMs: 0,     backoffMultiplier: 1 },
};

function computeBackoffMs(attempt: number, advice: RetryAdvice, retryAfterMs?: number): number {
  if (retryAfterMs !== undefined) return Math.min(retryAfterMs, advice.maxDelayMs);
  const delay = advice.baseDelayMs * Math.pow(advice.backoffMultiplier, Math.max(0, attempt - 1));
  return Math.min(delay, advice.maxDelayMs);
}

// ─────────────────────── 规则匹配 ───────────────────────
function matchGlob(pattern: string, text: string): boolean {
  const regex = new RegExp(
    "^" + pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*") + "$",
    "i",
  );
  return regex.test(text);
}

function extractMatchText(params: Record<string, unknown>): string {
  for (const key of ["command", "input", "path", "file_path", "url", "query"]) {
    if (typeof params[key] === "string") return params[key] as string;
  }
  try {
    return JSON.stringify(params);
  } catch {
    return "";
  }
}

function extractPathText(params: Record<string, unknown>): string {
  for (const key of ["path", "file_path", "filePath", "filename"]) {
    if (typeof params[key] === "string") return params[key] as string;
  }
  return "";
}

// ─────────────────────── 最近错误分类缓存（供 enhance_retry_status 查询） ───────────────────────
interface ErrorObservation {
  agentId: string;
  toolName: string;
  classified: ClassifiedError;
  advice: RetryAdvice;
  suggestedDelayMs: number;
  observedAt: number;
  attemptHint: number;
}

const recentObservations = new Map<string, ErrorObservation>();
const OBSERVATION_TTL_MS = 60_000;

function observationKey(agentId: string, toolName: string): string {
  return `${agentId}::${toolName}`;
}

function pruneObservations(now: number) {
  for (const [k, v] of recentObservations.entries()) {
    if (now - v.observedAt > OBSERVATION_TTL_MS) recentObservations.delete(k);
  }
}

// ─────────────────────── 主入口 ───────────────────────
export function registerToolSafety(api: OpenClawPluginApi, config?: SafetyConfig) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();
  const rules: SafetyRule[] = config?.rules ?? [];
  const defaultAction = config?.defaultAction ?? "allow";
  const enableRetry = config?.enableRetry ?? true;

  // ── Hook: before_tool_call — 补充式规则匹配（不重写龙虾原生决策） ──
  // v5.7.8: typed via openclaw 4.24 SDK (PluginHookBeforeToolCallEvent + PluginHookToolContext)
  api.on("before_tool_call", (event, ctx) => {
    const agentId = (ctx?.agentId ?? DEFAULT_AGENT_ID).trim();
    const toolName = event?.toolName ?? "";
    const params = event?.params ?? {};
    const matchText = extractMatchText(params);
    const pathText = extractPathText(params);

    for (const rule of rules) {
      if (!matchGlob(rule.tool, toolName)) continue;
      if (rule.pattern && !matchGlob(rule.pattern, matchText)) continue;
      if (rule.pathPattern && !matchGlob(rule.pathPattern, pathText)) continue;

      logSafetyEvent(db, agentId, toolName, matchText.slice(0, 500), rule.action, JSON.stringify(rule), rule.reason ?? "");

      if (rule.action === "hardblock") {
        api.logger.warn(`[enhance-safety] hardblock ${toolName} (agent: ${agentId})`);
        return { block: true, blockReason: rule.reason ?? "匹配 enhance 安全规则（hardblock）" };
      }
      if (rule.action === "block") {
        return {
          requireApproval: {
            title: `enhance 安全补充：工具「${toolName}」需确认`,
            description: [rule.reason ?? "该操作匹配 enhance 的细粒度安全规则。", `工具: ${toolName}`].join("\n"),
            severity: "critical" as const,
            timeoutMs: 30_000,
            timeoutBehavior: "deny" as const,
          },
        };
      }
      // log / allow: 不干预龙虾原生决策
      return {};
    }

    if (defaultAction === "log") {
      logSafetyEvent(db, agentId, toolName, matchText.slice(0, 500), "log", "", "default-log");
    }
    return {};
  }, { priority: 900 } as any);

  // ── Hook: after_tool_call — 错误观察（不自动重试，只给建议） ──
  // v5.7.8: typed via openclaw 4.24 SDK (PluginHookAfterToolCallEvent + PluginHookToolContext)
  if (enableRetry) {
    api.on("after_tool_call", (event, ctx) => {
      const agentId = (ctx?.agentId ?? DEFAULT_AGENT_ID).trim();
      const toolName = event?.toolName ?? "";
      const rawError = event?.error ?? "";
      const durationMs = event?.durationMs ?? 0;
      if (!rawError) return;

      const statusMatch = rawError.match(/\b(4\d{2}|5\d{2})\b/);
      const statusCode = statusMatch ? parseInt(statusMatch[1], 10) : undefined;
      const classified = classifyError(rawError, statusCode);
      const advice = RETRY_ADVICE[classified.category];
      const now = Date.now();

      pruneObservations(now);
      const key = observationKey(agentId, toolName);
      const prior = recentObservations.get(key);
      const attempt = prior ? Math.min(prior.attemptHint + 1, advice.maxAttempts) : 1;
      const suggestedDelayMs = classified.retryable
        ? computeBackoffMs(attempt, advice, classified.retryAfterMs)
        : 0;

      recentObservations.set(key, {
        agentId,
        toolName,
        classified,
        advice,
        suggestedDelayMs,
        observedAt: now,
        attemptHint: attempt,
      });

      logSafetyEvent(
        db,
        agentId,
        toolName,
        rawError.slice(0, 500),
        classified.category.toUpperCase(),
        JSON.stringify({
          category: classified.category,
          retryable: classified.retryable,
          statusCode,
          suggestedDelayMs,
          attemptHint: attempt,
          durationMs,
        }),
        classified.category,
      );

      if (classified.retryable) {
        api.logger.info(
          `[enhance-safety] ${toolName} → ${classified.category} (attempt≈${attempt}/${advice.maxAttempts}, 建议退避 ${suggestedDelayMs}ms)`,
        );
      } else {
        api.logger.warn(`[enhance-safety] ${toolName} → ${classified.category} (不建议重试)`);
      }
    });
  }

  // ── Tool: enhance_safety_log ──
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_safety_log",
      description: "查看 enhance 安全补充规则的审计日志",
      parameters: Type.Object({
        action: Type.Union([Type.Literal("recent"), Type.Literal("stats")], {
          description: "recent|stats",
        }),
        limit: Type.Optional(Type.Number({ description: "recent 条数", default: 15 })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = (((ctx as any)?.agentId as string | undefined) ?? DEFAULT_AGENT_ID).trim();
        if (params.action === "stats") {
          const stats = getSafetyStats(db, agentId);
          return {
            content: [
              {
                type: "text" as const,
                text: `enhance 安全补充统计 (agent: ${agentId})：\n总事件: ${stats.total}\n已拦截: ${stats.blocked}\n已记录: ${stats.logged}\n\n注：这些是 enhance 规则命中数，不包含龙虾原生 tools.allow/deny 拦截。`,
              },
            ],
          };
        }
        const events = getRecentSafetyEvents(db, agentId, (params.limit as number) ?? 15);
        if (events.length === 0) {
          return { content: [{ type: "text" as const, text: `暂无 enhance 安全事件 (agent: ${agentId})。` }] };
        }
        const lines = events.map(
          (e) => `[${e.action}] ${e.created_at} | ${e.tool}: ${(e.params ?? "").slice(0, 60)}${e.reason ? ` (${e.reason})` : ""}`,
        );
        return {
          content: [{ type: "text" as const, text: `最近 enhance 安全事件 (agent: ${agentId})：\n${lines.join("\n")}` }],
        };
      },
    })) as any,
    { name: "enhance_safety_log" },
  );

  // ── Tool: enhance_retry_status ──
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_retry_status",
      description: "查询最近一分钟失败工具调用的错误分类和建议退避（不自动重试）",
      parameters: Type.Object({}),
      async execute() {
        pruneObservations(Date.now());
        const agentId = (((ctx as any)?.agentId as string | undefined) ?? DEFAULT_AGENT_ID).trim();
        const entries = Array.from(recentObservations.values()).filter((e) => e.agentId === agentId);
        if (entries.length === 0) {
          return { content: [{ type: "text" as const, text: `当前 Agent (${agentId}) 无可观测的失败工具调用。` }] };
        }
        const lines = entries.map((e) => {
          const ageSec = Math.round((Date.now() - e.observedAt) / 1000);
          const suggestion = e.classified.retryable
            ? `建议退避 ${Math.round(e.suggestedDelayMs / 100) / 10}s（最多 ${e.advice.maxAttempts} 次）`
            : "不建议重试";
          return `[${e.classified.category}] ${e.toolName}\n  错误: ${e.classified.message.slice(0, 100)}\n  ${ageSec}s 前 · attempt≈${e.attemptHint}/${e.advice.maxAttempts} · ${suggestion}`;
        });
        return {
          content: [{ type: "text" as const, text: `最近失败观测 (${entries.length})：\n\n${lines.join("\n\n")}` }],
        };
      },
    })) as any,
    { name: "enhance_retry_status" },
  );

  // ── Tool: enhance_safety_rules ──
  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_safety_rules",
      description: "查看 enhance 补充安全规则清单（不含龙虾原生 tools.allow/deny）",
      parameters: Type.Object({}),
      async execute() {
        if (rules.length === 0) {
          return {
            content: [
              {
                type: "text" as const,
                text: `当前无 enhance 补充规则（默认策略 ${defaultAction}）。\n\n龙虾原生权限请查看 openclaw.json → tools.allow / tools.deny。\nenhance 细粒度规则配置：openclaw.json → plugins.entries.enhance.config.safety.rules。`,
              },
            ],
          };
        }
        const lines = rules.map(
          (r, i) =>
            `${i + 1}. [${r.action}] tool=${r.tool}${r.pattern ? ` pattern="${r.pattern}"` : ""}${r.pathPattern ? ` pathPattern="${r.pathPattern}"` : ""}${r.reason ? ` — ${r.reason}` : ""}`,
        );
        return {
          content: [
            {
              type: "text" as const,
              text: `enhance 补充规则 (${rules.length} 条)：\n${lines.join("\n")}\n\n默认策略: ${defaultAction}\n（龙虾原生 tools.allow/deny 独立生效，不经本表）`,
            },
          ],
        };
      },
    })) as any,
    { name: "enhance_safety_rules" },
  );

  api.logger.info(
    `[enhance] 工具安全补充模块已加载（${rules.length} 条规则；仅补充龙虾原生 tools.allow/deny 未覆盖的颗粒度；错误分类${enableRetry ? "已启用" : "已停用"}）`,
  );
}
