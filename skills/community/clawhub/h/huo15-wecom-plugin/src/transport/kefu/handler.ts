import type { ReplyHandle, ReplyPayload, UnifiedInboundEvent } from "../../types/index.js";
import type { KefuWebhookTarget } from "../http/registry.js";
import type { KefuSyncMessage } from "./api-client.js";
import { syncKefuMessages } from "./api-client.js";
import {
  beginKefuPull,
  endKefuPull,
  readKefuCursor,
  rememberKefuMsgId,
  writeKefuCursor,
} from "./cursor-store.js";
import { normalizeKefuMessage, type KefuNormalizedEvent } from "./normalize.js";
import {
  deliverKefuLink,
  deliverKefuMediaUrl,
  deliverKefuText,
  type KefuDeliveryTarget,
} from "./outbound.js";
import { toKefuText } from "../../wecom_msg_adapter/kefu_text_adapter.js";
import { registerWecomSourceSnapshot } from "../../runtime/source-registry.js";

const MAX_SYNC_ITERATIONS = 5;

export type KefuCallbackEnvelope = {
  token: string;
  openKfId?: string;
  rawXml: string;
  reqId: string;
};

export async function processKefuCallback(params: {
  target: KefuWebhookTarget;
  envelope: KefuCallbackEnvelope;
}): Promise<void> {
  const { target, envelope } = params;
  const { token, openKfId, rawXml, reqId } = envelope;
  if (!token) {
    target.runtimeEnv.error?.(
      `[wecom] inbound(kefu): reqId=${reqId} missing_token accountId=${target.kefu.accountId}`,
    );
    return;
  }
  const pullKey = openKfId || "__no_open_kfid__";
  if (!beginKefuPull(target.kefu.accountId, pullKey)) {
    target.runtimeEnv.log?.(
      `[wecom] inbound(kefu): reqId=${reqId} accountId=${target.kefu.accountId} openKfid=${pullKey} pull_already_inflight`,
    );
    return;
  }
  try {
    await pullKefuMessages({ target, token, openKfId, rawXml, reqId });
  } finally {
    endKefuPull(target.kefu.accountId, pullKey);
  }
}

async function pullKefuMessages(params: {
  target: KefuWebhookTarget;
  token: string;
  openKfId?: string;
  rawXml: string;
  reqId: string;
}): Promise<void> {
  const { target, token, openKfId, rawXml, reqId } = params;
  let cursor = openKfId ? readKefuCursor(target.kefu.accountId, openKfId) : undefined;
  let iterations = 0;
  while (iterations < MAX_SYNC_ITERATIONS) {
    iterations += 1;
    let syncResult;
    try {
      syncResult = await syncKefuMessages({
        kefu: target.kefu,
        token,
        cursor,
        openKfid: openKfId,
      });
    } catch (err) {
      target.runtimeEnv.error?.(
        `[wecom] inbound(kefu): reqId=${reqId} sync_failed accountId=${target.kefu.accountId} cursor=${cursor ?? "<none>"} err=${String(err)}`,
      );
      target.auditSink?.({
        transport: "kefu",
        category: "runtime-error",
        summary: `kefu sync_msg failed: ${String(err)}`,
        raw: { transport: "kefu", envelopeType: "xml", body: { token, openKfId } },
        error: err instanceof Error ? err.message : String(err),
      });
      return;
    }
    target.runtimeEnv.log?.(
      `[wecom] inbound(kefu): reqId=${reqId} accountId=${target.kefu.accountId} iter=${iterations} fetched=${syncResult.msg_list.length} has_more=${syncResult.has_more} next_cursor=${syncResult.next_cursor ?? "<none>"}`,
    );

    for (const msg of syncResult.msg_list) {
      await handleSyncedKefuMessage({ target, msg, rawXml, token, reqId });
    }

    if (syncResult.next_cursor && openKfId) {
      writeKefuCursor(target.kefu.accountId, openKfId, syncResult.next_cursor);
      cursor = syncResult.next_cursor;
    } else if (syncResult.next_cursor) {
      cursor = syncResult.next_cursor;
    }
    if (!syncResult.has_more || !syncResult.next_cursor) {
      break;
    }
  }
}

async function handleSyncedKefuMessage(params: {
  target: KefuWebhookTarget;
  msg: KefuSyncMessage;
  rawXml: string;
  token: string;
  reqId: string;
}): Promise<void> {
  const { target, msg, rawXml, token, reqId } = params;
  const normalized = normalizeKefuMessage({
    accountId: target.kefu.accountId,
    msg,
    rawXml,
    token,
  });
  if (!normalized) {
    target.runtimeEnv.log?.(
      `[wecom] inbound(kefu): reqId=${reqId} accountId=${target.kefu.accountId} skip reason=normalize_failed msgid=${msg.msgid ?? "n/a"}`,
    );
    return;
  }
  const { event, openKfId, externalUserId, rawMsgType, eventType } = normalized;
  if (!rememberKefuMsgId(target.kefu.accountId, event.messageId)) {
    target.auditSink?.({
      transport: "kefu",
      category: "duplicate-inbound",
      summary: `duplicate kefu msgid=${event.messageId} openKfId=${openKfId}`,
      messageId: event.messageId,
      raw: event.raw,
    });
    return;
  }
  target.touchTransportSession?.({ lastInboundAt: Date.now(), running: true });
  target.runtimeEnv.log?.(
    `[wecom] inbound(kefu): reqId=${reqId} accountId=${target.kefu.accountId} dispatch msgid=${event.messageId} openKfId=${openKfId} externalUserId=${externalUserId || "n/a"} msgtype=${rawMsgType} event=${eventType ?? "n/a"}`,
  );
  registerWecomSourceSnapshot({
    accountId: target.kefu.accountId,
    source: "kefu",
    messageId: event.messageId,
    peerKind: "direct",
    peerId: externalUserId || openKfId,
    kefuOpenKfId: openKfId,
  });

  const replyHandle = buildKefuReplyHandle({ target, normalized });
  try {
    await target.runtime.handleEvent(event, replyHandle);
  } catch (err) {
    target.runtimeEnv.error?.(
      `[wecom] inbound(kefu): reqId=${reqId} dispatch_failed msgid=${event.messageId} err=${String(err)}`,
    );
    target.auditSink?.({
      transport: "kefu",
      category: "runtime-error",
      summary: `kefu dispatch failed msgid=${event.messageId}`,
      messageId: event.messageId,
      raw: event.raw,
      error: err instanceof Error ? err.message : String(err),
    });
  }
}

