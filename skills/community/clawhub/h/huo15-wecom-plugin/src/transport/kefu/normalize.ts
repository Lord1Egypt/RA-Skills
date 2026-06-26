import type {
  ReplyContext,
  UnifiedInboundEvent,
  WecomInboundKind,
} from "../../types/index.js";
import type { KefuSyncMessage } from "./api-client.js";

type KefuNormalizeArgs = {
  accountId: string;
  msg: KefuSyncMessage;
  rawXml: string;
  token: string;
};

export type KefuNormalizedEvent = {
  event: UnifiedInboundEvent;
  openKfId: string;
  externalUserId: string;
  mediaId?: string;
  attachmentName?: string;
  link?: {
    title: string;
    desc?: string;
    url: string;
    thumbMediaId?: string;
  };
  miniProgram?: {
    title?: string;
    appId?: string;
    pagepath?: string;
    thumbMediaId?: string;
  };
  location?: {
    latitude?: number;
    longitude?: number;
    name?: string;
    address?: string;
  };
  eventType?: string;
  welcomeCode?: string;
  rawMsgType: string;
};

function coerceString(value: unknown): string {
  if (value == null) return "";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean" || typeof value === "bigint") {
    return String(value);
  }
  return "";
}

function readObject(value: unknown): Record<string, unknown> {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return value as Record<string, unknown>;
  }
  return {};
}

function resolveInboundKind(msgType: string, eventType: string): WecomInboundKind {
  const lower = msgType.toLowerCase();
  switch (lower) {
    case "text":
      return "text";
    case "image":
      return "image";
    case "voice":
      return "voice";
    case "video":
      return "video";
    case "file":
      return "file";
    case "location":
      return "location";
    case "link":
      return "link";
    case "miniprogram":
      return "miniprogram";
    case "msgmenu":
      return "menu";
    case "business_card":
      return "business-card";
    case "event":
      if (eventType === "enter_session") return "welcome";
      return "kefu-session-event";
    default:
      return "event";
  }
}

function resolveText(msg: KefuSyncMessage, msgType: string, eventType: string): string {
  const lower = msgType.toLowerCase();
  if (lower === "text") {
    return coerceString(readObject(msg.text).content);
  }
  if (lower === "image") {
    return "[图片]";
  }
  if (lower === "voice") {
    return "[语音]";
  }
  if (lower === "video") {
    return "[视频]";
  }
  if (lower === "file") {
    const name = coerceString(readObject(msg.file).filename);
    return name ? `[文件] ${name}` : "[文件]";
  }
  if (lower === "location") {
    const loc = readObject(msg.location);
    const name = coerceString(loc.name);
    const address = coerceString(loc.address);
    return `[位置] ${[name, address].filter(Boolean).join(" ")}`.trim();
  }
  if (lower === "link") {
    const link = readObject(msg.link);
    const title = coerceString(link.title);
    const desc = coerceString(link.desc);
    const url = coerceString(link.url);
    return `[链接] ${title}\n${desc}\n${url}`.trim();
  }
  if (lower === "miniprogram") {
    const mp = readObject(msg.miniprogram);
    const title = coerceString(mp.title);
    return `[小程序] ${title || coerceString(mp.appid)}`.trim();
  }
  if (lower === "msgmenu") {
    const menu = readObject(msg.msgmenu);
    return coerceString(menu.head_content) || "[菜单消息]";
  }
  if (lower === "business_card") {
    const card = readObject(msg.business_card);
    return `[名片] ${coerceString(card.userid)}`.trim();
  }
  if (lower === "event") {
    return `[客服事件] ${eventType || "unknown"}`;
  }
  return `[${msgType || "未知消息"}]`;
}

function resolveMediaId(msg: KefuSyncMessage, msgType: string): string | undefined {
  const lower = msgType.toLowerCase();
  if (lower === "image") return coerceString(readObject(msg.image).media_id) || undefined;
  if (lower === "voice") return coerceString(readObject(msg.voice).media_id) || undefined;
  if (lower === "video") return coerceString(readObject(msg.video).media_id) || undefined;
  if (lower === "file") return coerceString(readObject(msg.file).media_id) || undefined;
  return undefined;
}

function resolveAttachmentName(msg: KefuSyncMessage, msgType: string): string | undefined {
  const lower = msgType.toLowerCase();
  if (lower === "file") {
    const name = coerceString(readObject(msg.file).filename);
    return name || undefined;
  }
  return undefined;
}

