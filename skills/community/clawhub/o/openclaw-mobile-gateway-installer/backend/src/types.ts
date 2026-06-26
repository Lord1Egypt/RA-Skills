export type OpenClawVersion = "v1" | "v2" | "v3";

export interface OpenClawTarget {
  domain: string;
  version: OpenClawVersion;
  apiBaseUrl: string;
  gatewayToken?: string;
  healthPath?: string;
  chatPaths?: string[];
  authHeaderName?: string;
  authHeaderValue?: string;
  extraHeaders?: Record<string, string>;
  timeoutMs?: number;
}

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface ModelConfig {
  id: string;
  modelId: string;
  providerId: string;
  platform: string;
  name: string;
  enabled: boolean;
  maxTokens: number;
  apiKey?: string;
  baseUrl?: string;
}

export interface SkillConfig {
  id: string;
  name: string;
  enabled: boolean;
  description: string;
  group: string;
}

export interface ChannelConfig {
  id: string;
  name: string;
  enabled: boolean;
  weight: number;
  robotId?: string;
  robotSecret?: string;
}

export interface TokenUsageRecord {
  id: string;
  modelId: string;
  channelId: string;
  promptTokens: number;
  completionTokens: number;
  createdAt: string;
}

export interface MarkdownFileRecord {
  fileName: string;
  content: string;
}

export interface QuickActionItem {
  id: string;
  name: string;
  description: string;
}

export type RoutingScope = "global" | "domain";

export interface RoutingRule {
  taskTypes: string[];
  primaryModelId: string;
  fallbackModelIds: string[];
  channelPriority: string[];
  maxBudgetPerRequest?: number;
}

export interface RoutingStrategy {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  scope: RoutingScope;
  domain?: string;
  rules: RoutingRule[];
  hitCount: number;
  updatedAt: string;
}

export interface HealPolicy {
  enabled: boolean;
  windowSec: number;
  trigger: {
    errorRate: number;
    timeoutRate: number;
  };
  actions: Array<"retry" | "switch-model" | "switch-channel" | "restart-gateway" | "rollback">;
  updatedAt: string;
}

export interface HealEvent {
  id: string;
  domain: string;
  reason: string;
  action: string;
  result: "success" | "failed";
  createdAt: string;
}

export interface AppUpdatePolicy {
  platform: "android";
  channel: "samsung";
  latestVersionName: string;
  latestVersionCode: number;
  minSupportedVersionCode: number;
  forceUpdate: boolean;
  downloadUrl: string;
  releaseNotes: string;
  updatedAt: string;
}

export interface ServiceStatus {
  service: "gateway";
  installed: boolean;
  active: boolean;
  pid: number | null;
  detail: string;
  checkedAt: string;
}

export interface SecurityConfig {
  accessPasswordSet: boolean;
  ignoreRisk: boolean;
  updatedAt: string;
}

export interface PanelSettings {
  networkProxyUrl: string;
  proxyModelRequests: boolean;
  npmRegistry: string;
  updatedAt: string;
}

export interface AgentProfile {
  id: string;
  name: string;
  workspace: string;
  enabled: boolean;
  primaryModelId: string;
  fallbackModelIds: string[];
  updatedAt: string;
}

export interface CommunicationConfig {
  messages: {
    autoReplyEnabled: boolean;
    autoReplyTemplate: string;
  };
  broadcast: {
    strategy: "all" | "priority";
    defaultChannelId: string;
  };
  commands: {
    enabled: boolean;
    prefix: string;
  };
  hooks: {
    enabled: boolean;
    webhookUrl: string;
  };
  approvals: {
    execEnabled: boolean;
    requireConfirm: boolean;
  };
  updatedAt: string;
}

export interface MemoryFileItem {
  agentId: string;
  category: string;
  fileName: string;
  content: string;
  updatedAt: string;
}

export interface CronJob {
  id: string;
  name: string;
  cron: string;
  enabled: boolean;
  taskType: string;
  payload: string;
  updatedAt: string;
}

export interface ChatWsSession {
  sessionId: string;
  connectedAt: string;
  status: "connected" | "closed";
}

export interface AssistantSession {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
}

export interface AssistantMessage {
  id: string;
  sessionId: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
}

export interface AboutInfo {
  appName: string;
  appVersion: string;
  backendVersion: string;
  openclawLastUpdateAt: string;
  gatewayLastRestartAt: string;
}

export interface SkillDependencyIssue {
  name: string;
  severity: "info" | "warning" | "error";
  installed: boolean;
  message: string;
  fixHint?: string;
}

export interface SkillDependencyReport {
  skillId: string;
  ready: boolean;
  issues: SkillDependencyIssue[];
  checkedAt: string;
}
