import { Type } from "@sinclair/typebox";
import type { AnyAgentTool } from "../api.js";
import { OBSERVABILITY_LAB_MESSAGE_MARKER, OBSERVABILITY_LAB_PLUGIN_ID } from "../src/observability.js";

export function createObserveDemoEchoTool(): AnyAgentTool {
  return {
    name: "observe_demo_echo",
    label: "Observe Demo Echo",
    description: "Return a deterministic confirmation for the observe-demo skill.",
    parameters: Type.Object({
      command: Type.Optional(Type.String()),
      commandName: Type.Optional(Type.String()),
      skillName: Type.Optional(Type.String()),
    }),
    async execute(_toolCallId: string, params: Record<string, unknown>) {
      // 这个演示技能故意做成确定性输出，这样验证插件内 skill 是否生效时不依赖模型随机性。
      const rawInput = typeof params.command === "string" ? params.command : "";
      const commandName = typeof params.commandName === "string" ? params.commandName : "observe_demo";
      const skillName = typeof params.skillName === "string" ? params.skillName : "observe-demo";
      return {
        content: [
          {
            type: "text",
            text: [
              `${OBSERVABILITY_LAB_MESSAGE_MARKER} 技能调用已确认`,
              `- 插件：${OBSERVABILITY_LAB_PLUGIN_ID}`,
              `- 技能：${skillName}`,
              `- 命令：${commandName}`,
              `- 输入：${rawInput || "（空）"}`,
            ].join("\n"),
          },
        ],
        details: {
          pluginId: OBSERVABILITY_LAB_PLUGIN_ID,
          skillName,
          commandName,
          input: rawInput,
        },
      };
    },
  } as AnyAgentTool;
}
