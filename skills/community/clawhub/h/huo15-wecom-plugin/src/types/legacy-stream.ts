import type { WecomBotInboundMessage as WecomInboundMessage } from "./message.js";
import type { WecomWebhookTarget } from "./runtime-context.js";

export type StreamState = {
  streamId: string;
  msgid?: string;
  conversationKey?: string;
  batchKey?: string;
  userId?: string;
  chatType?: "group" | "direct";
  chatId?: string;
  aibotid?: string;
  taskKey?: string;
  createdAt: number;
  updatedAt: number;
  started: boolean;
  finished: boolean;
  error?: string;
  content: string;
  images?: { base64: string; md5: string }[];
  fallbackMode?: "media" | "timeout" | "error";
  fallbackPromptSentAt?: number;
  finalDeliveredAt?: number;
  dmContent?: string;
  agentMediaKeys?: string[];
};

export type PendingInbound = {
  streamId: string;
  conversationKey: string;
  batchKey: string;
  target: WecomWebhookTarget;
  msg: WecomInboundMessage;
  contents: string[];
  media?: { buffer: Buffer; contentType: string; filename: string };
  msgids: string[];
  nonce: string;
  timestamp: string;
  timeout: ReturnType<typeof setTimeout> | null;
  readyToFlush?: boolean;
  createdAt: number;
};

export type ActiveReplyState = {
  response_url: string;
  proxyUrl?: string;
  createdAt: number;
  usedAt?: number;
  lastError?: string;
};
