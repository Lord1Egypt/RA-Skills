/**
 * 模块: enhance_spawn_task — Claude-Code 风格的"离线 TODO 孵化器"
 *
 * 与 Claude Code 的 spawn_task 相比：
 * - Claude Code 的 spawn_task 能真正开一个新会话/worktree 去跑。
 * - 龙虾没有等价原语（子 Agent 是同 session 并发执行），所以我们不假装能"真的孵化"，
 *   而是把提案写到 enhance 的"延期任务"记忆条目里（category: project, tags: spawn-task），
 *   并通过通知提示用户手动派发（可以配合 cron-cli 或手动开新 session）。
 * - 同时在 dashboard 展示最近孵化任务列表，方便用户一键拷贝提示词。
 *
 * 这样我们既对齐了 Claude Code 的语义（"这件事值得做，但不应该污染当前上下文"），
 * 又不虚假地向用户承诺龙虾没有的能力。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { getDb, storeMemory } from "../utils/sqlite-store.js";
import { DEFAULT_AGENT_ID } from "../types.js";

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

/** POSIX 单引号 shell-escape，安全嵌入多行 prompt。 */
function shellEscape(s: string): string {
  return `'${s.replace(/'/g, "'\\''")}'`;
}

/** 生成一键派发的 CLI 命令（可直接复制到终端粘贴运行）。 */
function buildCliCmd(agentId: string, prompt: string, thinking: "off" | "low" | "medium" | "high" = "low"): string {
  return `openclaw agent --agent ${agentId} --thinking ${thinking} --message ${shellEscape(prompt)}`;
}

export function registerSpawnTask(api: OpenClawPluginApi) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_spawn_task",
      description: "孵化新 session 执行的子任务（只记录，由用户决定是否新开会话）",
      parameters: Type.Object({
        title: Type.String({ description: "动词短语标题（<60 字）" }),
        prompt: Type.String({ description: "新 session 的完整自包含提示词" }),
        tldr: Type.Optional(Type.String({ description: "1-2 句摘要" })),
        tags: Type.Optional(Type.String({ description: "逗号分隔标签" })),
        targetAgent: Type.Optional(
          Type.String({ description: "目标 agent id" }),
        ),
        thinking: Type.Optional(
          Type.Union([Type.Literal("off"), Type.Literal("low"), Type.Literal("medium"), Type.Literal("high")], {
            description: "思考档，默认 low",
          }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const currentAgentId = pickAgentId(ctx);
        const sessionId = pickSessionId(ctx);
        const title = String(params.title ?? "").trim();
        const prompt = String(params.prompt ?? "").trim();
        const tldr = String(params.tldr ?? "").trim();
        const extraTags = String(params.tags ?? "").trim();
        const targetAgent = String(params.targetAgent ?? "").trim() || currentAgentId;
        const thinking = (params.thinking as "off" | "low" | "medium" | "high" | undefined) ?? "low";

        if (!title || !prompt) {
          return {
            content: [{ type: "text" as const, text: "title 和 prompt 均必填。" }],
          };
        }

        const tags = ["spawn-task", ...(extraTags ? extraTags.split(",").map((t) => t.trim()).filter(Boolean) : [])].join(",");
        const cliCmd = buildCliCmd(targetAgent, prompt, thinking);
        const content = [
          `【孵化子任务】${title}`,
          tldr ? `TL;DR: ${tldr}` : "",
          `目标 Agent: ${targetAgent}  · 思考档: ${thinking}`,
          `CLI: ${cliCmd}`,
          `Prompt:`,
          prompt,
        ]
          .filter(Boolean)
          .join("\n");

        const entry = storeMemory(db, currentAgentId, "project", content, tags, 7, sessionId, {
          howToApply: `在终端运行 \`${cliCmd}\` 即可派发该子任务到 agent=${targetAgent}。`,
        });

        return {
          content: [
            {
              type: "text" as const,
              text: [
                `✓ 已孵化子任务 #${entry.id}：${title}`,
                tldr ? `   ${tldr}` : "",
                `   一键派发（复制到终端执行）：`,
                `   ${cliCmd}`,
                `   或在仪表盘 "子任务" 标签查看；也可直接新开 session 粘贴 Prompt。`,
              ]
                .filter(Boolean)
                .join("\n"),
            },
          ],
          structuredContent: {
            id: entry.id,
            title,
            tldr,
            prompt,
            targetAgent,
            thinking,
            cliCmd,
          },
        };
      },
    })) as any,
    { name: "enhance_spawn_task" },
  );

  api.logger.info("[enhance] 子任务派发模块已加载（enhance_spawn_task）");
}
