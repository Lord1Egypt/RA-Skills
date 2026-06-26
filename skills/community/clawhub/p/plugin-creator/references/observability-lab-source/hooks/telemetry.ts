import type {
  OpenClawPluginApi,
  PluginHookAfterToolCallEvent,
  PluginHookBeforeMessageWriteEvent,
  PluginHookBeforeMessageWriteResult,
  PluginHookBeforeToolCallEvent,
  PluginHookLlmInputEvent,
  PluginHookLlmOutputEvent,
  PluginHookMessageContext,
  PluginHookMessageReceivedEvent,
  PluginHookSessionContext,
  PluginHookSessionEndEvent,
  PluginHookSessionStartEvent,
  PluginHookToolContext,
} from "../api.js";
import {
  activateConversationCapture,
  activateSessionCapture,
  deactivateConversationCapture,
  deactivateSessionCapture,
  enqueueTelemetryEvent,
  flushTelemetryEvents,
  isConversationCaptureActive,
  isSessionCaptureActive,
  OBSERVABILITY_LAB_MESSAGE_MARKER,
  readObservabilityLabConfig,
} from "../src/observability.js";

function isPluginTriggerMessage(content: string): boolean {
  const normalized = content.trim().toLowerCase();
  return (
    normalized.startsWith("/observe ") ||
    normalized === "/observe" ||
    normalized === "/observe_help" ||
    normalized === "/observe_tail" ||
    normalized.startsWith("/observe_demo ") ||
    normalized === "/observe_demo" ||
    normalized.startsWith("/skill observe-demo")
  );
}

function isSessionResetMessage(content: string): boolean {
  const normalized = content.trim().toLowerCase();
  return normalized === "/new" || normalized === "/reset";
}

function getMessageText(message: PluginHookBeforeMessageWriteEvent["message"]): string {
  if (typeof (message as { content?: unknown }).content === "string") {
    return (message as { content: string }).content;
  }
  const content = (message as { content?: unknown }).content;
  if (!Array.isArray(content)) {
    return "";
  }
  return content
    .filter(
      (part) =>
        typeof part === "object" &&
        part !== null &&
        (part as { type?: unknown }).type === "text" &&
        typeof (part as { text?: unknown }).text === "string",
    )
    .map((part) => (part as { text: string }).text)
    .join("\n");
}

function prefixAssistantMessage(
  message: PluginHookBeforeMessageWriteEvent["message"],
  prefix: string,
): PluginHookBeforeMessageWriteEvent["message"] | undefined {
  if ((message as { role?: unknown }).role !== "assistant") {
    return undefined;
  }

  if (typeof (message as { content?: unknown }).content === "string") {
    const content = (message as { content: string }).content;
    if (content.startsWith(prefix)) {
      return undefined;
    }
    return {
      ...(message as Record<string, unknown>),
      content: `${prefix}${content}`,
    } as PluginHookBeforeMessageWriteEvent["message"];
  }

  const content = (message as { content?: unknown }).content;
  if (!Array.isArray(content)) {
    return undefined;
  }

  // 只改写第一个可见文本块，避免误伤 toolCall 或 thinking 这类非用户可见内容。
  const textIndex = content.findIndex(
    (part) =>
      typeof part === "object" &&
      part !== null &&
      (part as { type?: unknown }).type === "text" &&
      typeof (part as { text?: unknown }).text === "string",
  );
  if (textIndex === -1) {
    return undefined;
  }

  const nextParts = [...content];
  const textPart = nextParts[textIndex] as { text: string };
  if (textPart.text.startsWith(prefix)) {
    return undefined;
  }
  nextParts[textIndex] = {
    ...textPart,
    text: `${prefix}${textPart.text}`,
  };
  return {
    ...(message as Record<string, unknown>),
    content: nextParts,
  } as PluginHookBeforeMessageWriteEvent["message"];
}

async function maybeRecordSessionEvent(
  api: OpenClawPluginApi,
  type: "session_start" | "session_end",
  event: PluginHookSessionStartEvent | PluginHookSessionEndEvent,
  context: PluginHookSessionContext,
): Promise<void> {
  const stateDir = api.runtime.state.resolveStateDir();
  const sessionKey = context.sessionKey;
  if (type === "session_start") {
    // 新 session 开始时，显式清掉同一个 sessionKey 上的旧激活态，避免 /new 后串话。
    deactivateSessionCapture(sessionKey);
    return;
  }

  const cfg = api.runtime.config.loadConfig();
  const canCapture = readObservabilityLabConfig(cfg).captureEnabled;
  const active = isSessionCaptureActive(sessionKey);
  if (canCapture && active) {
    enqueueTelemetryEvent({
      stateDir,
      record: {
        type,
        at: new Date().toISOString(),
        event: { ...event },
        context: { ...context },
      },
    });
  }
  if (type === "session_end") {
    // 会话结束时，无论是否记录过，都要清掉激活态，确保不会污染下一次新会话。
    deactivateSessionCapture(sessionKey);
    // session_end 是一个低频节点，适合作为异步文件刷盘的收口点。
    await flushTelemetryEvents({ stateDir });
  }
}

