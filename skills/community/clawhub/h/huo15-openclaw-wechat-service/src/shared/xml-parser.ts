import { XMLBuilder, XMLParser } from "fast-xml-parser";

import type {
  WechatServiceEventType,
  WechatServiceInboundMessage,
  WechatServiceMsgType,
  WechatServicePassiveReply,
} from "../types.js";

const parser = new XMLParser({
  ignoreAttributes: true,
  processEntities: true,
  trimValues: true,
  parseTagValue: false,
  allowBooleanAttributes: false,
  cdataPropName: "__cdata",
});

const builder = new XMLBuilder({
  ignoreAttributes: true,
  processEntities: false,
  format: false,
  cdataPropName: "__cdata",
  suppressEmptyNode: true,
});

export function parseXmlObject(xml: string): Record<string, unknown> {
  const raw = parser.parse(xml) as Record<string, unknown>;
  const root = (raw?.xml ?? raw) as Record<string, unknown>;
  return unwrapCdata(root);
}

function unwrapCdata(input: unknown): Record<string, unknown> {
  if (!input || typeof input !== "object") return {};
  const output: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(input as Record<string, unknown>)) {
    if (value && typeof value === "object" && "__cdata" in value) {
      output[key] = String((value as { __cdata: unknown }).__cdata ?? "");
    } else if (Array.isArray(value)) {
      output[key] = value.map((v) =>
        v && typeof v === "object" && "__cdata" in v
          ? String((v as { __cdata: unknown }).__cdata ?? "")
          : unwrapIfObject(v),
      );
    } else if (value && typeof value === "object") {
      output[key] = unwrapCdata(value);
    } else {
      output[key] = value;
    }
  }
  return output;
}

function unwrapIfObject(value: unknown): unknown {
  if (value && typeof value === "object") {
    return unwrapCdata(value);
  }
  return value;
}

export function extractEncryptField(xml: string): string {
  const parsed = parseXmlObject(xml);
  const encrypt = parsed.Encrypt;
  if (typeof encrypt !== "string" || !encrypt) {
    throw new Error("Encrypt field missing in payload");
  }
  return encrypt;
}

function toNumber(value: unknown): number | undefined {
  if (value == null) return undefined;
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : undefined;
}

function toStringValue(value: unknown): string {
  if (value == null) return "";
  return String(value);
}

/**
 * **parseInboundMessage**
 *
 * 把微信服务号推送的 XML 明文解析为结构化 InboundMessage。
 * 覆盖 text / image / voice / video / shortvideo / location / link / event 所有类型。
 */
export function parseInboundMessage(xml: string): WechatServiceInboundMessage {
  const raw = parseXmlObject(xml);
  const msgType = toStringValue(raw.MsgType).toLowerCase() as WechatServiceMsgType;
  const message: WechatServiceInboundMessage = {
    toUserName: toStringValue(raw.ToUserName),
    fromUserName: toStringValue(raw.FromUserName),
    createTime: toNumber(raw.CreateTime) ?? Math.floor(Date.now() / 1000),
    msgType: (isKnownMsgType(msgType) ? msgType : "unknown") as WechatServiceMsgType,
    raw,
    rawXml: xml,
  };

  const maybe = (key: string): string | undefined => {
    const value = raw[key];
    if (typeof value === "string" && value.length > 0) return value;
    if (typeof value === "number") return String(value);
    return undefined;
  };

  message.msgId = maybe("MsgId") ?? maybe("MsgID");
  message.content = maybe("Content");
  message.picUrl = maybe("PicUrl");
  message.mediaId = maybe("MediaId");
  message.format = maybe("Format");
  message.recognition = maybe("Recognition");
  message.thumbMediaId = maybe("ThumbMediaId");
  message.title = maybe("Title");
  message.description = maybe("Description");
  message.url = maybe("Url");
  message.ticket = maybe("Ticket");
  message.eventKey = maybe("EventKey");

  message.locationX = toNumber(raw.Location_X ?? raw.LocationX);
  message.locationY = toNumber(raw.Location_Y ?? raw.LocationY);
  message.scale = toNumber(raw.Scale);
  message.label = maybe("Label");
  message.latitude = toNumber(raw.Latitude);
  message.longitude = toNumber(raw.Longitude);
  message.precision = toNumber(raw.Precision);

  if (message.msgType === "event") {
    const event = toStringValue(raw.Event);
    message.event = event as WechatServiceEventType;
  }

  return message;
}

