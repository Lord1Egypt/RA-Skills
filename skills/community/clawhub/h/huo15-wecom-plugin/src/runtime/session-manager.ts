import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";
import type { WecomMediaService } from "../shared/media-service.js";
import type { UnifiedInboundEvent } from "../types/index.js";
import { getPeerContextToken } from "../context-store.js";
import { buildWecomContextTarget, buildWecomKefuTarget } from "../target.js";
import { resolveRuntimeRoute } from "./routing-bridge.js";
import { registerWecomSourceSnapshot } from "./source-registry.js";

function extractKefuOpenKfId(event: UnifiedInboundEvent): string | undefined {
  if (event.transport !== "kefu") return undefined;
  const body = event.raw?.body;
  if (!body || typeof body !== "object") return undefined;
  const rec = body as Record<string, unknown>;
  const candidates = [rec.open_kfid, rec.openKfId];
  for (const candidate of candidates) {
    if (typeof candidate === "string" && candidate.trim()) return candidate.trim();
  }
  const eventObj = rec.event;
  if (eventObj && typeof eventObj === "object") {
    const eventRec = eventObj as Record<string, unknown>;
    const nested = eventRec.open_kfid;
    if (typeof nested === "string" && nested.trim()) return nested.trim();
  }
  return undefined;
}

export type PreparedSession = {
  route: ReturnType<typeof resolveRuntimeRoute>;
  ctx: ReturnType<PluginRuntime["channel"]["reply"]["finalizeInboundContext"]>;
  storePath: string;
};

function readContextSessionId(ctx: { SessionId?: string } | Record<string, unknown>): string | undefined {
  const sessionId = "SessionId" in ctx ? ctx.SessionId : undefined;
  return typeof sessionId === "string" && sessionId.trim() ? sessionId.trim() : undefined;
}