function buildKefuReplyHandle(params: {
  target: KefuWebhookTarget;
  normalized: KefuNormalizedEvent;
}): ReplyHandle {
  const { target, normalized } = params;
  const { event, openKfId, externalUserId } = normalized;
  const deliveryTarget: KefuDeliveryTarget = {
    kefu: target.kefu,
    openKfId,
    externalUserId,
  };
  return {
    context: event.replyContext,
    deliver: async (payload: ReplyPayload) => {
      await runKefuDelivery({ target, deliveryTarget, payload, event });
    },
    fail: async (error) => {
      target.auditSink?.({
        transport: "kefu",
        category: "runtime-error",
        summary: `kefu reply failed msgid=${event.messageId}`,
        messageId: event.messageId,
        raw: event.raw,
        error: error instanceof Error ? error.message : String(error),
      });
    },
  };
}

async function runKefuDelivery(params: {
  target: KefuWebhookTarget;
  deliveryTarget: KefuDeliveryTarget;
  payload: ReplyPayload;
  event: UnifiedInboundEvent;
}): Promise<void> {
  const { target, deliveryTarget, payload, event } = params;
  if (!deliveryTarget.externalUserId) {
    target.runtimeEnv.error?.(
      `[wecom] outbound(kefu): accountId=${target.kefu.accountId} drop reason=missing_external_userid msgid=${event.messageId}`,
    );
    return;
  }
  const text = payload.text ?? "";
  const mediaUrls = payload.mediaUrls && payload.mediaUrls.length > 0
    ? payload.mediaUrls
    : payload.mediaUrl
      ? [payload.mediaUrl]
      : [];

  const channelData = payload.channelData ?? {};
  const kefuLink = extractLinkFromChannelData(channelData);
  if (kefuLink) {
    try {
      await deliverKefuLink(deliveryTarget, kefuLink);
      target.touchTransportSession?.({ lastOutboundAt: Date.now(), running: true });
    } catch (err) {
      target.runtimeEnv.error?.(
        `[wecom] outbound(kefu): link_failed accountId=${target.kefu.accountId} err=${String(err)}`,
      );
    }
    return;
  }

  for (const mediaUrl of mediaUrls) {
    try {
      await deliverKefuMediaUrl(deliveryTarget, mediaUrl);
      target.touchTransportSession?.({ lastOutboundAt: Date.now(), running: true });
    } catch (err) {
      target.runtimeEnv.error?.(
        `[wecom] outbound(kefu): media_failed accountId=${target.kefu.accountId} url=${mediaUrl} err=${String(err)}`,
      );
      target.auditSink?.({
        transport: "kefu",
        category: "fallback-delivery-failed",
        summary: `kefu media delivery failed url=${mediaUrl}`,
        messageId: event.messageId,
        raw: event.raw,
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }

  const plainText = toKefuText(text);
  if (plainText.trim()) {
    try {
      await deliverKefuText(deliveryTarget, plainText);
      target.touchTransportSession?.({ lastOutboundAt: Date.now(), running: true });
    } catch (err) {
      target.runtimeEnv.error?.(
        `[wecom] outbound(kefu): text_failed accountId=${target.kefu.accountId} err=${String(err)}`,
      );
      target.auditSink?.({
        transport: "kefu",
        category: "fallback-delivery-failed",
        summary: `kefu text delivery failed`,
        messageId: event.messageId,
        raw: event.raw,
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }
}

function extractLinkFromChannelData(
  channelData: Record<string, unknown>,
): { title: string; desc?: string; url: string; thumbMediaId?: string } | undefined {
  const kefu = channelData.kefu;
  if (!kefu || typeof kefu !== "object") return undefined;
  const rec = kefu as Record<string, unknown>;
  const link = rec.link;
  if (!link || typeof link !== "object") return undefined;
  const linkRec = link as Record<string, unknown>;
  const url = typeof linkRec.url === "string" ? linkRec.url.trim() : "";
  const title = typeof linkRec.title === "string" ? linkRec.title.trim() : "";
  if (!url || !title) return undefined;
  return {
    title,
    desc: typeof linkRec.desc === "string" ? linkRec.desc : undefined,
    url,
    thumbMediaId: typeof linkRec.thumbMediaId === "string" ? linkRec.thumbMediaId : undefined,
  };
}
