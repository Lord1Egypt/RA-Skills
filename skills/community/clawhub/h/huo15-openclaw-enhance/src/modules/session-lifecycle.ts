/**
 * v5.7.7 Session Lifecycle — 接 openclaw 4.22 的 session_start / session_end /
 * before_reset / subagent_spawned / subagent_ended 五个 hook，闭环 session
 * 生命周期。
 *
 * 调研依据：openclaw plugin-sdk hook-types.d.ts 暴露 29 个 hook，enhance 之前
 * 只用了 4 个（before_prompt_build / before_tool_call / after_tool_call /
 * before_agent_reply）。Claude Code 官方 hook 体系（SessionStart / Stop /
 * SubagentStart / SubagentStop）在 openclaw 这边都有对应。
 *
 * 红线遵守：
 * - 完全是非侵入式增强 — 只读 enhance 自己的 SQLite，不动 openclaw 任何状态
 * - 不复制龙虾原生功能 — openclaw 自己有 hook 框架，enhance 只挂回调
 * - 写入用 enhance 自有表（chapters/memories），不污染龙虾原生 memory
 * - 高频 hook（如 session_start 在多 agent 场景每分钟可能多次触发）严格控
 *   写入：单 hook 最多写 1-2 条记录，并带 dedup tag
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import {
  getDb,
  addChapter,
  listChapters,
  getLatestTodos,
  storeMemory,
} from "../utils/sqlite-store.js";
import type { SessionLifecycleConfig, NotificationQueue } from "../types.js";
import { DEFAULT_AGENT_ID } from "../types.js";

/** v5.7.8: typed ctx — openclaw 4.24 暴露的具体 context 类型 */
function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

/** 限流去重表：避免短时间多次触发同一 hook 重复写记录（v5.7.1 反思：高频 hook 写持久化是 noise factory） */
const recentEvents = new Map<string, number>();
const DEDUP_WINDOW_MS = 30_000; // 30 秒
const MAX_RECENT_ENTRIES = 500;

function shouldFire(key: string): boolean {
  const now = Date.now();
  const last = recentEvents.get(key) ?? 0;
  if (now - last < DEDUP_WINDOW_MS) return false;
  // LRU eviction
  if (recentEvents.size >= MAX_RECENT_ENTRIES) {
    const oldest = recentEvents.keys().next().value;
    if (oldest !== undefined) recentEvents.delete(oldest);
  }
  // 重新插入刷新顺序
  if (recentEvents.has(key)) recentEvents.delete(key);
  recentEvents.set(key, now);
  return true;
}

