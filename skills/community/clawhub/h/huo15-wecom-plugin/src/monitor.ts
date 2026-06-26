import type { IncomingMessage, ServerResponse } from "node:http";

import { getWecomRuntime } from "./runtime.js";
import { handleWecomHttpRequest } from "./transport/http/request-handler.js";
import {
  registerAgentWebhookTarget,
  registerKefuWebhookTarget,
  registerWecomWebhookTarget,
} from "./transport/http/registry.js";
import { sendActiveMessage } from "./transport/bot-webhook/active-reply.js";
import { createBotWebhookRequestHandler } from "./transport/bot-webhook/request-handler.js";
import {
  shouldProcessBotInboundMessage,
  type BotInboundProcessDecision,
} from "./transport/bot-webhook/message-shape.js";

/**
 * Legacy compatibility bridge for the old monitor entrypoints.
 *
 * Bot webhook parsing and stream orchestration now live in
 * `transport/bot-webhook/*` and `capability/bot/*`.
 */

import type {
  WecomRuntimeAuditEvent,
  WecomWebhookTarget,
} from "./types/runtime-context.js";
import { monitorState } from "./monitor/state.js";
import { createBotStreamOrchestrator } from "./capability/bot/stream-orchestrator.js";

const streamStore = monitorState.streamStore;

function recordWebhookOperationalEvent(
  target:
    | Pick<WecomWebhookTarget, "account" | "auditSink">
    | { agent: { accountId: string }; auditSink?: (event: WecomRuntimeAuditEvent) => void },
  event: WecomRuntimeAuditEvent,
): void {
  const accountId = "account" in target ? target.account.accountId : target.agent.accountId;
  monitorState.operationalEvents.append({
    accountId,
    transport: event.transport,
    category: event.category,
    summary: event.summary,
    messageId: event.messageId,
  });
  target.auditSink?.(event);
}

function recordBotOperationalEvent(
  target: Pick<WecomWebhookTarget, "account" | "auditSink">,
  event: Omit<WecomRuntimeAuditEvent, "transport">,
): void {
  recordWebhookOperationalEvent(target, {
    transport: "bot-webhook",
    ...event,
  });
}

function logVerbose(target: WecomWebhookTarget, message: string): void {
  const should =
    target.core.logging?.shouldLogVerbose?.() ??
    (() => {
      try {
        return getWecomRuntime().logging.shouldLogVerbose();
      } catch {
        return false;
      }
    })();
  if (!should) return;
  target.runtime.log?.(`[wecom] ${message}`);
}

function logInfo(target: WecomWebhookTarget, message: string): void {
  target.runtime.log?.(`[wecom] ${message}`);
}

const botStreamOrchestrator = createBotStreamOrchestrator({
  streamStore,
  recordBotOperationalEvent,
});

const { flushPending, startAgentForStream } = botStreamOrchestrator;

monitorState.streamStore.setFlushHandler((pending) => void flushPending(pending));

const handleBotWebhookRequest = createBotWebhookRequestHandler({
  streamStore,
  logInfo,
  logVerbose,
  recordBotOperationalEvent,
  startAgentForStream,
});

export { registerAgentWebhookTarget, registerKefuWebhookTarget, registerWecomWebhookTarget };
export { sendActiveMessage, shouldProcessBotInboundMessage };
export type { BotInboundProcessDecision };

/**
 * **handleWecomWebhookRequest (HTTP 请求入口)**
 * 
 * 处理来自企业微信的所有 Webhook 请求。
 * 职责：
 * 1. 路由分发：优先按 `/plugins/wecom/{bot|agent}/{accountId}` 分流，并兼容历史 `/wecom/*` 路径。
 * 2. 安全校验：验证企业微信签名 (Signature)。
 * 3. 消息解密：处理企业微信的加密包。
 * 4. 响应处理：
 *    - GET 请求：处理 EchoStr 验证。
 *    - POST 请求：接收消息，放入 StreamStore，返回流式 First Chunk。
 */
export async function handleWecomWebhookRequest(req: IncomingMessage, res: ServerResponse): Promise<boolean> {
  return handleWecomHttpRequest({
    req,
    res,
    handleBotWebhookRequest,
  });
}

export async function handleLegacyWecomWebhookRequest(req: IncomingMessage, res: ServerResponse): Promise<boolean> {
  return handleWecomHttpRequest({
    req,
    res,
    handleBotWebhookRequest,
  });
}
