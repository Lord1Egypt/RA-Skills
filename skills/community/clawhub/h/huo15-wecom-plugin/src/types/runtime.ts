import type { PluginRuntime } from "openclaw/plugin-sdk";

import type { ResolvedAgentAccount, ResolvedBotAccount, ResolvedWecomAccount } from "./account.js";

export type WecomCapabilityKind = "bot" | "agent" | "kefu";
export type WecomTransportKind =
  | "bot-ws"
  | "bot-webhook"
  | "agent-callback"
  | "agent-api"
  | "kefu";
export type WecomAuditCategory =
  | "inbound"
  | "duplicate-inbound"
  | "duplicate-reply"
  | "owner-drift"
  | "ws-kicked"
  | "media-decrypt-failed"
  | "fallback-delivery-failed"
  | "runtime-error";
export type WecomRuntimeHealth = "idle" | "healthy" | "degraded" | "down";
export type WecomInboundKind =
  | "text"
  | "image"
  | "file"
  | "voice"
  | "video"
  | "mixed"
  | "location"
  | "link"
  | "event"
  | "welcome"
  | "template-card-event"
  | "miniprogram"
  | "menu"
  | "business-card"
  | "kefu-session-event";

export type ConversationRef = {
  accountId: string;
  peerKind: "direct" | "group";
  peerId: string;
  senderId: string;
};

export type RawFrameReference = {
  transport: WecomTransportKind;
  command?: string;
  headers?: Record<string, unknown>;
  body?: unknown;
  envelopeType: "json" | "xml" | "ws";
};

export type ReplyContext = {
  transport: WecomTransportKind;
  accountId: string;
  responseUrl?: string;
  reqId?: string;
  streamId?: string;
  webhookNonce?: string;
  webhookTimestamp?: string;
  passiveWindowMs?: number;
  /** WeCom peer identifier (userId for direct, chatId for group) */
  peerId?: string;
  peerKind?: "direct" | "group";
  raw: RawFrameReference;
};

export type UnifiedInboundEvent = {
  accountId: string;
  capability: WecomCapabilityKind;
  transport: WecomTransportKind;
  inboundKind: WecomInboundKind;
  messageId: string;
  conversation: ConversationRef;
  text: string;
  senderName?: string;
  timestamp: number;
  raw: RawFrameReference;
  replyContext: ReplyContext;
  attachments?: Array<{
    name?: string;
    contentType?: string;
    remoteUrl?: string;
    aesKey?: string;
  }>;
};

export type ReplyDeliveryInfo = {
  kind: "block" | "final" | "error";
};

export type ReplyPayload = {
  text?: string;
  mediaUrl?: string;
  mediaUrls?: string[];
  replyToId?: string;
  replyToTag?: boolean;
  replyToCurrent?: boolean;
  audioAsVoice?: boolean;
  isError?: boolean;
  isReasoning?: boolean;
  channelData?: Record<string, unknown>;
};

export type ReplyHandle = {
  context: ReplyContext;
  deliver: (payload: ReplyPayload, info: ReplyDeliveryInfo) => Promise<void>;
  fail?: (error: unknown) => Promise<void>;
  markExternalActivity?: () => void;
};

export type TransportSessionSnapshot = {
  accountId: string;
  transport: WecomTransportKind;
  running: boolean;
  ownerId?: string;
  connected?: boolean;
  authenticated?: boolean;
  lastConnectedAt?: number;
  lastDisconnectedAt?: number;
  lastInboundAt?: number;
  lastOutboundAt?: number;
  lastError?: string;
};

export type TransportSessionPatch = Partial<Omit<TransportSessionSnapshot, "accountId" | "transport">> & {
  lastError?: string | null;
};

export type AccountRuntimeStatusSnapshot = {
  accountId: string;
  health: WecomRuntimeHealth;
  transport?: WecomTransportKind;
  ownerId?: string | null;
  connected?: boolean;
  authenticated?: boolean;
  ownerDriftAt?: number | null;
  lastError?: string | null;
  lastErrorAt?: number | null;
  lastInboundAt?: number | null;
  lastOutboundAt?: number | null;
  recentInboundSummary?: string | null;
  recentOutboundSummary?: string | null;
  recentIssueCategory?: WecomAuditCategory | null;
  recentIssueSummary?: string | null;
  transportSessions?: string[];
};

export type DeliveryTask = {
  accountId: string;
  transport: WecomTransportKind;
  conversation: ConversationRef;
  messageId: string;
  status: "pending" | "delivered" | "failed";
  createdAt: number;
  updatedAt: number;
  error?: string;
};

export type RuntimeLogSink = {
  info?: (message: string) => void;
  warn?: (message: string) => void;
  error?: (message: string) => void;
};

export type RuntimeServices = {
  core: PluginRuntime;
  log: RuntimeLogSink;
};

export type AccountRuntimeContext = {
  account: ResolvedWecomAccount;
  bot?: ResolvedBotAccount;
  agent?: ResolvedAgentAccount;
  services: RuntimeServices;
};
