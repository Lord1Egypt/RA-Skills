import type { WecomBotInboundMessage as WecomInboundMessage, WecomInboundQuote } from "../../types/index.js";

export type BotInboundProcessDecision = {
  shouldProcess: boolean;
  reason: string;
  senderUserId?: string;
  chatId?: string;
};

export function resolveWecomSenderUserId(msg: WecomInboundMessage): string | undefined {
  const direct = msg.from?.userid?.trim();
  if (direct) return direct;
  const legacy = String((msg as any).fromuserid ?? (msg as any).from_userid ?? (msg as any).fromUserId ?? "").trim();
  return legacy || undefined;
}

export function shouldProcessBotInboundMessage(msg: WecomInboundMessage): BotInboundProcessDecision {
  const senderUserId = resolveWecomSenderUserId(msg)?.trim();
  if (!senderUserId) {
    return { shouldProcess: false, reason: "missing_sender" };
  }
  if (senderUserId.toLowerCase() === "sys") {
    return { shouldProcess: false, reason: "system_sender" };
  }

  const chatType = String(msg.chattype ?? "").trim().toLowerCase();
  if (chatType === "group") {
    const chatId = msg.chatid?.trim();
    if (!chatId) {
      return { shouldProcess: false, reason: "missing_chatid", senderUserId };
    }
    return { shouldProcess: true, reason: "user_message", senderUserId, chatId };
  }

  return { shouldProcess: true, reason: "user_message", senderUserId, chatId: senderUserId };
}

function formatQuote(quote: WecomInboundQuote): string {
  const type = quote.msgtype ?? "";
  if (type === "text") return quote.text?.content || "";
  if (type === "image") return `[引用: 图片] ${quote.image?.url || ""}`;
  if (type === "mixed" && quote.mixed?.msg_item) {
    const items = quote.mixed.msg_item
      .map((item) => {
        if (item.msgtype === "text") return item.text?.content;
        if (item.msgtype === "image") return `[图片] ${item.image?.url || ""}`;
        return "";
      })
      .filter(Boolean)
      .join(" ");
    return `[引用: 图文] ${items}`;
  }
  if (type === "voice") return `[引用: 语音] ${quote.voice?.content || ""}`;
  if (type === "file") return `[引用: 文件] ${quote.file?.url || ""}`;
  // 新增支持：引用视频类型 - 将在入站正规化中提取媒体并落盘
  if (type === "video") return `[引用: 视频] ${quote.video?.url || ""}`;
  return "";
}

export function buildInboundBody(msg: WecomInboundMessage): string {
  let body = "";
  const msgtype = String(msg.msgtype ?? "").toLowerCase();

  if (msgtype === "text") body = (msg as any).text?.content || "";
  else if (msgtype === "voice") body = (msg as any).voice?.content || "[voice]";
  else if (msgtype === "mixed") {
    const items = (msg as any).mixed?.msg_item;
    if (Array.isArray(items)) {
      body = items
        .map((item: any) => {
          const t = String(item?.msgtype ?? "").toLowerCase();
          if (t === "text") return item?.text?.content || "";
          if (t === "image") return `[image] ${item?.image?.url || ""}`;
          return `[${t || "item"}]`;
        })
        .filter(Boolean)
        .join("\n");
    } else body = "[mixed]";
  } else if (msgtype === "image") body = `[image] ${(msg as any).image?.url || ""}`;
  else if (msgtype === "file") body = `[file] ${(msg as any).file?.url || ""}`;
  else if (msgtype === "video") body = `[video] ${(msg as any).video?.url || ""}`;
  else if (msgtype === "event") body = `[event] ${(msg as any).event?.eventtype || ""}`;
  else if (msgtype === "stream") body = `[stream_refresh] ${(msg as any).stream?.id || ""}`;
  else body = msgtype ? `[${msgtype}]` : "";

  const quote = (msg as any).quote;
  if (quote) {
    const quoteText = formatQuote(quote).trim();
    if (quoteText) body += `\n\n> ${quoteText}`;
  }
  return body;
}