export function registerSessionLifecycle(
  api: OpenClawPluginApi,
  config: SessionLifecycleConfig | undefined,
  notifyQueue: NotificationQueue,
) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();
  const enableSessionStart = config?.enableSessionStart !== false;
  const enableSessionEnd = config?.enableSessionEnd !== false;
  const enableBeforeReset = config?.enableBeforeReset !== false;
  const enableSubagent = config?.enableSubagent !== false;
  const debug = config?.debug === true;

  // ── Hook: session_start ─────────────────────────────────────────────────
  // 用途：每个新会话起点 —— 给一个章节占位（如果距上一个 chapter 已经过去 > 30min）+ 推通知
  // 不做：不自动 inject prompt 上下文（那是 session-recap 模块的职责，避免重复）
  if (enableSessionStart) {
    try {
      api.on("session_start", (_event, ctx) => {
        try {
          const agentId = pickAgentId(ctx);
          const sessionId = pickSessionId(ctx);
          const dedupKey = `start:${agentId}:${sessionId}`;
          if (!shouldFire(dedupKey)) return undefined;

          // 看上一个 chapter 距离多久
          const chapters = listChapters(db, agentId, sessionId, 1);
          const last = chapters[0];
          const lastMs = last ? new Date(last.created_at).getTime() : 0;
          const idleMin = lastMs ? Math.round((Date.now() - lastMs) / 60_000) : Infinity;

          // 仅当 idle > 30min 或者根本没 chapter 时才插入新章节占位
          if (idleMin >= 30) {
            const title = idleMin === Infinity
              ? "🚀 会话开始"
              : `🚀 会话续启（距上次 ${idleMin} 分钟）`;
            addChapter(db, agentId, sessionId, title, `session_start hook 自动标记`);
            if (debug) api.logger.info(`[enhance-lifecycle] session_start → 添加章节: ${title}`);
          }
        } catch (err) {
          api.logger.error(`[enhance-lifecycle] session_start handler 错误: ${(err as Error).message}`);
        }
        return undefined; // void hook
      });
    } catch {
      // hook 不可用时静默
    }
  }

  // ── Hook: session_end ───────────────────────────────────────────────────
  // 用途：会话结束自动 mark_chapter + flush 未结束的 in_progress todo 到 decision memory
  if (enableSessionEnd) {
    try {
      api.on("session_end", (_event, ctx) => {
        try {
          const agentId = pickAgentId(ctx);
          const sessionId = pickSessionId(ctx);
          const dedupKey = `end:${agentId}:${sessionId}`;
          if (!shouldFire(dedupKey)) return undefined;

          // 1) 自动加一个收尾章节
          addChapter(db, agentId, sessionId, "🏁 会话结束", "session_end hook 自动标记");

          // 2) 抢救未完成的 in_progress todo 到 decision memory（带保留 tag 防 noise factory）
          const latestTodos = getLatestTodos(db, agentId);
          const inProgress = latestTodos.filter((t) => t.status === "in_progress");
          if (inProgress.length > 0) {
            const summary = inProgress
              .map((t, i) => `${i + 1}. ${t.content.slice(0, 100)}`)
              .join("\n");
            storeMemory(
              db,
              agentId,
              "project",
              `[lifecycle:flush] 会话结束时仍有 ${inProgress.length} 条 in_progress todo 未完成：\n${summary}`,
              "session-flush", // 不进 corpus pruner 黑名单 — 用户下次会想恢复，让 pruner 按相关度自然评分
              4, // 重要性低（不是用户主动决策）
              sessionId,
              {
                why: "下次会话恢复时可从这里查看上次未完成的工作",
                howToApply: "新 session 开始时 search memory 看是否有 [lifecycle:flush] 条目",
              },
            );
            if (debug) api.logger.info(`[enhance-lifecycle] session_end → flush ${inProgress.length} 条 in_progress todo`);
          }
        } catch (err) {
          api.logger.error(`[enhance-lifecycle] session_end handler 错误: ${(err as Error).message}`);
        }
        return undefined;
      });
    } catch {
      // 静默
    }
  }

  // ── Hook: before_reset ─────────────────────────────────────────────────
  // 用途：reset 前最后机会，把 in_progress todo + 最近一条 chapter 抢救到 decision memory
  // 区别于 session_end：reset 是用户主动清理，更激进，需要更彻底的"最后挽救"
  if (enableBeforeReset) {
    try {
      api.on("before_reset", (_event, ctx) => {
        try {
          const agentId = pickAgentId(ctx);
          const sessionId = pickSessionId(ctx);
          const dedupKey = `reset:${agentId}:${sessionId}`;
          if (!shouldFire(dedupKey)) return undefined;

          const latestTodos = getLatestTodos(db, agentId);
          const open = latestTodos.filter((t) => t.status !== "completed").slice(0, 10);
          const recentChap = listChapters(db, agentId, sessionId, 3);

          if (open.length === 0 && recentChap.length === 0) return undefined;

          const lines: string[] = [];
          if (recentChap.length > 0) {
            lines.push("最近章节：");
            for (const c of recentChap) lines.push(`  • ${c.title}（${c.summary?.slice(0, 60) ?? ""}）`);
          }
          if (open.length > 0) {
            lines.push("");
            lines.push("未完成 todo：");
            for (const t of open) lines.push(`  • [${t.status}] ${t.content.slice(0, 100)}`);
          }
          const body = lines.join("\n");

          storeMemory(
            db,
            agentId,
            "decision",
            `[lifecycle:reset] reset 前抢救（${new Date().toISOString().slice(0, 19)}）：\n${body}`,
            "reset-rescue", // 不进黑名单 — 用户下次新 session 会查
            6, // reset 前抢救偏重要（用户即将清空状态）
            sessionId,
            {
              why: "reset 后这些信息可能丢失，提前固化",
              howToApply: "下次新会话用 enhance_memory_search [lifecycle:reset] 查看历史",
            },
          );
          if (debug) api.logger.info(`[enhance-lifecycle] before_reset → 抢救 ${recentChap.length} 章节 + ${open.length} todo`);

          notifyQueue.emit(
            agentId,
            "warn",
            "config-doctor",
            `enhance: 即将 reset，已固化 ${recentChap.length} 章节 + ${open.length} todo 到 decision memory`,
            body.slice(0, 500),
          );
        } catch (err) {
          api.logger.error(`[enhance-lifecycle] before_reset handler 错误: ${(err as Error).message}`);
        }
        return undefined;
      });
    } catch {
      // 静默
    }
  }

  // ── Hook: subagent_spawned / subagent_ended ────────────────────────────
  // 用途：spawn 链路追踪 — 每次派生子 agent 时自动加一个章节，结束时再加一个
  // 跟 enhance_spawn_task 闭环（之前只返回 CLI 命令，现在也跟踪生命周期）
  if (enableSubagent) {
    try {
      // subagent_spawned: ctx 字段是 { runId?, childSessionKey?, requesterSessionKey? }（无 agentId）
      // event 字段是 { agentId, label?, mode, requester?, threadRequested, runId, childSessionKey }
      api.on("subagent_spawned", (event, ctx) => {
        try {
          // ctx 没 agentId — 用 requesterSessionKey 当 sessionId 关联到父 session 的 chapter
          const sessionId = (ctx?.requesterSessionKey ?? "") + "";
          const child = event?.label ?? event?.agentId ?? "?";
          const childAgentId = event?.agentId ?? DEFAULT_AGENT_ID;
          const dedupKey = `spawn:${childAgentId}:${sessionId}:${child}`;
          if (!shouldFire(dedupKey)) return;
          addChapter(
            db,
            DEFAULT_AGENT_ID, // 父章节挂在 main agent（subagent ctx 拿不到 requester agentId）
            sessionId,
            `🤖 派生子 agent: ${child}`,
            event?.requester
              ? `mode=${event.mode}, channel=${event.requester.channel ?? "?"}, runId=${event.runId?.slice(0, 12) ?? "?"}`
              : "subagent_spawned hook 自动标记",
          );
          if (debug) api.logger.info(`[enhance-lifecycle] subagent_spawned → ${child}`);
        } catch (err) {
          api.logger.error(`[enhance-lifecycle] subagent_spawned handler 错误: ${(err as Error).message}`);
        }
      });

      api.on("subagent_ended", (event, ctx) => {
        try {
          const sessionId = (ctx?.requesterSessionKey ?? event?.targetSessionKey ?? "") + "";
          const child = event?.targetSessionKey?.slice(-12) ?? "?";
          const dedupKey = `end-spawn:${sessionId}:${child}`;
          if (!shouldFire(dedupKey)) return;
          const outcome = event?.outcome ?? "ok";
          const icon = outcome === "ok" ? "✅" : outcome === "error" ? "❌" : "⚠️";
          addChapter(
            db,
            DEFAULT_AGENT_ID,
            sessionId,
            `${icon} 子 agent 结束: ${child}`,
            `outcome=${outcome}, reason=${event?.reason?.slice(0, 100) ?? "?"}`,
          );
          if (debug) api.logger.info(`[enhance-lifecycle] subagent_ended → ${child} (${outcome})`);
        } catch (err) {
          api.logger.error(`[enhance-lifecycle] subagent_ended handler 错误: ${(err as Error).message}`);
        }
      });
    } catch {
      // 静默
    }
  }

  api.logger.info(
    `[enhance] 会话生命周期模块已加载（hooks: ${[
      enableSessionStart ? "session_start" : "",
      enableSessionEnd ? "session_end" : "",
      enableBeforeReset ? "before_reset" : "",
      enableSubagent ? "subagent_spawned/ended" : "",
    ].filter(Boolean).join(" / ")}）`,
  );
}