function resolveLink(msg: KefuSyncMessage, msgType: string): KefuNormalizedEvent["link"] {
  if (msgType.toLowerCase() !== "link") return undefined;
  const link = readObject(msg.link);
  const url = coerceString(link.url);
  if (!url) return undefined;
  return {
    title: coerceString(link.title),
    desc: coerceString(link.desc) || undefined,
    url,
    thumbMediaId: coerceString(link.thumb_media_id) || undefined,
  };
}

function resolveMiniProgram(msg: KefuSyncMessage, msgType: string): KefuNormalizedEvent["miniProgram"] {
  if (msgType.toLowerCase() !== "miniprogram") return undefined;
  const mp = readObject(msg.miniprogram);
  return {
    title: coerceString(mp.title) || undefined,
    appId: coerceString(mp.appid) || undefined,
    pagepath: coerceString(mp.pagepath) || undefined,
    thumbMediaId: coerceString(mp.thumb_media_id) || undefined,
  };
}

function resolveLocation(msg: KefuSyncMessage, msgType: string): KefuNormalizedEvent["location"] {
  if (msgType.toLowerCase() !== "location") return undefined;
  const loc = readObject(msg.location);
  const latitude = Number(coerceString(loc.latitude));
  const longitude = Number(coerceString(loc.longitude));
  return {
    latitude: Number.isFinite(latitude) ? latitude : undefined,
    longitude: Number.isFinite(longitude) ? longitude : undefined,
    name: coerceString(loc.name) || undefined,
    address: coerceString(loc.address) || undefined,
  };
}

/**
 * Convert a raw `KefuSyncMessage` (as returned by `kf/sync_msg`) into a
 * `UnifiedInboundEvent` plus a bundle of kefu-specific side metadata the
 * orchestrator needs (openKfId, media, event type).
 */
export function normalizeKefuMessage(args: KefuNormalizeArgs): KefuNormalizedEvent | null {
  const { accountId, msg, rawXml, token } = args;
  const msgType = coerceString(msg.msgtype).toLowerCase();
  if (!msgType) return null;
  const event = readObject(msg.event);
  const eventType = coerceString(event.event_type);
  const openKfId = coerceString(msg.open_kfid) || coerceString(event.open_kfid);
  const externalUserId = coerceString(msg.external_userid) || coerceString(event.external_userid);
  if (!openKfId) return null;

  const messageId = coerceString(msg.msgid) || `${openKfId}:${externalUserId || "anon"}:${msg.send_time ?? ""}`;
  const sendTime = typeof msg.send_time === "number" && Number.isFinite(msg.send_time)
    ? msg.send_time * 1000
    : Date.now();

  const text = resolveText(msg, msgType, eventType);
  const mediaId = resolveMediaId(msg, msgType);
  const attachmentName = resolveAttachmentName(msg, msgType);
  const link = resolveLink(msg, msgType);
  const miniProgram = resolveMiniProgram(msg, msgType);
  const location = resolveLocation(msg, msgType);

  const conversation = {
    accountId,
    peerKind: "direct" as const,
    peerId: externalUserId || openKfId,
    senderId: externalUserId || "",
  };

  const replyContext: ReplyContext = {
    transport: "kefu",
    accountId,
    peerId: conversation.peerId,
    peerKind: "direct",
    raw: {
      transport: "kefu",
      envelopeType: "json",
      body: msg,
    },
  };

  const attachments = mediaId
    ? [
        {
          name: attachmentName,
          contentType: msgType === "image" ? "image/*" : undefined,
          remoteUrl: undefined,
          aesKey: undefined,
        },
      ]
    : undefined;

  const inboundEvent: UnifiedInboundEvent = {
    accountId,
    capability: "kefu",
    transport: "kefu",
    inboundKind: resolveInboundKind(msgType, eventType),
    messageId,
    conversation,
    text,
    senderName: externalUserId || undefined,
    timestamp: sendTime,
    raw: {
      transport: "kefu",
      envelopeType: "json",
      body: msg,
      headers: { token, rawXml },
    },
    replyContext,
    attachments,
  };

  return {
    event: inboundEvent,
    openKfId,
    externalUserId,
    mediaId,
    attachmentName,
    link,
    miniProgram,
    location,
    eventType: eventType || undefined,
    welcomeCode: coerceString(event.welcome_code) || undefined,
    rawMsgType: msgType,
  };
}
