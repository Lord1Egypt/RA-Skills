import { pathToFileURL } from "node:url";

import type { PluginRuntime } from "openclaw/plugin-sdk";

import { resolveWecomMediaMaxBytes, shouldRejectWecomDefaultRoute } from "../../config/index.js";
import { ensureDynamicAgentListed, generateAgentId, shouldUseDynamicAgent } from "../../dynamic-agent.js";
import { LIMITS, type StreamStore } from "../../monitor/state.js";
import { getWecomRuntime } from "../../runtime.js";
import { buildWecomUnauthorizedCommandPrompt, resolveWecomCommandAuthorization } from "../../shared/command-auth.js";
import type { PendingInbound } from "../../types/legacy-stream.js";
import type { WecomBotInboundMessage as WecomInboundMessage } from "../../types/index.js";
import type { WecomWebhookTarget } from "../../types/runtime-context.js";
import { looksLikeSendLocalFileIntent, processBotInboundMessage } from "../../transport/bot-webhook/inbound-normalizer.js";
import { resolveWecomSenderUserId } from "../../transport/bot-webhook/message-shape.js";
import { buildWecomBotDispatchConfig } from "./dispatch-config.js";
import { buildFallbackPrompt, resolveAgentAccountOrUndefined, sendBotFallbackPromptNow } from "./fallback-delivery.js";
import { finalizeBotStream } from "./stream-finalizer.js";
import { handleDirectLocalPathIntent } from "./local-path-delivery.js";
import { stageWecomInboundMediaForSession } from "./sandbox-media.js";
import { createBotReplyDispatcher } from "./stream-delivery.js";
import type { BotRuntimeLogger, RecordBotOperationalEvent } from "./types.js";

export type StartBotAgentStreamParams = {
  target: WecomWebhookTarget;
  accountId: string;
  msg: WecomInboundMessage;
  streamId: string;
  mergedContents?: string[] | string;
  mergedMsgids?: string[];
};

