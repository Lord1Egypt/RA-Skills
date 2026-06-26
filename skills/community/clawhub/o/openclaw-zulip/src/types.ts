// Zulip adapter type definitions
// Based on Zulip REST API v1 and chat-infra spec (phase1/zulip-api-client-spec.md)

import type {
  BlockStreamingCoalesceConfig,
  DmConfig,
  DmPolicy,
  GroupPolicy,
  GroupToolPolicyBySenderConfig,
  GroupToolPolicyConfig,
  MarkdownConfig,
  OpenClawConfig,
  BaseProbeResult,
} from "./runtime-api.js";

// ─── Client Config ───

export interface ZulipClientConfig {
  realm: string; // e.g. "https://myorg.zulipchat.com"
  email: string; // bot email
  apiKey: string; // bot API key
  timeout?: number; // HTTP timeout ms, default 90_000
}

// ─── API Response Types ───

export interface ServerSettings {
  zulip_version: string;
  zulip_feature_level: number;
  push_notifications_enabled: boolean;
  require_email_format_usernames: boolean;
  authentication_methods: Record<string, boolean>;
}

export interface OwnUser {
  user_id: number;
  email: string;
  full_name: string;
  is_bot: boolean;
}

export interface SendMessageParams {
  type: "stream" | "channel" | "direct" | "private";
  to: string | number | number[];
  topic?: string;
  content: string;
}

export interface SendMessageResponse {
  id: number;
  deliver_at?: string;
}

export interface UploadFileResponse {
  uri: string;
  url?: string;
}

export interface GetMessagesParams {
  anchor: number | "newest" | "oldest" | "first_unread";
  num_before: number;
  num_after: number;
  narrow?: NarrowFilter[];
}

export interface NarrowFilter {
  operator: "channel" | "topic" | "sender" | "dm" | "is" | "search" | "stream";
  operand: string | number | number[];
}

export interface ZulipMessage {
  id: number;
  sender_id: number;
  sender_email: string;
  sender_full_name: string;
  type: "stream" | "private";
  stream_id?: number;
  display_recipient: string | DirectMessageRecipient[];
  subject: string; // topic name
  content: string; // rendered HTML
  timestamp: number;
}

export interface DirectMessageRecipient {
  id: number;
  email: string;
  full_name: string;
}

export interface GetMessagesResponse {
  messages: ZulipMessage[];
  found_anchor: boolean;
  found_newest: boolean;
  found_oldest: boolean;
}

// ─── Event Queue Types ───

export interface RegisterQueueParams {
  event_types?: string[];
  narrow?: NarrowFilter[];
  all_public_streams?: boolean;
  apply_markdown?: boolean;
  idle_queue_timeout?: number;
}

export interface RegisterResponse {
  queue_id: string;
  last_event_id: number;
  idle_queue_timeout_secs: number;
  max_message_length: number;
  max_topic_length: number;
  max_file_upload_size_mib: number;
  zulip_version: string;
  zulip_feature_level: number;
}

export interface MessageEvent {
  type: "message";
  id: number;
  message: ZulipMessage;
  flags: string[];
}

export interface HeartbeatEvent {
  type: "heartbeat";
  id: number;
}

export interface UpdateMessageEvent {
  type: "update_message";
  id: number;
  message_id: number;
  stream_id?: number;
  orig_subject?: string;
  subject?: string;
  propagate_mode?: "change_one" | "change_later" | "change_all";
}

export type ZulipEvent = MessageEvent | HeartbeatEvent | UpdateMessageEvent;

export interface EventsResponse {
  events: ZulipEvent[];
}

// ─── API Error ───

export interface ZulipApiError {
  result: "error";
  msg: string;
  code?: string;
}

// ─── Adapter Config Types ───

export type ZulipStreamConfig = {
  requireMention?: boolean;
  tools?: GroupToolPolicyConfig;
  toolsBySender?: GroupToolPolicyBySenderConfig;
  skills?: string[];
  enabled?: boolean;
  allowFrom?: Array<string | number>;
  systemPrompt?: string;
};

export type ZulipAccountConfig = {
  name?: string;
  enabled?: boolean;
  realm?: string;
  email?: string;
  apiKey?: string;
  dmPolicy?: DmPolicy;
  allowFrom?: Array<string | number>;
  defaultTo?: string;
  groupPolicy?: GroupPolicy;
  groupAllowFrom?: Array<string | number>;
  streams?: string[];
  defaultStream?: string;
  defaultTopic?: string;
  groups?: Record<string, ZulipStreamConfig>;
  markdown?: MarkdownConfig;
  historyLimit?: number;
  dmHistoryLimit?: number;
  dms?: Record<string, DmConfig>;
  textChunkLimit?: number;
  blockStreaming?: boolean;
  blockStreamingCoalesce?: BlockStreamingCoalesceConfig;
  responsePrefix?: string;
  mediaMaxMb?: number;
};

export type ZulipConfig = ZulipAccountConfig & {
  accounts?: Record<string, ZulipAccountConfig>;
  defaultAccount?: string;
};

export type CoreConfig = OpenClawConfig & {
  channels?: OpenClawConfig["channels"] & {
    zulip?: ZulipConfig;
  };
};

// ─── Inbound Message ───

export type ZulipInboundMessage = {
  messageId: string;
  target: string; // stream#topic for groups, sender email/id for DMs
  senderEmail: string;
  senderId: number;
  senderName: string;
  text: string;
  timestamp: number;
  isGroup: boolean;
  streamName?: string;
  topic?: string;
};

// ─── Probe ───

export type ZulipProbe = BaseProbeResult<string> & {
  realm: string;
  version: string;
  featureLevel: number;
  latencyMs?: number;
};
