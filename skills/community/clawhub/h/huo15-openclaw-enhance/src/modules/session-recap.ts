/**
 * 模块: 会话回顾（Session Recap）— 对齐 Claude Code 75-min idle auto-summary
 *
 * 触发条件（AND）：
 * 1. before_prompt_build 看到当前 agent/session 的上一次活动距现在 > recapIdleMinutes（默认 75）
 * 2. 距离上次 recap 已超过 recapMinIntervalMinutes（默认 30）或本进程内从未 recap 过此 agent
 *
 * 恢复内容（prependContext 里追加）：
 *   - 最近 1 个章节（title + summary）
 *   - 最近 3 条 in_progress/pending todo
 *   - 最近 2 条 decision 类记忆
 *   - 一句"你刚回来，上次到这儿"的引导
 *
 * 非侵入式保证：
 *   - 只读三张已有表（chapters / todos / memories），不建新表
 *   - 纯追加 prependContext，绝不覆盖龙虾原生 system prompt
 *   - 可通过 config.sessionRecap.enabled = false 关闭
 *   - 同时提供 enhance_session_recap 工具，用户可手动"给我做个回顾"
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { getDb, listChapters, getLatestTodos, searchMemories } from "../utils/sqlite-store.js";
import { DEFAULT_AGENT_ID } from "../types.js";

export interface SessionRecapConfig {
  enabled?: boolean;
  /** 距上次活动多久（分钟）就认为是 idle，默认 75 */
  recapIdleMinutes?: number;
  /** 两次 recap 的最小间隔（分钟），防抖，默认 30 */
  recapMinIntervalMinutes?: number;
  /** recap 里章节数，默认 1 */
  maxChapters?: number;
  /** recap 里 todo 数，默认 3 */
  maxTodos?: number;
  /** recap 里 decision 记忆数，默认 2 */
  maxDecisions?: number;
}

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

function parseSqliteTs(s: string | undefined): number {
  if (!s) return 0;
  // SQLite datetime('now') 格式: "YYYY-MM-DD HH:MM:SS" （UTC）
  const t = Date.parse(s.includes("T") ? s : s.replace(" ", "T") + "Z");
  return isNaN(t) ? 0 : t;
}

function fmtGap(ms: number): string {
  const min = Math.floor(ms / 60000);
  if (min < 60) return `${min} 分钟前`;
  const h = Math.floor(min / 60);
  if (h < 24) return `${h} 小时前`;
  return `${Math.floor(h / 24)} 天前`;
}

/**
 * 构建一次 recap 文本；若没有任何素材返回空串（调用方可据此决定是否注入）。
 */
export function buildRecapText(
  db: ReturnType<typeof getDb>,
  agentId: string,
  sessionId: string,
  cfg: Required<Pick<SessionRecapConfig, "maxChapters" | "maxTodos" | "maxDecisions">>,
  idleMs: number,
): string {
  const lines: string[] = [];

  const chapters = listChapters(db, agentId, sessionId || undefined, cfg.maxChapters);
  const todos = getLatestTodos(db, agentId).filter((t) => t.status === "in_progress" || t.status === "pending").slice(0, cfg.maxTodos);
  const decisions = searchMemories(db, agentId, { category: "decision", limit: cfg.maxDecisions });

  if (chapters.length === 0 && todos.length === 0 && decisions.length === 0) {
    return "";
  }

  lines.push(`【会话回顾】你上次活动是 ${fmtGap(idleMs)}，帮你把关键状态拉回来：`);
  lines.push("");

  if (chapters.length > 0) {
    lines.push("— 最近章节 —");
    for (const ch of chapters) {
      lines.push(`  · #${ch.id} ${ch.title}${ch.summary ? ` — ${ch.summary}` : ""}`);
    }
    lines.push("");
  }

  if (todos.length > 0) {
    lines.push("— 待办 —");
    for (const t of todos) {
      const status = t.status === "in_progress" ? "🔄" : "⏳";
      lines.push(`  ${status} ${t.content}`);
    }
    lines.push("");
  }

  if (decisions.length > 0) {
    lines.push("— 关键决定 —");
    for (const d of decisions) {
      const text = (d.content ?? "").trim();
      lines.push(`  · ${text.slice(0, 80)}${text.length > 80 ? "..." : ""}`);
    }
    lines.push("");
  }

  lines.push("（本回顾由 @huo15/openclaw-enhance session-recap 自动生成；若不需要可 config.sessionRecap.enabled=false）");
  return lines.join("\n");
}

