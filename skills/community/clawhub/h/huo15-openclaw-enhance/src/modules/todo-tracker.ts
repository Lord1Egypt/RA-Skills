/**
 * 模块: 任务追踪（Claude-Code 风格 TodoWrite）
 *
 * - enhance_todo_write(todos[]): 整组覆盖式写入（与 Claude Code 语义一致）
 * - enhance_todo_update(position, status): 单项状态变更，不动顺序
 * - enhance_todo_list(): 查看当前 session 的任务
 *
 * 与龙虾原生 task tool 的区分：
 * - 龙虾的 "task" 指并发子 Agent（Agent tool）。
 * - 本模块是轻量级的"清单/进度条"，面向主 Agent 自身的心流管理，
 *   仪表盘会实时显示。不启动子 Agent，不读龙虾 task 执行栈。
 *
 * 龙虾原生未提供 TodoWrite 等价物，因此本模块纯新增，不与龙虾功能重复。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import {
  getDb,
  replaceTodos,
  listTodos,
  updateTodoStatus,
  type TodoInput,
} from "../utils/sqlite-store.js";
import type { NotificationQueue, TodoEntry } from "../types.js";
import { DEFAULT_AGENT_ID } from "../types.js";

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

function renderTodo(t: TodoEntry): string {
  const marker = t.status === "completed" ? "[x]" : t.status === "in_progress" ? "[~]" : "[ ]";
  const active = t.status === "in_progress" ? ` — ${t.active_form}` : "";
  return `${marker} ${t.content}${active}`;
}

function summarize(rows: TodoEntry[]): string {
  if (rows.length === 0) return "（无任务）";
  const done = rows.filter((r) => r.status === "completed").length;
  const active = rows.find((r) => r.status === "in_progress");
  const head = `任务清单（${done}/${rows.length} 完成${active ? `，进行中：${active.content}` : ""}）：`;
  return [head, ...rows.map(renderTodo)].join("\n");
}

export function registerTodoTracker(api: OpenClawPluginApi, notifyQueue: NotificationQueue) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();

  // enhance_todo_write — 覆盖式写入整组
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_todo_write",
      description: "维护任务清单（整组覆盖写入）；任务≥3步用，同时只一项 in_progress",
      parameters: Type.Object({
        todos: Type.Array(
          Type.Object({
            content: Type.String({ description: "任务内容（祈使句）" }),
            activeForm: Type.String({ description: "进行中展示形式" }),
            status: Type.Optional(
              Type.Union(
                [Type.Literal("pending"), Type.Literal("in_progress"), Type.Literal("completed")],
                { description: "默认 pending" },
              ),
            ),
          }),
          { description: "覆盖式写入；空数组=清空" },
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const todos = ((params.todos as TodoInput[]) ?? []).map((t) => ({
          content: String(t.content ?? "").trim(),
          activeForm: String(t.activeForm ?? "").trim() || String(t.content ?? "").trim(),
          status: (t.status ?? "pending") as TodoInput["status"],
        })).filter((t) => t.content.length > 0);

        const stored = replaceTodos(db, agentId, sessionId, todos);

        const inProgressCount = stored.filter((r) => r.status === "in_progress").length;
        if (inProgressCount > 1) {
          notifyQueue.emit(
            agentId,
            "warn",
            "workflow",
            "任务清单提醒",
            `检测到 ${inProgressCount} 个 in_progress 任务；建议同一时间只保留一个。`,
          );
        }

        return {
          content: [
            { type: "text" as const, text: summarize(stored) },
          ],
        };
      },
    })) as any,
    { name: "enhance_todo_write" },
  );

  // enhance_todo_update — 单项状态变更
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_todo_update",
      description: "更新单条任务状态（按 position 索引，完成后立即调用）",
      parameters: Type.Object({
        position: Type.Integer({ description: "位置（从 0 开始）" }),
        status: Type.Union(
          [Type.Literal("pending"), Type.Literal("in_progress"), Type.Literal("completed")],
          { description: "目标状态" },
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const updated = updateTodoStatus(
          db,
          agentId,
          sessionId,
          Number(params.position ?? -1),
          params.status as any,
        );
        if (!updated) {
          return {
            content: [{ type: "text" as const, text: `未找到 position=${params.position} 的任务。` }],
          };
        }
        const all = listTodos(db, agentId, sessionId);
        return {
          content: [{ type: "text" as const, text: `已更新：${renderTodo(updated)}\n\n${summarize(all)}` }],
        };
      },
    })) as any,
    { name: "enhance_todo_update" },
  );

  // enhance_todo_list — 查询
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_todo_list",
      description: "查看当前 session 的任务清单。",
      parameters: Type.Object({}),
      async execute() {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const rows = listTodos(db, agentId, sessionId);
        return {
          content: [{ type: "text" as const, text: summarize(rows) }],
        };
      },
    })) as any,
    { name: "enhance_todo_list" },
  );

  api.logger.info("[enhance] 任务追踪模块已加载（enhance_todo_write / update / list）");
}
