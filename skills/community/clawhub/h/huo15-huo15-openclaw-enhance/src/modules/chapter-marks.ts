/**
 * 模块: 章节标记（Claude-Code 风格 mark_chapter）
 *
 * 把长会话切成可回溯的章节。仪表盘用它生成时间线。
 * 与龙虾原生 session 的关系：龙虾只有 session 本身，没有章节概念；
 * 本模块是纯新增，完全不影响龙虾 session 内部状态。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { getDb, addChapter, listChapters } from "../utils/sqlite-store.js";
import { DEFAULT_AGENT_ID } from "../types.js";

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

export function registerChapterMarks(api: OpenClawPluginApi) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_mark_chapter",
      description: "标记会话章节（阶段切换时用，一会话 3-8 个）",
      parameters: Type.Object({
        title: Type.String({ description: "短名词短语，<40 字" }),
        summary: Type.Optional(Type.String({ description: "一行摘要" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const title = String(params.title ?? "").trim();
        if (!title) {
          return {
            content: [{ type: "text" as const, text: "章节标题不能为空。" }],
          };
        }
        const chapter = addChapter(db, agentId, sessionId, title.slice(0, 80), String(params.summary ?? "").trim());
        return {
          content: [
            {
              type: "text" as const,
              text: `✓ 章节已标记 #${chapter.id}：${chapter.title}${chapter.summary ? ` — ${chapter.summary}` : ""}`,
            },
          ],
        };
      },
    })) as any,
    { name: "enhance_mark_chapter" },
  );

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_chapter_list",
      description: "查看 session 或 Agent 章节时间线",
      parameters: Type.Object({
        scope: Type.Optional(
          Type.Union([Type.Literal("session"), Type.Literal("agent")], {
            description: "session(默认)|agent",
          }),
        ),
        limit: Type.Optional(Type.Integer({ description: "默认 50" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const limit = Number(params.limit ?? 50);
        const scope = params.scope === "agent" ? undefined : sessionId;
        const rows = listChapters(db, agentId, scope, limit);
        if (rows.length === 0) {
          return {
            content: [{ type: "text" as const, text: `暂无章节记录 (agent: ${agentId})。` }],
          };
        }
        const lines = rows.map(
          (c) => `· ${c.created_at} · #${c.id} ${c.title}${c.summary ? ` — ${c.summary}` : ""}`,
        );
        return {
          content: [{ type: "text" as const, text: `章节时间线（${rows.length} 条）：\n${lines.join("\n")}` }],
        };
      },
    })) as any,
    { name: "enhance_chapter_list" },
  );

  api.logger.info("[enhance] 章节标记模块已加载（enhance_mark_chapter / chapter_list）");
}
