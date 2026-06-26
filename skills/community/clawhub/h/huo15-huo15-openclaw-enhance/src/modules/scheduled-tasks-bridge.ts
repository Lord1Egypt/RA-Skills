/**
 * 模块: 定时任务桥（scheduled-tasks bridge）
 *
 * 龙虾提供了 cron-cli（`openclaw cron ...`）用于创建/列出定时任务，但插件侧没有 API 能直接
 * 注册 cron。本模块的桥接策略：
 *
 *  1. 用户/Agent 通过 enhance_loop_register 声明一个"希望定时触发的工作流"。
 *  2. 本模块把声明写入 scheduled_task_bindings 表，并在响应里**返回一条确切的 openclaw cron
 *     CLI 命令**，由用户一键复制执行（我们不擅自代替用户运行 CLI）。
 *  3. Cron 真正触发时，会回调 openclaw 的主循环并通过一个约定的入口消息重新唤起 session，
 *     此时 enhance 的 before_prompt_build 看到消息前缀 `[enhance-loop:{name}]` 就能把对应
 *     binding 的 instructions 注入上下文（和 workflow-hooks 复用）。
 *
 * 这样做的好处：
 *  - 不绕过龙虾的 cron-cli（尊重"host 调度"原则）。
 *  - Plugin 只负责登记 + 触发时装填上下文，cron 生命周期归龙虾管。
 *  - 用户可以直接用 `openclaw cron list` 看到真实调度状态，不会出现"双源真相"。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import {
  getDb,
  upsertScheduledBinding,
  listScheduledBindings,
  disableScheduledBinding,
  touchScheduledBindingFired,
} from "../utils/sqlite-store.js";
import { DEFAULT_AGENT_ID } from "../types.js";

const LOOP_MARKER_RE = /^\[enhance-loop:([^\]]+)\]/;

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID);
}

function quote(s: string): string {
  return `'${s.replace(/'/g, "'\\''")}'`;
}

export function registerScheduledTasksBridge(api: OpenClawPluginApi) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();

  // ── Hook: before_prompt_build ── 识别 loop 前缀并注入对应 binding 的 instructions
  // v5.7.8: typed via openclaw 4.24 SDK
  api.on("before_prompt_build", (event, ctx) => {
    const prompt = String((event as { prompt?: string } | undefined)?.prompt ?? "");
    const match = prompt.match(LOOP_MARKER_RE);
    if (!match) return;

    const agentId = pickAgentId(ctx);
    const name = match[1].trim();
    const binding = listScheduledBindings(db, agentId).find((b) => b.name === name && b.enabled === 1);
    if (!binding) return;

    touchScheduledBindingFired(db, binding.id);

    const header = `【定时任务 ${name}】已由 openclaw cron 触发。按下面的指令执行：\n`;
    return {
      prependContext: header + binding.instructions,
    };
  });

  // ── Tool: enhance_loop_register ──
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_loop_register",
      description: "登记定时工作流，返回一条 openclaw cron add 命令供用户挂到调度器",
      parameters: Type.Object({
        name: Type.String({ description: "任务名（agent 内唯一）" }),
        cron: Type.String({ description: "cron 表达式" }),
        instructions: Type.String({ description: "触发时注入给 Agent 的指令" }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const name = String(params.name ?? "").trim();
        const cron = String(params.cron ?? "").trim();
        const instructions = String(params.instructions ?? "").trim();

        if (!name || !cron || !instructions) {
          return {
            content: [{ type: "text" as const, text: "name/cron/instructions 均必填。" }],
          };
        }

        const binding = upsertScheduledBinding(db, agentId, name, cron, instructions);

        const triggerMessage = `[enhance-loop:${name}] 定时触发，请执行 ${name} 工作流。`;
        const cliCmd = `openclaw cron add --name ${quote(`enhance-${name}`)} --cron ${quote(cron)} --message ${quote(triggerMessage)} --agent ${quote(agentId)}`;

        return {
          content: [
            {
              type: "text" as const,
              text: [
                `✓ 已登记定时工作流 #${binding.id}：${name}（agent: ${agentId}）`,
                "",
                "下一步（手动挂到龙虾原生调度器）：",
                "```",
                cliCmd,
                "```",
                "",
                "触发时 enhance 会拦截消息前缀，把以下内容注入给 Agent：",
                "---",
                instructions,
                "---",
                "",
                "停用：enhance_loop_disable(name)",
              ].join("\n"),
            },
          ],
        };
      },
    })) as any,
    { name: "enhance_loop_register" },
  );

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_loop_list",
      description: "列出当前 Agent 已登记的定时工作流",
      parameters: Type.Object({}),
      async execute() {
        const agentId = pickAgentId(ctx);
        const rows = listScheduledBindings(db, agentId);
        if (rows.length === 0) {
          return {
            content: [{ type: "text" as const, text: `暂无定时工作流 (agent: ${agentId})。` }],
          };
        }
        const lines = rows.map(
          (r) =>
            `${r.enabled ? "●" : "○"} ${r.name} · cron=${r.cron_ref} · last_fired=${r.last_fired_at ?? "never"}\n    ${r.instructions.slice(0, 100)}${r.instructions.length > 100 ? "…" : ""}`,
        );
        return {
          content: [{ type: "text" as const, text: `定时工作流 (${rows.length})：\n${lines.join("\n\n")}` }],
        };
      },
    })) as any,
    { name: "enhance_loop_list" },
  );

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_loop_disable",
      description: "停用定时工作流（软删除，仍需手动 openclaw cron remove）",
      parameters: Type.Object({
        name: Type.String({ description: "登记时的 name" }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = pickAgentId(ctx);
        const name = String(params.name ?? "").trim();
        const ok = disableScheduledBinding(db, agentId, name);
        const cliCmd = `openclaw cron remove --name ${quote(`enhance-${name}`)}`;
        return {
          content: [
            {
              type: "text" as const,
              text: ok
                ? `✓ enhance 侧已停用 ${name}。\n别忘了去龙虾原生调度器里移除：\n  ${cliCmd}`
                : `未找到名为 ${name} 的定时工作流。`,
            },
          ],
        };
      },
    })) as any,
    { name: "enhance_loop_disable" },
  );

  api.logger.info("[enhance] 定时任务桥模块已加载（enhance_loop_register/list/disable，通过 openclaw cron-cli 挂载）");
}
