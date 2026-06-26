/**
 * 将解密后的 XML 明文解析成 UnifiedInboundEvent。
 *
 * 微信服务号是 one-to-one 的公众号↔用户关系，所以 peerKind 恒为 "direct"，
 * peerId/senderId 都是发送消息的用户 openid。
 */

import type {
  WechatServiceInboundMessage,
  WechatServiceUnifiedInboundEvent,
} from "../../types.js";

export function buildUnifiedInboundEvent(params: {
  accountId: string;
  inbound: WechatServiceInboundMessage;
}): WechatServiceUnifiedInboundEvent {
  const { accountId, inbound } = params;
  const openid = inbound.fromUserName;
  const messageId = buildMessageId(inbound);
  const text = buildCommandText(inbound);

  return {
    accountId,
    transport: "webhook",
    messageId,
    text,
    senderName: openid,
    conversation: {
      peerKind: "direct",
      peerId: openid,
      senderId: openid,
    },
    replyContext: {
      accountId,
      toUserName: inbound.toUserName,
      fromUserName: inbound.fromUserName,
      receivedAt: Date.now(),
    },
    raw: inbound,
  };
}

function buildMessageId(inbound: WechatServiceInboundMessage): string {
  if (inbound.msgId) return `msg:${inbound.msgId}`;
  if (inbound.msgType === "event") {
    return `evt:${inbound.event ?? "unknown"}:${inbound.fromUserName}:${inbound.createTime}`;
  }
  return `msg:${inbound.fromUserName}:${inbound.createTime}`;
}

function buildCommandText(inbound: WechatServiceInboundMessage): string {
  switch (inbound.msgType) {
    case "text":
      return inbound.content ?? "";
    case "image":
      return `[图片]${inbound.picUrl ? ` ${inbound.picUrl}` : ""}`;
    case "voice":
      return inbound.recognition ? `[语音识别] ${inbound.recognition}` : "[语音]";
    case "video":
      return "[视频]";
    case "shortvideo":
      return "[小视频]";
    case "location":
      return `[位置] ${inbound.label ?? ""} (${inbound.locationX ?? ""},${inbound.locationY ?? ""})`;
    case "link":
      return `[链接] ${inbound.title ?? ""} ${inbound.url ?? ""}`;
    case "event":
      return formatEventText(inbound);
    default:
      return "[未知消息]";
  }
}

function formatEventText(inbound: WechatServiceInboundMessage): string {
  const event = inbound.event ?? "unknown";
  switch (event) {
    case "subscribe":
      return inbound.ticket ? `[扫码关注] ${inbound.eventKey ?? ""}` : "[关注]";
    case "unsubscribe":
      return "[取消关注]";
    case "SCAN":
      return `[扫码] ${inbound.eventKey ?? ""}`;
    case "LOCATION":
      return `[上报位置] (${inbound.latitude ?? ""},${inbound.longitude ?? ""})`;
    case "CLICK":
      return `[菜单点击] ${inbound.eventKey ?? ""}`;
    case "VIEW":
      return `[菜单跳转] ${inbound.eventKey ?? ""}`;
    default:
      return `[事件:${event}]${inbound.eventKey ? ` ${inbound.eventKey}` : ""}`;
  }
}

/**
 * **resolveEventRoutingAgentId**
 *
 * 按事件类型选择 routing.events 中的 agentId（如果配置了），
 * 否则返回 undefined，让上游使用默认路由逻辑。
 */
export function resolveEventRoutingAgentId(params: {
  inbound: WechatServiceInboundMessage;
  routing: {
    events?: Record<string, string | undefined>;
  };
}): string | undefined {
  if (params.inbound.msgType !== "event") return undefined;
  const event = params.inbound.event ?? "";
  const map = params.routing.events ?? {};
  const lookup: Record<string, string> = {
    subscribe: "subscribe",
    unsubscribe: "unsubscribe",
    SCAN: "scan",
    LOCATION: "location",
    CLICK: "click",
    VIEW: "view",
    scancode_push: "scancodePush",
    scancode_waitmsg: "scancodeWaitmsg",
    pic_sysphoto: "picSysphoto",
    pic_photo_or_album: "picPhotoOrAlbum",
    pic_weixin: "picWeixin",
    location_select: "locationSelect",
    TEMPLATESENDJOBFINISH: "templateSendJobFinish",
    MASSSENDJOBFINISH: "massSendJobFinish",
  };
  const key = lookup[event];
  if (!key) return undefined;
  const routed = map[key];
  if (typeof routed === "string" && routed.trim()) return routed.trim();
  return undefined;
}