export function createBotStreamOrchestrator(params: {
  streamStore: StreamStore;
  recordBotOperationalEvent: RecordBotOperationalEvent;
}) {
  const { streamStore, recordBotOperationalEvent } = params;

  const logVerbose: BotRuntimeLogger = (target, message) => {
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
  };

  const logInfo: BotRuntimeLogger = (target, message) => {
    target.runtime.log?.(`[wecom] ${message}`);
  };

  const truncateUtf8Bytes = (text: string, maxBytes: number): string => {
    const buf = Buffer.from(text, "utf8");
    if (buf.length <= maxBytes) return text;
    return buf.subarray(buf.length - maxBytes).toString("utf8");
  };

  const computeTaskKey = (target: WecomWebhookTarget, msg: WecomInboundMessage): string | undefined => {
    const msgid = msg.msgid ? String(msg.msgid) : "";
    if (!msgid) return undefined;
    const aibotid = String((msg as any).aibotid ?? "unknown").trim() || "unknown";
    return `bot:${target.account.accountId}:${aibotid}:${msgid}`;
  };

  async function flushPending(pending: PendingInbound): Promise<void> {
    const { streamId, target, msg, contents, msgids, conversationKey, batchKey } = pending;
    const mergedContents = contents.filter((c) => c.trim()).join("\n").trim();

    let core: PluginRuntime | null = null;
    try {
      core = getWecomRuntime();
    } catch (err) {
      logVerbose(target, `flush pending: runtime not ready: ${String(err)}`);
      streamStore.markFinished(streamId);
      logInfo(target, `queue: runtime not ready，结束批次并推进 streamId=${streamId}`);
      streamStore.onStreamFinished(streamId);
      return;
    }

    if (!core) return;

    streamStore.markStarted(streamId);
    const enrichedTarget: WecomWebhookTarget = { ...target, core };
    logInfo(
      target,
      `flush pending: start batch streamId=${streamId} batchKey=${batchKey} conversationKey=${conversationKey} mergedCount=${contents.length}`,
    );
    logVerbose(target, `防抖结束: 开始处理聚合消息 数量=${contents.length} streamId=${streamId}`);

    startAgentForStream({
      target: enrichedTarget,
      accountId: target.account.accountId,
      msg,
      streamId,
      mergedContents: contents.length > 1 ? mergedContents : undefined,
      mergedMsgids: msgids.length > 1 ? msgids : undefined,
    }).catch((err) => {
      streamStore.updateStream(streamId, (state) => {
        state.error = err instanceof Error ? err.message : String(err);
        state.content = state.content || `Error: ${state.error}`;
        state.finished = true;
      });
      target.runtime.error?.(`[${target.account.accountId}] wecom agent failed (处理失败): ${String(err)}`);
      streamStore.onStreamFinished(streamId);
    });
  }

  async function startAgentForStream(params: StartBotAgentStreamParams): Promise<void> {
    const { target, msg, streamId } = params;
    const core = target.core;
    const config = target.config;
    const account = target.account;

    const userId = resolveWecomSenderUserId(msg) || "unknown";
    const chatType = msg.chattype === "group" ? "group" : "direct";
    const chatId = msg.chattype === "group" ? (msg.chatid?.trim() || "unknown") : userId;
    const taskKey = computeTaskKey(target, msg);
    const aibotid = String((msg as any).aibotid ?? "").trim() || undefined;

    streamStore.updateStream(streamId, (s) => {
      s.userId = userId;
      s.chatType = chatType;
      s.chatId = chatId;
      s.taskKey = taskKey;
      s.aibotid = aibotid;
    });

    let { body: rawBody, media } = await processBotInboundMessage({
      target,
      msg,
      recordOperationalIssue: (event) => recordBotOperationalEvent(target, event),
    });

    if (params.mergedContents) {
      rawBody = Array.isArray(params.mergedContents) ? params.mergedContents.join("\n") : params.mergedContents;
    }

    const handledLocalPath = await handleDirectLocalPathIntent({
      streamStore,
      target,
      streamId,
      rawBody,
      userId,
      chatType,
      logVerbose,
      looksLikeSendLocalFileIntent,
    });
    if (handledLocalPath) return;

    let mediaPath: string | undefined;
    let mediaType: string | undefined;
    const mediaFilename = media?.filename;
    if (media) {
      try {
        const maxBytes = resolveWecomMediaMaxBytes(target.config, target.account.accountId);
        const saved = await core.channel.media.saveMediaBuffer(media.buffer, media.contentType, "inbound", maxBytes, media.filename);
        mediaPath = saved.path;
        mediaType = saved.contentType;
        logVerbose(target, `saved inbound media to ${mediaPath} (${mediaType})`);
      } catch (err) {
        target.runtime.error?.(`Failed to save inbound media: ${String(err)}`);
      }
    }

    const route = core.channel.routing.resolveAgentRoute({
      cfg: config,
      channel: "wecom",
      accountId: account.accountId,
      peer: { kind: chatType === "group" ? "group" : "direct", id: chatId },
    });

    const useDynamicAgent = shouldUseDynamicAgent({
      chatType: chatType === "group" ? "group" : "dm",
      senderId: userId,
      config,
    });

    if (shouldRejectWecomDefaultRoute({ cfg: config, matchedBy: route.matchedBy, useDynamicAgent })) {
      const prompt =
        `当前账号（${account.accountId}）未绑定 OpenClaw Agent，已拒绝回退到默认主智能体。` +
        `请在 bindings 中添加：{"agentId":"你的Agent","match":{"channel":"wecom","accountId":"${account.accountId}"}}`;
      target.runtime.error?.(
        `[wecom] routing guard: blocked default fallback accountId=${account.accountId} matchedBy=${route.matchedBy} streamId=${streamId}`,
      );
      streamStore.updateStream(streamId, (s) => {
        s.finished = true;
        s.content = prompt;
      });
      try {
        await sendBotFallbackPromptNow({ streamId, text: prompt });
      } catch (err) {
        target.runtime.error?.(`routing guard prompt push failed streamId=${streamId}: ${String(err)}`);
      }
      streamStore.onStreamFinished(streamId);
      return;
    }

    if (useDynamicAgent) {
      const dmOrGroup: "dm" | "group" = chatType === "group" ? "group" : "dm";
      const targetAgentId = generateAgentId(dmOrGroup, chatId, account.accountId);
      route.agentId = targetAgentId;
      route.sessionKey = `agent:${targetAgentId}:wecom:${account.accountId}:${dmOrGroup}:${chatId}`;
      ensureDynamicAgentListed({
        agentId: targetAgentId,
        chatType: dmOrGroup,
        peerId: chatId,
        accountId: account.accountId,
        runtime: core,
      }).catch(() => { });
      logVerbose(target, `dynamic agent routing: ${targetAgentId}, sessionKey=${route.sessionKey}`);
    }

    if (mediaPath) {
      try {
        const stagedSessionPath = await stageWecomInboundMediaForSession({
          cfg: target.config,
          accountId: target.account.accountId,
          agentId: route.agentId,
          sessionKey: route.sessionKey,
          mediaPath,
          filename: mediaFilename,
        });
        mediaPath = stagedSessionPath;
        logVerbose(target, `session media staged to ${mediaPath}`);
      } catch (err) {
        target.runtime.error?.(`Failed to stage inbound media for session workspace: ${String(err)}`);
      }
    }

    logVerbose(target, `starting agent processing (streamId=${streamId}, agentId=${route.agentId}, peerKind=${chatType}, peerId=${chatId})`);
    logVerbose(target, `启动 Agent 处理: streamId=${streamId} 路由=${route.agentId} 类型=${chatType} ID=${chatId}`);

    const fromLabel = chatType === "group" ? `group:${chatId}` : `user:${userId}`;
    const storePath = core.channel.session.resolveStorePath(config.session?.store, { agentId: route.agentId });
    const envelopeOptions = core.channel.reply.resolveEnvelopeFormatOptions(config);
    const previousTimestamp = core.channel.session.readSessionUpdatedAt({
      storePath,
      sessionKey: route.sessionKey,
    });
    const body = core.channel.reply.formatAgentEnvelope({
      channel: "WeCom",
      from: fromLabel,
      previousTimestamp,
      envelope: envelopeOptions,
      body: rawBody,
    });

    const authz = await resolveWecomCommandAuthorization({
      core,
      cfg: config,
      accountConfig: account.config,
      rawBody,
      senderUserId: userId,
    });
    const commandAuthorized = authz.commandAuthorized;
    logVerbose(
      target,
      `authz: dmPolicy=${authz.dmPolicy} shouldCompute=${authz.shouldComputeAuth} sender=${userId.toLowerCase()} senderAllowed=${authz.senderAllowed} authorizerConfigured=${authz.authorizerConfigured} commandAuthorized=${String(authz.commandAuthorized)}`,
    );

    if (authz.shouldComputeAuth && authz.commandAuthorized !== true) {
      const prompt = buildWecomUnauthorizedCommandPrompt({ senderUserId: userId, dmPolicy: authz.dmPolicy, scope: "bot" });
      streamStore.updateStream(streamId, (s) => {
        s.finished = true;
        s.content = prompt;
      });
      try {
        await sendBotFallbackPromptNow({ streamId, text: prompt });
        logInfo(target, `authz: 未授权命令已提示用户 streamId=${streamId}`);
      } catch (err) {
        target.runtime.error?.(`authz: 未授权命令提示推送失败 streamId=${streamId}: ${String(err)}`);
      }
      streamStore.onStreamFinished(streamId);
      return;
    }

    const attachments = mediaPath
      ? [
        {
          name: media?.filename || "file",
          mimeType: mediaType,
          url: pathToFileURL(mediaPath).href,
        },
      ]
      : undefined;

    const ctxPayload = core.channel.reply.finalizeInboundContext({
      Body: body,
      RawBody: rawBody,
      CommandBody: rawBody,
      Attachments: attachments,
      From: chatType === "group" ? `wecom:group:${chatId}` : `wecom:user:${userId}`,
      To: chatType === "group" ? `wecom:group:${chatId}` : `wecom:user:${chatId}`,
      SessionKey: route.sessionKey,
      AccountId: route.accountId,
      ChatType: chatType,
      ConversationLabel: fromLabel,
      SenderName: userId,
      SenderId: userId,
      Provider: "wecom",
      Surface: "wecom",
      MessageSid: msg.msgid,
      CommandAuthorized: commandAuthorized,
      OriginatingChannel: "wecom",
      OriginatingTo: chatType === "group" ? `wecom:group:${chatId}` : `wecom:user:${chatId}`,
      MediaPath: mediaPath,
      MediaType: mediaType,
      MediaUrl: mediaPath,
    });

    await core.channel.session.recordInboundSession({
      storePath,
      sessionKey: ctxPayload.SessionKey ?? route.sessionKey,
      ctx: ctxPayload,
      onRecordError: (err) => {
        target.runtime.error?.(`wecom: failed updating session meta: ${String(err)}`);
      },
    });

    const tableMode = core.channel.text.resolveMarkdownTableMode({
      cfg: config,
      channel: "wecom",
      accountId: account.accountId,
    });
    const cfgForDispatch = buildWecomBotDispatchConfig(config);
    logVerbose(target, "tool-policy: WeCom Bot 会话已禁用 message 工具（tools.deny += message；并同步到 tools.sandbox.tools.deny，防止绕过 Bot 交付）");

    // 主动 fallback timer：长任务期间 deliver 可能完全沉默（dispatcher 没机会触发 nearTimeout），
    // 4 分钟时强制切到 fallback("timeout") 并推 prompt，让用户在 response_url 过期前看到提示。
    // 与 stream-delivery.ts 的 BOT_WINDOW_MS(4.5min) - BOT_SWITCH_MARGIN_MS(30s) 对齐。
    const PROACTIVE_FALLBACK_DELAY_MS = 4 * 60 * 1000;
    let proactiveFallbackTimer: NodeJS.Timeout | null = setTimeout(() => {
      proactiveFallbackTimer = null;
      void (async () => {
        const current = streamStore.getStream(streamId);
        if (!current || current.finished || current.fallbackMode) return;
        const agentCfg = resolveAgentAccountOrUndefined(config, account.accountId);
        const prompt = buildFallbackPrompt({
          kind: "timeout",
          agentConfigured: Boolean(agentCfg),
          userId: current.userId,
          chatType: current.chatType,
        });
        streamStore.updateStream(streamId, (s) => {
          s.fallbackMode = "timeout";
          s.fallbackPromptSentAt = s.fallbackPromptSentAt ?? Date.now();
        });
        try {
          await sendBotFallbackPromptNow({ streamId, text: prompt });
          logVerbose(
            target,
            `proactive fallback(timeout): 主动推送 prompt streamId=${streamId} agentConfigured=${Boolean(agentCfg)}`,
          );
        } catch (err) {
          target.runtime.error?.(`proactive fallback prompt push failed streamId=${streamId}: ${String(err)}`);
          recordBotOperationalEvent(target, {
            category: "fallback-delivery-failed",
            summary: `proactive fallback prompt push failed streamId=${streamId}`,
            error: err instanceof Error ? err.message : String(err),
          });
        }
      })();
    }, PROACTIVE_FALLBACK_DELAY_MS);

    try {
      await core.channel.reply.dispatchReplyWithBufferedBlockDispatcher({
        ctx: ctxPayload,
        cfg: cfgForDispatch,
        replyOptions: { disableBlockStreaming: false },
        dispatcherOptions: createBotReplyDispatcher({
          streamStore,
          target,
          accountId: account.accountId,
          config,
          msg,
          streamId,
          rawBody,
          chatType,
          userId,
          core,
          tableMode,
          logVerbose,
          truncateUtf8Bytes,
          recordBotOperationalEvent,
        }),
      });

      const rawBodyNormalized = rawBody.trim();
      const isResetCommand = /^\/(new|reset)(?:\s|$)/i.test(rawBodyNormalized);
      const resetCommandKind = isResetCommand ? (rawBodyNormalized.match(/^\/(new|reset)/i)?.[1]?.toLowerCase() ?? "new") : null;

      await finalizeBotStream({
        streamStore,
        target,
        streamId,
        chatType,
        core,
        config,
        accountId: account.accountId,
        isResetCommand,
        resetCommandKind,
        logInfo,
        logVerbose,
        recordBotOperationalEvent,
      });
    } finally {
      if (proactiveFallbackTimer) {
        clearTimeout(proactiveFallbackTimer);
        proactiveFallbackTimer = null;
      }
    }
  }

  return {
    flushPending,
    startAgentForStream,
  };
}