/**
 * 查当前 agent/session 最近一次活动时间（取三张表里最大 updated_at / created_at 作代理）
 */
function getLastActivityMs(
  db: ReturnType<typeof getDb>,
  agentId: string,
  sessionId: string,
): number {
  const rows = db
    .prepare(
      `SELECT MAX(ts) AS ts FROM (
         SELECT MAX(updated_at) AS ts FROM memories WHERE agent_id = ?
         UNION ALL
         SELECT MAX(created_at) AS ts FROM chapters WHERE agent_id = ?${sessionId ? " AND session_id = ?" : ""}
         UNION ALL
         SELECT MAX(updated_at) AS ts FROM todos WHERE agent_id = ?
       )`,
    )
    .all(...(sessionId ? [agentId, agentId, sessionId, agentId] : [agentId, agentId, agentId])) as Array<{ ts: string | null }>;
  return parseSqliteTs(rows[0]?.ts ?? undefined);
}

export function registerSessionRecap(api: OpenClawPluginApi, config?: SessionRecapConfig) {
  if (config?.enabled === false) return;

  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();

  const idleMinutes = config?.recapIdleMinutes ?? 75;
  const minIntervalMinutes = config?.recapMinIntervalMinutes ?? 30;
  const maxChapters = config?.maxChapters ?? 1;
  const maxTodos = config?.maxTodos ?? 3;
  const maxDecisions = config?.maxDecisions ?? 2;

  // 进程内防抖表：agentId + sessionId → lastRecapAt(ms)
  // v5.7.2: 加 LRU cap 防止跨 session 永不清造成内存泄漏
  const lastRecapAt = new Map<string, number>();
  const MAX_RECAP_ENTRIES = 500;

  // ── Hook: before_prompt_build ── 自动 recap
  // v5.7.8: typed via openclaw 4.24 SDK
  api.on("before_prompt_build", (_event, ctx) => {
    const agentId = pickAgentId(ctx);
    const sessionId = pickSessionId(ctx);
    const key = `${agentId}::${sessionId}`;

    const now = Date.now();
    const lastActivity = getLastActivityMs(db, agentId, sessionId);
    if (!lastActivity) return;

    const idleMs = now - lastActivity;
    if (idleMs < idleMinutes * 60_000) return;

    const lastRecap = lastRecapAt.get(key) ?? 0;
    if (now - lastRecap < minIntervalMinutes * 60_000) return;

    const text = buildRecapText(
      db,
      agentId,
      sessionId,
      { maxChapters, maxTodos, maxDecisions },
      idleMs,
    );
    if (!text) return;

    // LRU eviction: 重新插入 key 让活跃 session 不被淘汰
    if (lastRecapAt.has(key)) lastRecapAt.delete(key);
    while (lastRecapAt.size >= MAX_RECAP_ENTRIES) {
      const oldest = lastRecapAt.keys().next().value;
      if (oldest === undefined) break;
      lastRecapAt.delete(oldest);
    }
    lastRecapAt.set(key, now);
    return { prependContext: text };
  });

  // ── Tool: enhance_session_recap ── 手动触发
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_session_recap",
      description: "手动生成会话回顾（章节+待办+关键决定）",
      parameters: Type.Object({
        scope: Type.Optional(
          Type.Union([Type.Literal("session"), Type.Literal("agent")], {
            description: "session(默认)|agent",
          }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const scope = params.scope === "agent" ? "" : sessionId;

        const now = Date.now();
        const lastActivity = getLastActivityMs(db, agentId, scope);
        const idleMs = lastActivity ? now - lastActivity : 0;

        const text = buildRecapText(
          db,
          agentId,
          scope,
          { maxChapters, maxTodos, maxDecisions },
          idleMs,
        );

        if (!text) {
          return {
            content: [{ type: "text" as const, text: "暂无可回顾的内容（没有章节/待办/决定记忆）。" }],
          };
        }

        return { content: [{ type: "text" as const, text }] };
      },
    })) as any,
    { name: "enhance_session_recap" },
  );
}
