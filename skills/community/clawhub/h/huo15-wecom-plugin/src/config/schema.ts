export interface DmConfig {
  policy?: "pairing" | "allowlist" | "open" | "disabled";
  allowFrom?: (string | number)[];
}

export interface MediaConfig {
  tempDir?: string;
  retentionHours?: number;
  cleanupOnStart?: boolean;
  maxBytes?: number;
  downloadTimeoutMs?: number;
  localRoots?: string[];
}

export interface NetworkConfig {
  egressProxyUrl?: string;
  timeoutMs?: number;
  mediaDownloadTimeoutMs?: number;
}

export interface RoutingConfig {
  failClosedOnDefaultRoute?: boolean;
}

export interface BotWsConfig {
  botId: string;
  secret: string;
}

export interface BotWebhookConfig {
  token: string;
  encodingAESKey: string;
  receiveId?: string;
}

export interface BotConfig {
  primaryTransport?: "ws" | "webhook";
  streamPlaceholderContent?: string;
  welcomeText?: string;
  /**
   * v2.8.17+：长任务进度反馈模式。默认 "progress"。仅 bot-ws 生效。
   */
  progressMode?: "progress" | "heartbeat" | "delayed" | "off";
  /**
   * v2.8.17+：progressMode="delayed" 时的沉默时长（毫秒）。默认 30000。
   */
  progressDelayedMs?: number;
  dm?: DmConfig;
  aibotid?: string;
  botIds?: string[];
  ws?: BotWsConfig;
  webhook?: BotWebhookConfig;
}

export interface AgentConfig {
  corpId: string;
  agentSecret?: string;
  corpSecret?: string;
  agentId?: number | string;
  token: string;
  encodingAESKey: string;
  welcomeText?: string;
  dm?: DmConfig;
}

export interface KefuWebhookConfig {
  token: string;
  encodingAESKey: string;
}

export interface KefuConfig {
  corpId: string;
  corpSecret: string;
  openKfIds: string[];
  webhook: KefuWebhookConfig;
  welcomeText?: string;
  dm?: DmConfig;
}

export interface DynamicAgentsConfig {
  enabled?: boolean;
  dmCreateAgent?: boolean;
  groupEnabled?: boolean;
  adminUsers?: string[];
}

export interface AccountConfig {
  enabled?: boolean;
  name?: string;
  mediaMaxMb?: number;
  bot?: BotConfig;
  agent?: AgentConfig;
  kefu?: KefuConfig;
}

export interface WecomConfigInput {
  enabled?: boolean;
  mediaMaxMb?: number;
  mediaDownloadTimeoutMs?: number;
  bot?: BotConfig;
  agent?: AgentConfig;
  kefu?: KefuConfig;
  accounts?: Record<string, AccountConfig>;
  defaultAccount?: string;
  media?: MediaConfig;
  network?: NetworkConfig;
  routing?: RoutingConfig;
  dynamicAgents?: DynamicAgentsConfig;
}

/**
 * @deprecated No longer a Zod schema. Kept as a type-only export for backward compatibility.
 */
export const WecomConfigSchema = undefined;
