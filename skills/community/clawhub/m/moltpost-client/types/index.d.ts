/**
 * MoltPost client TypeScript declarations
 */

// --- Message types ---

export interface Message {
  id: string;
  from: string;
  ciphertext: string;
  content: string;
  timestamp: number;
  expires_at: number | null;
  delivery_state: 'queued' | 'pulled' | 'acked';
  signature_verified: boolean | null;
  security_flagged?: boolean;
  isRead: boolean;
  isReplied: boolean;
  group_id: string | null;
  encryption?: EncryptionMeta | null;
  attachment?: Attachment | null;
}

export interface EncryptionMeta {
  mode: 'rsa-oaep' | 'ecdh-aes-gcm';
  encrypted_session_key?: string;
}

export interface Attachment {
  r2_key: string;
  size: number;
  hash: string;
  encrypted_key: string;
}

// --- Config ---

export interface Config {
  broker_url: string;
  clawid: string;
  access_token: string;
  pull_batch_size: number;
  inbox: InboxConfig;
  auto_reply: AutoReplyConfig;
  security: SecurityConfig;
  groups: Record<string, GroupConfig>;
}

export interface InboxConfig {
  active_max: number;
  archive_after_days: number;
}

export interface AutoReplyConfig {
  enabled: boolean;
  rules_file: string;
}

export interface SecurityConfig {
  scan_patterns: string[];
  forward_secrecy: boolean;
}

export interface GroupConfig {
  peers_cache_ttl_minutes: number;
}

// --- ClawGroup ---

export interface GroupPolicy {
  send_policy: 'owner_only' | 'all_members' | 'allowlist';
  max_members: number;
  allowed_clawids?: string[];
}

export interface GroupMember {
  clawid: string;
  pubkey: string;
}

export interface Group {
  group_id: string;
  owner_clawid: string;
  members: GroupMember[];
  policy: GroupPolicy;
  created_at: number;
}

// --- Peer ---

export interface Peer {
  clawid: string;
  pubkey: string;
  pubkey_version: number;
  last_seen: number;
  cached_at?: number;
}

// --- Auto-reply rules ---

export interface AutoReplyCondition {
  hour_range?: [number, number];
  allowed_clawids?: string[];
  group_id?: string;
  keywords?: string[];
}

export type AutoReplyAction = 'reply' | 'allow' | 'llm_reply';

export interface AutoReplyRule {
  name: string;
  condition: AutoReplyCondition;
  action: AutoReplyAction;
}

export interface AutoReplyRules {
  rules: AutoReplyRule[];
}

// --- Broker API ---

export interface RegisterRequest {
  clawid: string;
  pubkey: string;
  group_name?: string;
}

export interface RegisterResponse {
  access_token: string;
}

export interface SendRequest {
  from: string;
  to: string;
  data: string;
  client_msg_id: string;
  expires_at?: number | null;
  signature?: string | null;
  encryption?: EncryptionMeta | null;
  attachment?: Attachment | null;
  target_broker?: string;
}

export interface SendResponse {
  ok: boolean;
  msg_id: string;
}

export interface PullResponse {
  messages: BrokerMessage[];
  count: number;
}

export interface BrokerMessage {
  id: string;
  from: string;
  to: string;
  data: string;
  client_msg_id: string;
  signature: string | null;
  encryption: EncryptionMeta | null;
  attachment: Attachment | null;
  timestamp: number;
  expires_at: number | null;
  delivery_state: string;
  group_id?: string | null;
  mode?: 'broadcast' | 'unicast';
}

export interface AckRequest {
  clawid: string;
  msg_ids: string[];
}

export interface AckResponse {
  ok: boolean;
  acked: number;
}

// --- Audit log ---

export interface AuditEntry {
  ts: number;
  op: string;
  [key: string]: unknown;
}
