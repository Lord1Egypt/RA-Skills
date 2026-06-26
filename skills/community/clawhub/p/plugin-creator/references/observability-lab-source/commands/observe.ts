import type { OpenClawPluginApi, PluginCommandContext, PluginCommandResult } from "../api.js";
import {
  DEFAULT_TRANSCRIPT_PREFIX,
  OBSERVABILITY_LAB_MESSAGE_MARKER,
  OBSERVABILITY_LAB_PLUGIN_ID,
  flushTelemetryEvents,
  readObservabilityLabConfig,
  readTelemetryTail,
  updateObservabilityLabConfig,
} from "../src/observability.js";

function parseObserveArgs(args: string | undefined): string[] {
  // 这里的命令语法很简单，直接按空白切分就足够了。
  return (args?.trim().toLowerCase() || "status").split(/\s+/).filter(Boolean);
}

export async function runObserveCommand(
  api: OpenClawPluginApi,
  ctx: PluginCommandContext,
): Promise<PluginCommandResult> {
  const cfg = api.runtime.config.loadConfig();
  const settings = readObservabilityLabConfig(cfg);
  const [action = "status", detail = ""] = parseObserveArgs(ctx.args);

  if (action === "status" || action === "") {
    return {
      text: [
        `${OBSERVABILITY_LAB_MESSAGE_MARKER} 状态`,
        `- 录制开关：${settings.captureEnabled ? "开启" : "关闭"}`,
        `- 改写开关：${settings.rewriteEnabled ? "开启" : "关闭"}`,
        `- 转写前缀：${settings.transcriptPrefix}`,
        "- Hook：message_received、llm_input、llm_output、before_tool_call、after_tool_call、before_message_write、session_start、session_end",
        `- 遥测文件：${api.runtime.state.resolveStateDir()}/plugins/${OBSERVABILITY_LAB_PLUGIN_ID}/telemetry.jsonl`,
        "- 说明：只有当前会话命中本插件命令或技能后，才会开始记录后续事件；会话结束后自动停止。",
      ].join("\n"),
    };
  }

  if (action === "on" || action === "off") {
    const next = updateObservabilityLabConfig(cfg, { captureEnabled: action === "on" });
    await api.runtime.config.writeConfigFile(next);
    return {
      text: `${OBSERVABILITY_LAB_MESSAGE_MARKER} 录制已${action === "on" ? "开启" : "关闭"}。`,
    };
  }

  if (action === "rewrite") {
    // 改写控制的是同步的 before_message_write 路径。
    if (detail === "status" || detail === "") {
      return {
        text: `${OBSERVABILITY_LAB_MESSAGE_MARKER} 改写当前为${settings.rewriteEnabled ? "开启" : "关闭"}（前缀：${settings.transcriptPrefix}）。`,
      };
    }
    if (detail === "on" || detail === "off") {
      const next = updateObservabilityLabConfig(cfg, { rewriteEnabled: detail === "on" });
      await api.runtime.config.writeConfigFile(next);
      return {
        text: `${OBSERVABILITY_LAB_MESSAGE_MARKER} 改写已${detail === "on" ? "开启" : "关闭"}（前缀：${settings.transcriptPrefix}）。`,
      };
    }
  }

  if (action === "prefix") {
    // 这里要保留空格，所以不能复用上面的 lower-case token 结果，而是回到原始参数重组。
    const nextPrefix = ctx.args?.trim().split(/\s+/).slice(1).join(" ") || DEFAULT_TRANSCRIPT_PREFIX;
    const next = updateObservabilityLabConfig(cfg, { transcriptPrefix: nextPrefix });
    await api.runtime.config.writeConfigFile(next);
    return {
      text: `${OBSERVABILITY_LAB_MESSAGE_MARKER} 转写前缀已更新为：${nextPrefix}`,
    };
  }

  return {
    text: [
      `${OBSERVABILITY_LAB_MESSAGE_MARKER} 用法`,
      "/observe status",
      "/observe on",
      "/observe off",
      "/observe rewrite <on|off|status>",
      "/observe prefix <文本>",
    ].join("\n"),
  };
}

export function runObserveHelpCommand(): PluginCommandResult {
  // 帮助文案和命令实现放在一起，后续拿这个插件当脚手架时更容易复制和改造。
  return {
    text: [
      `${OBSERVABILITY_LAB_MESSAGE_MARKER} 使用说明`,
      "",
      "插件命令：",
      "/observe status",
      "/observe on",
      "/observe off",
      "/observe rewrite on",
      "/observe rewrite off",
      "/observe prefix [text]",
      "/observe_tail",
      "/observe_help",
      "",
      "技能命令：",
      "/observe_demo <text>",
      "/skill observe-demo <text>",
      "",
      "说明：",
      "- 遥测会先写入内存队列，再异步刷入本地 JSONL 文件",
      "- 只有当前会话命中本插件命令或 observe-demo 技能后，才会开始记录后续事件",
      "- 记录范围会持续到本次会话结束，不会自动影响下一次新会话",
      "- before_message_write 可以同步改写 assistant 转写文本，不会阻塞文件 I/O",
      "- /observe_demo 现在是真正的 skill；是否调用工具由 agent 按 skill 指令自己决定",
    ].join("\n"),
  };
}

export async function runObserveTailCommand(api: OpenClawPluginApi): Promise<PluginCommandResult> {
  const stateDir = api.runtime.state.resolveStateDir();
  // tail 是给人看的检查命令，所以这里优先保证“最新”，先 flush 再读文件。
  await flushTelemetryEvents({ stateDir });
  const tail = await readTelemetryTail({ stateDir, limit: 5 });
  if (tail.length === 0) {
    return { text: `${OBSERVABILITY_LAB_MESSAGE_MARKER} 当前还没有已落盘的遥测记录。` };
  }
  return {
    text: [
      `${OBSERVABILITY_LAB_MESSAGE_MARKER} 最近遥测：`,
      ...tail.map((entry, index) => `${index + 1}. ${entry.type}`),
    ].join("\n"),
  };
}