async function maybeRecordMessageEvent(
  api: OpenClawPluginApi,
  type: "message_received",
  event: PluginHookMessageReceivedEvent,
  context: PluginHookMessageContext,
): Promise<void> {
  if (isSessionResetMessage(event.content)) {
    // 用户显式开启新会话或重置会话时，当前对话入口上的激活态也要一并清掉。
    deactivateConversationCapture(context);
    return;
  }

  if (isPluginTriggerMessage(event.content)) {
    // 命中本插件命令或技能时，只把“当前对话入口”标记为已激活；等后续拿到
    // sessionKey 的 hook 再把真正的会话级观测打开。
    activateConversationCapture(context);
    return;
  }

  if (!isConversationCaptureActive(context)) {
    return;
  }
  const cfg = api.runtime.config.loadConfig();
  if (!readObservabilityLabConfig(cfg).captureEnabled) {
    return;
  }
  enqueueTelemetryEvent({
    stateDir: api.runtime.state.resolveStateDir(),
    record: {
      type,
      at: new Date().toISOString(),
      event: { ...event },
      context: { ...context },
    },
  });
}

async function maybeRecordAgentEvent(
  api: OpenClawPluginApi,
  type: "llm_input" | "llm_output",
  event: PluginHookLlmInputEvent | PluginHookLlmOutputEvent,
  context: PluginHookSessionContext,
): Promise<void> {
  if (!isSessionCaptureActive(context.sessionKey)) {
    return;
  }
  const cfg = api.runtime.config.loadConfig();
  if (!readObservabilityLabConfig(cfg).captureEnabled) {
    return;
  }
  enqueueTelemetryEvent({
    stateDir: api.runtime.state.resolveStateDir(),
    record: {
      type,
      at: new Date().toISOString(),
      event: { ...event },
      context: { ...context },
    },
  });
}

async function maybeRecordToolEvent(
  api: OpenClawPluginApi,
  type: "before_tool_call" | "after_tool_call",
  event: PluginHookBeforeToolCallEvent | PluginHookAfterToolCallEvent,
  context: PluginHookToolContext,
): Promise<void> {
  if (type === "before_tool_call" && event.toolName === "observe_demo_echo") {
    // 插件内的演示技能通过这个 tool 进入，命中后立即激活当前会话的观测。
    activateSessionCapture(context.sessionKey);
  }
  if (!isSessionCaptureActive(context.sessionKey)) {
    return;
  }
  const cfg = api.runtime.config.loadConfig();
  if (!readObservabilityLabConfig(cfg).captureEnabled) {
    return;
  }
  enqueueTelemetryEvent({
    stateDir: api.runtime.state.resolveStateDir(),
    record: {
      type,
      at: new Date().toISOString(),
      event: { ...event },
      context: { ...context },
    },
  });
}

function handleBeforeMessageWrite(
  api: OpenClawPluginApi,
  event: PluginHookBeforeMessageWriteEvent,
  context: { agentId?: string; sessionKey?: string },
): PluginHookBeforeMessageWriteResult {
  const cfg = api.runtime.config.loadConfig();
  const settings = readObservabilityLabConfig(cfg);
  const sessionKey = context.sessionKey;
  const messageText = getMessageText(event.message);

  if (messageText.includes(OBSERVABILITY_LAB_MESSAGE_MARKER)) {
    // 插件命令或技能响应带有固定标记，看到它就说明当前 sessionKey 已经和插件交互过。
    activateSessionCapture(sessionKey);
  }

  const active = isSessionCaptureActive(sessionKey);
  if (settings.captureEnabled && active) {
    enqueueTelemetryEvent({
      stateDir: api.runtime.state.resolveStateDir(),
      record: {
        type: "before_message_write",
        at: new Date().toISOString(),
        event: { message: event.message as Record<string, unknown> },
        context: { ...context },
      },
    });
  }

  if (!settings.rewriteEnabled || !active) {
    return {};
  }
  // 这个 hook 必须保持同步；这里最多只做轻量判断和入队，真正刷盘留给异步路径。
  const message = prefixAssistantMessage(event.message, settings.transcriptPrefix);
  return message ? { message } : {};
}

export function registerObservabilityHooks(api: OpenClawPluginApi): void {
  // 按运行时链路顺序注册，方便把这个插件当脚手架时直接照着扩展：
  // 会话开始 -> 入站消息 -> 模型 -> 工具 -> transcript -> 会话结束。
  api.on("session_start", async (event, context) => {
    await maybeRecordSessionEvent(api, "session_start", event, context);
  });

  api.on("message_received", async (event, context) => {
    await maybeRecordMessageEvent(api, "message_received", event, context);
  });

  api.on("llm_input", async (event, context) => {
    await maybeRecordAgentEvent(api, "llm_input", event, context);
  });

  api.on("llm_output", async (event, context) => {
    await maybeRecordAgentEvent(api, "llm_output", event, context);
  });

  api.on("before_tool_call", async (event, context) => {
    await maybeRecordToolEvent(api, "before_tool_call", event, context);
  });

  api.on("after_tool_call", async (event, context) => {
    await maybeRecordToolEvent(api, "after_tool_call", event, context);
  });

  api.on("before_message_write", (event, context) => {
    return handleBeforeMessageWrite(api, event, context);
  });

  api.on("session_end", async (event, context) => {
    await maybeRecordSessionEvent(api, "session_end", event, context);
  });
}
