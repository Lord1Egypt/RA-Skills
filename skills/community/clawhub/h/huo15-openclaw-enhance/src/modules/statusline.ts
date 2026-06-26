/**
 * 模块: 状态栏
 *
 * 龙虾的状态展示通常依赖 CLI/Control UI，缺少一个"一眼看全插件增强信号"的入口。
 * 本模块做两件事：
 *  1. 暴露 enhance_statusline 工具：模型/用户随时查询当前模式、任务、记忆命中、宠物。
 *  2. 挂 HTTP 路由 /plugins/enhance/api/statusline，JSON 快照，方便 Control UI 嵌入。
 *
 * 纯只读，绝不影响龙虾运行状态。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import type Database from "better-sqlite3";
import {
  getLatestTodos,
  listChapters,
  getMemoryStats,
  getOrCreatePet,
  listScheduledBindings,
} from "../utils/sqlite-store.js";
import type { NotificationQueue, TodoEntry } from "../types.js";
import { DEFAULT_AGENT_ID } from "../types.js";
import { getCurrentMode } from "./mode-gate.js";

/** Observability bits read from ctx / runtimeConfig at tool-call time. */
export interface ObservabilityContext {
  model?: string;
  thinking?: string;
  fastMode?: boolean;
  channel?: string;
  sessionId?: string;
}

function pickObservability(ctx: unknown): ObservabilityContext {
  const c = ctx as {
    runtimeConfig?: { agents?: { defaults?: any; list?: any[] } };
    agentId?: string;
    sessionId?: string;
    sessionKey?: string;
    messageChannel?: string;
  } | undefined;
  const agentId = c?.agentId;
  const agents = c?.runtimeConfig?.agents;
  const defaults = agents?.defaults;
  const cfg = agents?.list?.find((a: { id?: string }) => a?.id === agentId) ?? defaults ?? {};
  const modelCfg = cfg?.model ?? defaults?.model;
  const modelStr = typeof modelCfg === "string"
    ? modelCfg
    : (modelCfg?.primary ?? undefined);
  return {
    model: modelStr,
    thinking: cfg?.thinkingDefault ?? defaults?.thinkingDefault,
    fastMode: cfg?.fastModeDefault ?? defaults?.fastModeDefault,
    channel: c?.messageChannel,
    sessionId: c?.sessionId ?? c?.sessionKey,
  };
}

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

function summariseTodos(todos: TodoEntry[]): { done: number; total: number; active?: string } {
  const done = todos.filter((t) => t.status === "completed").length;
  const active = todos.find((t) => t.status === "in_progress")?.content;
  return { done, total: todos.length, active };
}

interface Snapshot {
  agentId: string;
  mode: string;
  todos: { done: number; total: number; active?: string };
  chaptersToday: number;
  memory: { total: number; byCategory: Record<string, number> };
  unreadNotifications: number;
  pet: { name: string; level: number; color: string; mood: string };
  scheduledBindings: number;
  /** Observability (runtime-only; undefined if not resolvable). */
  observability?: ObservabilityContext;
}

export function buildSnapshot(
  db: Database.Database,
  agentId: string,
  sessionId: string,
  notifyQueue: NotificationQueue,
  observability?: ObservabilityContext,
): Snapshot {
  const todos = getLatestTodos(db, agentId);
  const chapters = listChapters(db, agentId, undefined, 200).filter((c) => {
    const created = new Date(c.created_at).getTime();
    return Date.now() - created < 24 * 60 * 60 * 1000;
  });
  const memoryStats = getMemoryStats(db, agentId);
  const totalMem = memoryStats.total ?? 0;
  const byCat: Record<string, number> = {};
  for (const [k, v] of Object.entries(memoryStats)) {
    if (k !== "total") byCat[k] = v;
  }
  const pet = getOrCreatePet(db, agentId);
  const scheduled = listScheduledBindings(db, agentId).filter((b) => b.enabled === 1);
  return {
    agentId,
    mode: getCurrentMode(agentId, sessionId),
    todos: summariseTodos(todos),
    chaptersToday: chapters.length,
    memory: { total: totalMem, byCategory: byCat },
    unreadNotifications: notifyQueue.getUnreadCount(agentId),
    pet: { name: pet.name, level: pet.level, color: pet.color, mood: pet.mood },
    scheduledBindings: scheduled.length,
    observability,
  };
}