function isKnownMsgType(msgType: string): boolean {
  return [
    "text",
    "image",
    "voice",
    "video",
    "shortvideo",
    "location",
    "link",
    "event",
  ].includes(msgType);
}

function cdata(content: string): { __cdata: string } {
  return { __cdata: content };
}

/**
 * **buildPassiveReplyXml**
 *
 * 生成微信服务号被动回复的 XML。5 秒超时窗口内写入。
 */
export function buildPassiveReplyXml(params: {
  toUser: string;
  fromUser: string;
  reply: WechatServicePassiveReply;
  createTime?: number;
}): string {
  const createTime = params.createTime ?? Math.floor(Date.now() / 1000);
  const base: Record<string, unknown> = {
    ToUserName: cdata(params.toUser),
    FromUserName: cdata(params.fromUser),
    CreateTime: createTime,
  };

  switch (params.reply.type) {
    case "text":
      base.MsgType = cdata("text");
      base.Content = cdata(params.reply.content);
      break;
    case "image":
      base.MsgType = cdata("image");
      base.Image = { MediaId: cdata(params.reply.mediaId) };
      break;
    case "voice":
      base.MsgType = cdata("voice");
      base.Voice = { MediaId: cdata(params.reply.mediaId) };
      break;
    case "video":
      base.MsgType = cdata("video");
      base.Video = {
        MediaId: cdata(params.reply.mediaId),
        Title: cdata(params.reply.title ?? ""),
        Description: cdata(params.reply.description ?? ""),
      };
      break;
    case "music":
      base.MsgType = cdata("music");
      base.Music = {
        Title: cdata(params.reply.title ?? ""),
        Description: cdata(params.reply.description ?? ""),
        MusicUrl: cdata(params.reply.musicUrl ?? ""),
        HQMusicUrl: cdata(params.reply.hqMusicUrl ?? ""),
        ThumbMediaId: cdata(params.reply.thumbMediaId),
      };
      break;
    case "news":
      base.MsgType = cdata("news");
      base.ArticleCount = params.reply.articles.length;
      base.Articles = {
        item: params.reply.articles.map((article) => ({
          Title: cdata(article.title),
          Description: cdata(article.description ?? ""),
          PicUrl: cdata(article.picUrl ?? ""),
          Url: cdata(article.url ?? ""),
        })),
      };
      break;
    case "transfer_customer_service":
      base.MsgType = cdata("transfer_customer_service");
      if (params.reply.kfAccount) {
        base.TransInfo = { KfAccount: cdata(params.reply.kfAccount) };
      }
      break;
    default: {
      const exhaustive: never = params.reply;
      throw new Error(`Unsupported passive reply type: ${JSON.stringify(exhaustive)}`);
    }
  }

  return builder.build({ xml: base }) as string;
}

/**
 * **buildEncryptedReplyXml**
 *
 * 包装加密回复的外层 XML（微信服务号兼容/安全模式要求）。
 */
export function buildEncryptedReplyXml(params: {
  encrypt: string;
  msgSignature: string;
  timestamp: string;
  nonce: string;
}): string {
  return builder.build({
    xml: {
      Encrypt: cdata(params.encrypt),
      MsgSignature: cdata(params.msgSignature),
      TimeStamp: params.timestamp,
      Nonce: cdata(params.nonce),
    },
  }) as string;
}
