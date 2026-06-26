/**
 * 模块3: 提示词增强（多 Agent 隔离版）
 *
 * before_prompt_build hook 签名:
 *   event: { prompt, messages }
 *   ctx:   { runId, agentId, sessionKey, sessionId, workspaceDir, messageProvider, trigger, channelId }
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { DEFAULT_AGENT_ID, type PromptConfig, type PromptSection } from "../types.js";

// 仅保留 openclaw 内置系统提示词未覆盖的段落：
// - taskClassification 已移除：openclaw "## Execution Bias" 已覆盖
// - safetyAwareness 已移除：openclaw "## Safety" 已覆盖
// - memoryInstructions 已移除：openclaw memory-core "## Memory Recall" 已覆盖
const SECTIONS: Record<PromptSection, string> = {
  qualityGuidelines: [
    "## 响应质量准则（增强包）",
    "- 直接给出答案或行动，不要先复述用户说了什么",
    "- 一句话能说清的不要用三句话",
    "- 修 bug 不要顺手重构周围代码",
    "- 不要添加请求之外的功能、注释或类型标注",
    "- 不要为不可能发生的场景做错误处理",
    "- 三行相似代码好过一个过早的抽象",
    "- 失败时先诊断原因，不要盲目重试",
    "- 做破坏性操作前先确认（删除、force push、覆盖未保存的修改）",
  ].join("\n"),
};

export function registerPromptEnhancer(api: OpenClawPluginApi, config?: PromptConfig) {
  // 默认只启用质量准则；memoryInstructions 仅作为托底（结构化记忆模块禁用时才需要）
  const enabledSections: PromptSection[] = config?.sections ?? ["qualityGuidelines"];

  api.on("before_prompt_build", (_event, ctx) => {
    const agentId = (ctx?.agentId ?? DEFAULT_AGENT_ID).trim();
    const parts: string[] = [];

    for (const section of enabledSections) {
      const content = SECTIONS[section];
      if (content) parts.push(content);
    }

    if (parts.length === 0) return {};

    return {
      appendSystemContext: [
        `\n\n<!-- enhance-prompt agent:${agentId} -->`,
        ...parts,
      ].join("\n\n"),
    };
  });

  api.logger.info(`[enhance] 提示词增强模块已加载，启用段落: ${enabledSections.join(", ")}`);
}
