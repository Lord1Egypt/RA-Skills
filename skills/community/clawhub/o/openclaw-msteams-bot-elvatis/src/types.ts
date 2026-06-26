import { ConversationReference } from "botbuilder";

/** Logger interface provided by OpenClaw Gateway */
export interface Logger {
  info(message: string, ...args: unknown[]): void;
  warn(message: string, ...args: unknown[]): void;
  error(message: string, ...args: unknown[]): void;
  debug(message: string, ...args: unknown[]): void;
}

/** Inbound message sent to OpenClaw Gateway */
export interface InboundMessage {
  sessionId: string;
  text: string;
  sender?: string;
  metadata?: Record<string, unknown>;
}

/** Response received from OpenClaw Gateway */
export interface GatewayResponse {
  text: string;
  sessionId: string;
  metadata?: Record<string, unknown>;
}

/** Gateway API for interacting with OpenClaw sessions */
export interface GatewayAPI {
  sendMessage(message: InboundMessage): Promise<GatewayResponse>;
  createSession(options: {
    id: string;
    label?: string;
    systemPrompt?: string;
    model?: string;
    metadata?: Record<string, unknown>;
  }): Promise<void>;
  hasSession(id: string): Promise<boolean>;
}

/** Plugin context provided by OpenClaw Gateway to plugins */
export interface PluginContext {
  config: PluginConfig;
  gateway: GatewayAPI;
  logger: Logger;
}

/** Per-channel configuration */
export interface TeamsChannelConfig {
  systemPrompt?: string;
  model?: string;
  label?: string;
}

/** Top-level plugin configuration from openclaw.json */
export interface PluginConfig {
  enabled?: boolean;
  port?: number;
  appId: string;
  appPassword: string;
  appTenantId?: string;
  channels?: Record<string, TeamsChannelConfig>;
}

/** A tracked session mapped from a Teams channel */
export interface SessionEntry {
  sessionId: string;
  channelId: string;
  channelName: string;
  label: string;
  model?: string;
  systemPrompt?: string;
  conversationReference: Partial<ConversationReference>;
}
export interface GraphConfig {
  tenantId: string
  clientId: string
  clientSecret: string
}

export interface GitHubConfig {
  /** GitHub App authentication */
  appId?: number
  privateKey?: string
  installationId?: number
  /** Personal access token authentication */
  token?: string
  /** Default organization filter (e.g. "elvatis") */
  defaultOrg?: string
}

export interface DriveItem {
  id: string
  name: string
  size: number
  webUrl: string
  lastModifiedDateTime: string
  file?: { mimeType: string }
  folder?: { childCount: number }
  parentReference?: {
    driveId: string
    id: string
    path: string
  }
}

export interface Team {
  id: string
  displayName: string
  description: string | null
}

export interface Channel {
  id: string
  displayName: string
  description: string | null
  membershipType: string
}

export interface ToolResult {
  success: boolean
  data?: unknown
  error?: string
}

