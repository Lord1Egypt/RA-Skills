/**
 * 把 UnifiedInboundEvent 派发到 OpenClaw 的 agent，并把 agent 回复通过回调发送回用户。
 *
 * 模式：
 *  - async：立即 200 success 回应 webhook，后台跑 agent，通过客服消息（48h 窗口）回发。
 *  - passive：在 5 秒内如果 agent 已经产出 text，则打包成被动回复 XML 写入响应；
 *    否则 fallback 到 async 模式。
 */

import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";

import { accessTokenHandleFor } from "../access-token.js";
import { sendCustomerServiceMessage } from "../api/customer-service.js";
import { getAccountRuntime, updateAccountRuntime } from "../app/index.js";
import {
  ensureDynamicAgentListed,
  generateAgentId,
  shouldUseDynamicAgent,
} from "../dynamic-agent.js";
import { dualWriteInboundTranscript } from "../knowledge/index.js";
import { injectGuardToEnvelope, resolveAgentInstructions } from "../shared/guard.js";
import {
  renderMarkdownForWechatText,
  truncateForWechatText,
} from "../shared/markdown-to-wechat.js";
import type {
  ResolvedWechatServiceAccount,
  WechatServicePassiveReply,
  WechatServiceUnifiedInboundEvent,
} from "../types.js";
import { resolveEventRoutingAgentId } from "../transport/webhook/normalize.js";

export type PassivePromise = Promise<WechatServicePassiveReply | undefined>;

/**
 * **dispatchInboundEvent**
 *
 * 主入口：
 * 1. 解析事件，决定路由 agent
 * 2. prepareInboundSession + dispatchReplyWithBufferedBlockDispatcher
 * 3. 把 delivered text/media 通过客服消息 API 下发给用户
 */
