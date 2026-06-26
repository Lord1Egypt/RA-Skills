import type { BaseMessage, EventMessage, WsFrame } from "@wecom/aibot-node-sdk";

import { buildInboundBody } from "../bot-webhook/message-shape.js";
import type {
  ResolvedBotAccount,
  UnifiedInboundEvent,
  WecomBotInboundMessage,
  WecomInboundKind,
} from "../../types/index.js";

function resolveInboundKind(message: BaseMessage | EventMessage): WecomInboundKind {
  if (message.msgtype === "event") {
    const eventType = String((message as EventMessage).event?.eventtype ?? "").trim();
    if (eventType === "enter_chat") return "welcome";
    if (eventType === "template_card_event") return "template-card-event";
    return "event";
  }
  switch (message.msgtype) {
    case "image":
      return "image";
    case "file":
      return "file";
    case "voice":
      return "voice";
    case "video":
      return "video";
    case "mixed":
      return "mixed";
    default:
      return "text";
  }
}

function pushAttachment(
  list: NonNullable<UnifiedInboundEvent["attachments"]>,
  name: "image" | "file" | "video",
  remoteUrl?: string,
  aesKey?: string,
): void {
  if (!remoteUrl) {
    return;
  }
  list.push({ name, remoteUrl, aesKey });
}

function resolveEventText(message: BaseMessage | EventMessage, account: ResolvedBotAccount): string {
  if (message.msgtype !== "event") {
    return buildInboundBody(message as WecomBotInboundMessage);
  }

  const event = message as EventMessage;
  if (event.event?.eventtype === "enter_chat" && account.config.welcomeText) {
    return account.config.welcomeText;
  }
  return `[event:${String(event.event?.eventtype ?? "unknown")}]`;
}

export function mapBotWsFrameToInboundEvent(params: {
  account: ResolvedBotAccount;
  frame: WsFrame<BaseMessage | EventMessage>;
}): UnifiedInboundEvent {
  const { account, frame } = params;
  const body = frame.body;
  if (!body) {
    throw new Error("Bot WS frame body is required");
  }
  const peerKind = body.chattype === "group" ? "group" : "direct";
  const senderId = body.from?.userid ?? "unknown";
  const peerId = peerKind === "group" ? body.chatid ?? senderId : senderId;
  const inboundKind = resolveInboundKind(body);

  let attachments: UnifiedInboundEvent["attachments"];
  const collected: NonNullable<UnifiedInboundEvent["attachments"]> = [];
  const collectFromMixedItems = (items: unknown): void => {
    if (!Array.isArray(items)) return;
    for (const item of items) {
      const itemType = String(item?.msgtype ?? "").toLowerCase();
      if (itemType === "image") {
        pushAttachment(collected, "image", item.image?.url, item.image?.aeskey);
      } else if (itemType === "file") {
        pushAttachment(collected, "file", item.file?.url, item.file?.aeskey);
      } else if (itemType === "video") {
        pushAttachment(collected, "video", item.video?.url, item.video?.aeskey);
      }
    }
  };

  if (body.msgtype === "image") {
    pushAttachment(collected, "image", (body as any).image?.url, (body as any).image?.aeskey);
  } else if (body.msgtype === "file") {
    pushAttachment(collected, "file", (body as any).file?.url, (body as any).file?.aeskey);
  } else if (body.msgtype === "video") {
    pushAttachment(collected, "video", (body as any).video?.url, (body as any).video?.aeskey);
  } else if (body.msgtype === "mixed") {
    collectFromMixedItems((body as any).mixed?.msg_item);
  }

  // 没有顶层媒体时，尝试从引用消息里提取附件（quote.image/file/video 或 quote.mixed.*）
  if (collected.length === 0) {
    const quote = (body as any).quote;
    if (quote) {
      const quoteType = String(quote.msgtype ?? "").toLowerCase();
      if (quoteType === "image") {
        pushAttachment(collected, "image", quote.image?.url, quote.image?.aeskey);
      } else if (quoteType === "file") {
        pushAttachment(collected, "file", quote.file?.url, quote.file?.aeskey);
      } else if (quoteType === "video") {
        pushAttachment(collected, "video", quote.video?.url, quote.video?.aeskey);
      } else if (quoteType === "mixed") {
        // v2.8.8 ⭐ 之前只取首张以"与 webhook 一致"，但现在 webhook 路径已支持完整 mixed
        // 提取（inbound-normalizer.ts:499 起），ws 这边对齐：把所有 image/file/video 都收上来。
        collectFromMixedItems(quote.mixed?.msg_item);
      }
    }
  }

  // 入向解析可观测性：媒体类型消息但没解析出任何 attachments，通常是 url/aeskey 字段缺失
  // 或 SDK 未来变更字段名 —— 留 warn 日志便于排查。
  if (
    collected.length === 0 &&
    (body.msgtype === "image" ||
      body.msgtype === "file" ||
      body.msgtype === "video" ||
      body.msgtype === "mixed")
  ) {
    console.warn(
      `[wecom-ws-inbound] media-typed message produced no attachments msgtype=${body.msgtype} msgid=${body.msgid ?? "?"} keys=${Object.keys(body as object).join(",")}`,
    );
  }

  if (collected.length > 0) {
    attachments = collected;
  }

  return {
    accountId: account.accountId,
    capability: "bot",
    transport: "bot-ws",
    inboundKind,
    messageId: body.msgid,
    conversation: {
      accountId: account.accountId,
      peerKind,
      peerId,
      senderId,
    },
    senderName: senderId,
    text: resolveEventText(body, account),
    timestamp: typeof body.create_time === "number" ? body.create_time : Date.now(),
    raw: {
      transport: "bot-ws",
      command: frame.cmd,
      headers: frame.headers,
      body,
      envelopeType: "ws",
    },
    replyContext: {
      transport: "bot-ws",
      accountId: account.accountId,
      reqId: frame.headers.req_id,
      raw: {
        transport: "bot-ws",
        command: frame.cmd,
        headers: frame.headers,
        body,
        envelopeType: "ws",
      },
    },
    ...(attachments && { attachments }),
  };
}