export async function prepareInboundSession(params: {
  core: PluginRuntime;
  cfg: OpenClawConfig;
  event: UnifiedInboundEvent;
  mediaService: WecomMediaService;
}): Promise<PreparedSession> {
  const { core, cfg, event, mediaService } = params;
  const route = resolveRuntimeRoute({ core, cfg, event });
  const source =
    event.transport === "bot-ws"
      ? "bot-ws"
      : event.transport === "agent-callback"
        ? "agent-callback"
        : event.transport === "kefu"
          ? "kefu"
          : undefined;
  const kefuOpenKfId = extractKefuOpenKfId(event);
  if (source) {
    registerWecomSourceSnapshot({
      accountId: event.accountId,
      source,
      messageId: event.messageId,
      sessionKey: route.sessionKey,
      peerKind: event.conversation.peerKind,
      peerId: event.conversation.peerId,
      kefuOpenKfId,
    });
  }
  const storePath = core.channel.session.resolveStorePath(cfg.session?.store, {
    agentId: route.agentId,
  });
  const previousTimestamp = core.channel.session.readSessionUpdatedAt({
    storePath,
    sessionKey: route.sessionKey,
  });
  const envelopeOptions = core.channel.reply.resolveEnvelopeFormatOptions(cfg);
  const body = core.channel.reply.formatAgentEnvelope({
    channel: "WeCom",
    from: `${event.conversation.peerKind}:${event.conversation.peerId}`,
    previousTimestamp,
    envelope: envelopeOptions,
    body: event.text,
  });

  const totalAttachments = event.attachments?.length ?? 0;
  // v2.8.8 ⭐ 一条 inbound 只能填一个 ctx.MediaPath，但 mixed/quote 类型可能携带多张图片。
  // 单图走老路径；多图时一次性下载全部并把首张挂到 MediaPath，其余仅落盘 + 记日志。
  let mediaPath: string | undefined;
  let mediaContentType: string | undefined;
  if (totalAttachments <= 1) {
    const firstAttachment = await mediaService.normalizeFirstAttachment(event);
    if (firstAttachment) {
      mediaPath = await mediaService.saveInboundAttachment(event, firstAttachment);
      mediaContentType = firstAttachment.contentType;
    }
  } else {
    const all = await mediaService.normalizeAllAttachments(event);
    if (all.length > 0) {
      mediaPath = await mediaService.saveInboundAttachment(event, all[0]);
      mediaContentType = all[0].contentType;
      const tailPaths: string[] = [];
      for (let i = 1; i < all.length; i += 1) {
        try {
          tailPaths.push(await mediaService.saveInboundAttachment(event, all[i]));
        } catch (err) {
          console.warn(
            `[wecom-session] tail attachment#${i} save failed: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      }
      console.info(
        `[wecom-session] inbound has ${totalAttachments} attachments accountId=${event.accountId} transport=${event.transport} messageId=${event.messageId}; ctx.MediaPath=${mediaPath}; tail=${tailPaths.length > 0 ? tailPaths.join("|") : "none"}`,
      );
    }
  }
  const defaultOriginatingTo =
    event.conversation.peerKind === "group"
      ? `wecom:group:${event.conversation.peerId}`
      : `wecom:user:${event.conversation.peerId}`;
  const contextToken =
    event.transport === "bot-ws"
      ? getPeerContextToken(event.accountId, event.conversation.peerId)
      : undefined;
  const kefuOriginatingTo =
    event.transport === "kefu" && kefuOpenKfId
      ? buildWecomKefuTarget({
          accountId: event.accountId,
          openKfId: kefuOpenKfId,
          externalUserId: event.conversation.peerId,
        })
      : undefined;
  const originatingTo =
    kefuOriginatingTo ??
    (contextToken ? buildWecomContextTarget(contextToken) : defaultOriginatingTo);
  const providerContext =
    event.transport === "bot-ws"
      ? {
          // Bot WS inbound turns already have a live reply handle bound to the
          // current req_id. Mark the current surface as WeCom so core final text
          // stays on that handle and replaces the placeholder instead of being
          // re-routed as a second active-push message.
          Provider: "wecom" as const,
          Surface: "wecom" as const,
        }
      : {
          Provider: "wecom" as const,
        };

  const ctx = core.channel.reply.finalizeInboundContext({
    Body: body,
    RawBody: event.text,
    CommandBody: event.text,
    From:
      event.conversation.peerKind === "group"
        ? `wecom:group:${event.conversation.peerId}`
        : `wecom:user:${event.conversation.senderId}`,
    To:
      event.conversation.peerKind === "group"
        ? `wecom:group:${event.conversation.peerId}`
        : `wecom:user:${event.conversation.peerId}`,
    SessionKey: route.sessionKey,
    AccountId: route.accountId,
    ChatType: event.conversation.peerKind,
    ConversationLabel: `${event.conversation.peerKind}:${event.conversation.peerId}`,
    SenderName: event.senderName ?? event.conversation.senderId,
    SenderId: event.conversation.senderId,
    // Keep Originating* populated so explicit route-to-origin flows and message
    // tools can still resolve the active peer context when needed.
    ...providerContext,
    OriginatingChannel: "wecom",
    OriginatingTo: originatingTo,
    MessageSid: event.messageId,
    CommandAuthorized: true,
    MediaPath: mediaPath,
    MediaUrl: mediaPath,
    MediaType: mediaContentType,
  });

  if (source) {
    registerWecomSourceSnapshot({
      accountId: event.accountId,
      source,
      messageId: event.messageId,
      sessionKey: ctx.SessionKey ?? route.sessionKey,
      sessionId: readContextSessionId(ctx),
      peerKind: event.conversation.peerKind,
      peerId: event.conversation.peerId,
      kefuOpenKfId,
    });
  }

  await core.channel.session.recordInboundSession({
    storePath,
    sessionKey: ctx.SessionKey ?? route.sessionKey,
    ctx,
    onRecordError: () => {},
  });

  return { route, ctx, storePath };
}
