/**
 * 模块: 模式闸门（plan / explore）
 *
 * Claude Code 的 plan mode / explore mode 在龙虾里没有等价物。
 * 本模块通过 before_tool_call 钩子，在 plan/explore 模式下拦截写入类工具。
 *
 * 模式切换通过 enhance_set_mode 工具完成（每 agent+session 独立）。
 *
 * 默认禁用（defaultMode: "normal"），需要在配置里显式 enabled:true 才介入。
 * 与龙虾 tools.allow/deny 互不冲突：即使本模块允许，龙虾仍会独立检查。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import type { AgentMode, ModeConfig, NotificationQueue } from "../types.js";
import { DEFAULT_AGENT_ID } from "../types.js";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { getDb, storeMemory } from "../utils/sqlite-store.js";

// ── 写入类工具名（子串匹配，大小写不敏感） ──
// 只拦截"会改动外部状态"的工具，搜索/读取类不受影响。
const MUTATING_TOOL_PATTERNS = [
  "edit", "write", "patch", "apply",
  "create_file", "create-file",
  "rm", "delete",
  "mv", "move",
  "install", "uninstall",
  "commit", "push", "merge", "rebase", "reset",
  "exec", "run_command",
];

const BASH_LIKE = ["bash", "shell", "execute", "run"];
const DESTRUCTIVE_BASH_TOKENS = [
  "rm ", "rm -", "sudo ", "git push", "git commit", "git reset --hard",
  "git rebase", "git merge", "chmod ", "chown ", "mv ",
  "npm install", "pnpm install", "bun install",
  "> ", ">> ", "| sh", "| bash", "curl ", "wget ",
];

const modeState = new Map<string, AgentMode>();

/** Ring buffer of tool calls the model attempted during plan mode — surfaced at ExitPlanMode time. */
interface PlannedAction {
  toolName: string;
  paramsSummary: string;
  at: string;
}
const plannedActions = new Map<string, PlannedAction[]>();
const MAX_PLANNED = 50;

/**
 * v5.7.2: LRU caps to prevent unbounded growth across long-lived processes (agents 跨 session 永不清).
 * Map iteration is insertion order, so deleting `keys().next()` evicts the oldest entry.
 */
const MAX_STATE_ENTRIES = 200;
const MAX_PLANNED_ENTRIES = 200;

function evictOldest<K, V>(map: Map<K, V>, capacity: number) {
  while (map.size >= capacity) {
    const oldest = map.keys().next().value;
    if (oldest === undefined) break;
    map.delete(oldest);
  }
}

function stateKey(agentId: string, sessionId: string): string {
  return `${agentId}::${sessionId}`;
}

function getMode(agentId: string, sessionId: string, fallback: AgentMode): AgentMode {
  return modeState.get(stateKey(agentId, sessionId)) ?? fallback;
}

function setMode(agentId: string, sessionId: string, mode: AgentMode) {
  const key = stateKey(agentId, sessionId);
  // Refresh insertion order on update so active sessions don't get evicted.
  if (modeState.has(key)) modeState.delete(key);
  evictOldest(modeState, MAX_STATE_ENTRIES);
  modeState.set(key, mode);
  // Leaving plan mode clears the captured plan (a fresh plan mode starts clean).
  if (mode !== "plan") plannedActions.delete(key);
}

function recordPlannedAction(agentId: string, sessionId: string, toolName: string, params: Record<string, unknown>) {
  const key = stateKey(agentId, sessionId);
  const arr = plannedActions.get(key) ?? [];
  if (!plannedActions.has(key)) {
    evictOldest(plannedActions, MAX_PLANNED_ENTRIES);
  }
  const summary = (() => {
    const keyPairs = Object.entries(params).slice(0, 3);
    if (keyPairs.length === 0) return "";
    return keyPairs
      .map(([k, v]) => `${k}=${typeof v === "string" ? v.slice(0, 60) : JSON.stringify(v).slice(0, 60)}`)
      .join(", ");
  })();
  arr.push({ toolName, paramsSummary: summary, at: new Date().toISOString() });
  if (arr.length > MAX_PLANNED) arr.splice(0, arr.length - MAX_PLANNED);
  plannedActions.set(key, arr);
}

function takePlannedActions(agentId: string, sessionId: string): PlannedAction[] {
  const key = stateKey(agentId, sessionId);
  const arr = plannedActions.get(key) ?? [];
  plannedActions.delete(key);
  return arr;
}

function isMutatingTool(toolName: string, params: Record<string, unknown>): boolean {
  const lower = toolName.toLowerCase();
  if (MUTATING_TOOL_PATTERNS.some((p) => lower.includes(p))) return true;
  if (BASH_LIKE.some((p) => lower.includes(p))) {
    const command = String(params.command ?? params.input ?? params.cmd ?? "").toLowerCase();
    if (!command) return false;
    return DESTRUCTIVE_BASH_TOKENS.some((t) => command.includes(t));
  }
  return false;
}

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