function renderLine(snap: Snapshot): string {
  const parts = [
    `agent=${snap.agentId}`,
    `mode=${snap.mode}`,
    `todos=${snap.todos.done}/${snap.todos.total}`,
  ];
  if (snap.todos.active) parts.push(`▶ ${snap.todos.active}`);
  parts.push(`mem=${snap.memory.total}`);
  parts.push(`chapters(24h)=${snap.chaptersToday}`);
  if (snap.unreadNotifications > 0) parts.push(`notif=${snap.unreadNotifications}`);
  parts.push(`🔥${snap.pet.name}·Lv${snap.pet.level}`);
  if (snap.scheduledBindings > 0) parts.push(`cron=${snap.scheduledBindings}`);
  const obs = snap.observability;
  if (obs?.model) parts.push(`model=${obs.model}`);
  if (obs?.thinking && obs.thinking !== "off") parts.push(`think=${obs.thinking}`);
  if (obs?.fastMode) parts.push(`fast`);
  if (obs?.channel) parts.push(`ch=${obs.channel}`);
  return parts.join(" · ");
}

export function registerStatusline(
  api: OpenClawPluginApi,
  db: Database.Database,
  notifyQueue: NotificationQueue,
) {
  // Tool
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_statusline",
      description: "查看 Agent/session 状态快照（模式、任务、记忆、宠物、通知）",
      parameters: Type.Object({
        format: Type.Optional(
          Type.Union([Type.Literal("line"), Type.Literal("detail"), Type.Literal("json")], {
            description: "line(默认)|detail|json",
          }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const obs = pickObservability(ctx);
        const snap = buildSnapshot(db, agentId, sessionId, notifyQueue, obs);
        const format = (params.format as string | undefined) ?? "line";
        if (format === "json") {
          return { content: [{ type: "text" as const, text: JSON.stringify(snap, null, 2) }] };
        }
        if (format === "detail") {
          const memLines = Object.entries(snap.memory.byCategory)
            .map(([k, v]) => `  · ${k}: ${v}`)
            .join("\n");
          const obsLines: string[] = [];
          if (snap.observability?.model) obsLines.push(`模型: ${snap.observability.model}`);
          if (snap.observability?.thinking) obsLines.push(`思考档: ${snap.observability.thinking}`);
          if (snap.observability?.fastMode) obsLines.push(`快速模式: 开`);
          if (snap.observability?.channel) obsLines.push(`通道: ${snap.observability.channel}`);
          if (snap.observability?.sessionId) obsLines.push(`Session: ${snap.observability.sessionId.slice(0, 12)}`);
          const text = [
            `📊 状态快照 (agent: ${snap.agentId})`,
            `模式: ${snap.mode}`,
            `任务: ${snap.todos.done}/${snap.todos.total}${snap.todos.active ? ` · 进行中：${snap.todos.active}` : ""}`,
            `记忆: ${snap.memory.total} 条`,
            memLines,
            `章节(24h): ${snap.chaptersToday}`,
            `未读通知: ${snap.unreadNotifications}`,
            `🔥 ${snap.pet.name}（Lv${snap.pet.level}·${snap.pet.color}·${snap.pet.mood}）`,
            `定时任务: ${snap.scheduledBindings}`,
            ...(obsLines.length > 0 ? [``, `— 可观测性 —`, ...obsLines] : []),
          ].join("\n");
          return { content: [{ type: "text" as const, text }] };
        }
        return { content: [{ type: "text" as const, text: renderLine(snap) }] };
      },
    })) as any,
    { name: "enhance_statusline" },
  );

  api.logger.info("[enhance] 状态栏模块已加载（enhance_statusline；HTTP 端点由仪表盘路由 /plugins/enhance/api/statusline 提供）");
}