export async function dispatchInboundEvent(params: {
  core: PluginRuntime;
  cfg: OpenClawConfig;
  account: ResolvedWechatServiceAccount;
  event: WechatServiceUnifiedInboundEvent;
}): Promise<void> {
  const { core, cfg, account, event } = params;
  const tokenHandle = accessTokenHandleFor(account);
  const routing = account.routing;
  const routedAgent =
    resolveEventRoutingAgentId({
      inbound: event.raw,
      routing,
    }) ?? routing.defaultAgent;

  const route = core.channel.routing.resolveAgentRoute({
    cfg,
    channel: "wechat-service",
    accountId: event.accountId,
    peer: {
      kind: event.conversation.peerKind,
      id: event.conversation.peerId,
    },
    ...(routedAgent ? { preferredAgentId: routedAgent } : {}),
  });

  // 动态 Agent 覆盖：当 channels["wechat-service"].dynamicAgents.enabled 为 true 时，
  // 每个 openid 派生一个独立 agent。与 @huo15/wecom 的 dynamic-agent 同构；
  // 公众号是 1:1 私聊（peerKind 永远是 "direct"），所以 chatType 永远是 "dm"。
  // 管理员 openid 在 adminUsers 列表里时不走动态路由（继续用上面解析出来的静态 agent）。
  const chatType: "dm" | "group" =
    event.conversation.peerKind === "direct" ? "dm" : "group";
  const useDynamicAgent = shouldUseDynamicAgent({
    chatType,
    senderId: event.conversation.senderId,
    config: cfg,
  });
  if (useDynamicAgent) {
    const targetAgentId = generateAgentId(
      chatType,
      event.conversation.peerId,
      event.accountId,
    );
    route.agentId = targetAgentId;
    route.sessionKey = `agent:${targetAgentId}:wechat-service:${event.accountId}:${chatType}:${event.conversation.peerId}`;

    // 解析角色护栏 instructions（role-based 模式下返回护栏 prompt，否则返回 undefined）
    const instructions = resolveAgentInstructions({
      openid: event.conversation.peerId,
      accountId: event.accountId,
      cfg,
      accountName: account.name,
    });
    // fire-and-forget：把 agent id（及 instructions）写入 agents.list
    ensureDynamicAgentListed(targetAgentId, core, instructions).catch(() => {});
  }

  const storePath = core.channel.session.resolveStorePath(cfg.session?.store, {
    agentId: route.agentId,
  });
  const previousTimestamp = core.channel.session.readSessionUpdatedAt({
    storePath,
    sessionKey: route.sessionKey,
  });
  const envelopeOptions = core.channel.reply.resolveEnvelopeFormatOptions(cfg);

  // role-based 模式下，将角色护栏注入消息信封
  const guardedBody = injectGuardToEnvelope({
    body: event.text,
    openid: event.conversation.peerId,
    cfg,
    accountName: account.name,
  });

  const body = core.channel.reply.formatAgentEnvelope({
    channel: "WeChat-Service",
    from: `direct:${event.conversation.peerId}`,
    previousTimestamp,
    envelope: envelopeOptions,
    body: guardedBody,
  });

  const ctx = core.channel.reply.finalizeInboundContext({
    Body: body,
    RawBody: event.text,
    CommandBody: event.text,
    From: `wechat-service:user:${event.conversation.senderId}`,
    To: `wechat-service:user:${event.conversation.peerId}`,
    SessionKey: route.sessionKey,
    AccountId: route.accountId ?? event.accountId,
    ChatType: "direct",
    ConversationLabel: `direct:${event.conversation.peerId}`,
    SenderName: event.senderName ?? event.conversation.senderId,
    SenderId: event.conversation.senderId,
    Provider: "wechat-service",
    OriginatingChannel: "wechat-service",
    OriginatingTo: `wechat-service:user:${event.conversation.peerId}`,
    MessageSid: event.messageId,
    CommandAuthorized: true,
  });

  await core.channel.session.recordInboundSession({
    storePath,
    sessionKey: ctx.SessionKey ?? route.sessionKey,
    ctx,
    onRecordError: () => {},
  });

  updateAccountRuntime(event.accountId, {
    lastInboundAt: Date.now(),
  });
  getAccountRuntime(event.accountId)?.log.info?.(
    `[wechat-service] inbound dispatch accountId=${event.accountId} agent=${route.agentId ?? "default"} from=${event.conversation.peerId} type=${event.raw.msgType}${event.raw.event ? `/${event.raw.event}` : ""}`,
  );

  const deliveredChunks: string[] = [];
  let agentError: unknown;
  try {
    await core.channel.reply.dispatchReplyWithBufferedBlockDispatcher({
      ctx,
      cfg,
      replyOptions: { disableBlockStreaming: true },
      dispatcherOptions: {
        deliver: async (payload) => {
          const text = typeof payload.text === "string" ? payload.text.trim() : "";
          if (text) deliveredChunks.push(text);
          if (payload.mediaUrl) {
            deliveredChunks.push(`[media] ${payload.mediaUrl}`);
          }
        },
        onError: async (err) => {
          agentError = err;
        },
      },
    });
  } catch (err) {
    agentError = err;
  }

  const replyText = deliveredChunks.join("\n\n").trim();
  if (replyText) {
    // LLM 输出常带 markdown，公众号 text 不渲染 markdown，
    // 先转 markdown → 微信 text，再做**字节级**截断（v2.3.5+ 修订）。
    // 微信限制是 UTF-8 2048 字节（errcode 45002），不是字符；中文 1 字 = 3 字节，
    // 之前按 2000 字符截断的版本会被 45002 拒掉客服消息（粉丝只收 placeholder
    // 不收真回复）。这里默认 1900 字节留 ~150 字节安全余量。
    const renderedReply = truncateForWechatText(
      renderMarkdownForWechatText(replyText),
    );
    try {
      await sendCustomerServiceMessage({
        account,
        tokenHandle,
        message: {
          touser: event.conversation.peerId,
          msgtype: "text",
          text: { content: renderedReply },
        },
      });
      updateAccountRuntime(event.accountId, { lastOutboundAt: Date.now() });
    } catch (err) {
      getAccountRuntime(event.accountId)?.log.error?.(
        `[wechat-service] customer_service_send failed accountId=${event.accountId}: ${err instanceof Error ? err.message : String(err)}`,
      );
      updateAccountRuntime(event.accountId, {
        lastError: err instanceof Error ? err.message : String(err),
      });
    }
  }

  if (agentError) {
    getAccountRuntime(event.accountId)?.log.error?.(
      `[wechat-service] agent_dispatch_error accountId=${event.accountId}: ${
        agentError instanceof Error ? agentError.message : String(agentError)
      }`,
    );
    updateAccountRuntime(event.accountId, {
      lastError: agentError instanceof Error ? agentError.message : String(agentError),
    });
  }

  if (account.knowledgeSync?.enabled) {
    void dualWriteInboundTranscript({
      account,
      event,
      replyText,
    }).catch((err) => {
      getAccountRuntime(event.accountId)?.log.warn?.(
        `[wechat-service] knowledge_sync_failed accountId=${event.accountId}: ${err instanceof Error ? err.message : String(err)}`,
      );
    });
  }
}