export function registerModeGate(
  api: OpenClawPluginApi,
  config: ModeConfig | undefined,
  notifyQueue: NotificationQueue,
) {
  const defaultMode: AgentMode = config?.defaultMode ?? "normal";

  // v5.7.8: typed via openclaw 4.24 SDK
  api.on(
    "before_tool_call",
    (event, ctx) => {
      const agentId = pickAgentId(ctx);
      const sessionId = pickSessionId(ctx);
      const mode = getMode(agentId, sessionId, defaultMode);
      if (mode === "normal") return;

      const toolName = event?.toolName ?? "";
      const params = event?.params ?? {};
      if (toolName.startsWith("enhance_set_mode") || toolName.startsWith("enhance_current_mode")) {
        return;
      }

      if (!isMutatingTool(toolName, params)) return;

      const reason =
        mode === "plan"
          ? "当前处于 plan 模式：只做规划与只读勘察，写入类工具被拦截。请在规划完成后调用 enhance_exit_plan_mode 提交计划给用户审批。"
          : "当前处于 explore 模式：只允许只读勘察，写入类工具被拦截。";

      if (mode === "plan") {
        recordPlannedAction(agentId, sessionId, toolName, params);
      }

      notifyQueue.emit(agentId, "warn", "workflow", `${mode} 模式拦截`, `工具 ${toolName} 被 ${mode} 模式拦截。`);
      return { block: true, blockReason: reason };
    },
    { priority: 950 },
  );

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_set_mode",
      description: "切换 session 模式：normal(无限制)|plan(拦截写入)|explore(只读)",
      parameters: Type.Object({
        mode: Type.Union([Type.Literal("normal"), Type.Literal("plan"), Type.Literal("explore")], {
          description: "目标模式",
        }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const target = params.mode as AgentMode;
        setMode(agentId, sessionId, target);
        return {
          content: [{ type: "text" as const, text: `✓ 已切换至 ${target} 模式 (agent: ${agentId})` }],
        };
      },
    })) as any,
    { name: "enhance_set_mode" },
  );

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_current_mode",
      description: "查看当前 session 的运行模式",
      parameters: Type.Object({}),
      async execute() {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const mode = getMode(agentId, sessionId, defaultMode);
        return {
          content: [{ type: "text" as const, text: `当前模式: ${mode} (agent: ${agentId})` }],
        };
      },
    })) as any,
    { name: "enhance_current_mode" },
  );

  // ── enhance_exit_plan_mode: Claude-Code 风格的 Plan 审批闭环 ──
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_exit_plan_mode",
      description: "提交 plan 给用户审批并退出 plan 模式（保存为 decision 记忆）",
      parameters: Type.Object({
        plan: Type.String({ description: "计划正文（Markdown）" }),
        why: Type.Optional(Type.String({ description: "动机/约束" })),
        autoApprove: Type.Optional(
          Type.Boolean({ description: "是否直接切到 normal，默认 false" }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const mode = getMode(agentId, sessionId, defaultMode);
        const plan = String(params.plan ?? "").trim();
        const why = String(params.why ?? "").trim();
        const autoApprove = Boolean(params.autoApprove);

        if (!plan) {
          return { content: [{ type: "text" as const, text: "plan 必填。" }] };
        }
        if (mode !== "plan") {
          return {
            content: [
              {
                type: "text" as const,
                text: `当前不在 plan 模式（mode=${mode}），无需提交计划；若要进入 plan 先调用 enhance_set_mode plan。`,
              },
            ],
          };
        }

        const captured = takePlannedActions(agentId, sessionId);
        const actionsBlock =
          captured.length === 0
            ? "（plan 期间未触发写入拦截）"
            : captured
                .map((a, i) => `  ${i + 1}. ${a.toolName}${a.paramsSummary ? `  [${a.paramsSummary}]` : ""}`)
                .join("\n");

        const memoryContent = [
          `【plan 模式退出】`,
          plan,
          ``,
          `拦截到的意图操作:`,
          actionsBlock,
        ].join("\n");

        const entry = storeMemory(
          db,
          agentId,
          "decision",
          memoryContent,
          "plan,exit-plan",
          7,
          sessionId,
          {
            why: why || "plan 模式退出前的决策快照",
            howToApply: autoApprove
              ? "已自动切到 normal 模式，可以开始执行 plan 列出的写入操作。"
              : "等待用户批准：用户 /enhance_set_mode normal 后可开始执行 plan。",
          },
        );

        if (autoApprove) {
          setMode(agentId, sessionId, "normal");
          notifyQueue.emit(
            agentId,
            "success",
            "workflow",
            "plan 审批：auto-approved",
            `plan #${entry.id} 已自动批准，切到 normal 模式`,
          );
        } else {
          notifyQueue.emit(
            agentId,
            "info",
            "workflow",
            "plan 待审批",
            `plan #${entry.id} 已提交，等待用户批准（调用 enhance_set_mode normal）`,
          );
        }

        return {
          content: [
            {
              type: "text" as const,
              text: [
                `✓ plan 已提交（记忆 #${entry.id}）`,
                autoApprove ? "   已自动批准并切到 normal 模式，可以开始写入。" : "   等待用户批准。用户可调用 enhance_set_mode normal 放行。",
                captured.length > 0 ? `   plan 期间捕获到 ${captured.length} 个被拦截的写入意图。` : "",
              ]
                .filter(Boolean)
                .join("\n"),
            },
          ],
          structuredContent: {
            planId: entry.id,
            plan,
            why: why || undefined,
            capturedActions: captured,
            autoApproved: autoApprove,
            mode: autoApprove ? "normal" : "plan",
          },
        };
      },
    })) as any,
    { name: "enhance_exit_plan_mode" },
  );

  api.logger.info(
    `[enhance] 模式闸门模块已加载（默认 ${defaultMode}；plan/explore 拦截写入；enhance_exit_plan_mode 提交审批）`,
  );
}

export function getCurrentMode(agentId: string, sessionId: string): AgentMode {
  return modeState.get(stateKey(agentId, sessionId)) ?? "normal";
}
