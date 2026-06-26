export type WecomDmPolicy = "open" | "pairing" | "allowlist" | "disabled";
export type WecomBotPrimaryTransport = "ws" | "webhook";
/**
 * 长任务进度反馈模式（v2.8.17+）
 * - "progress"（默认）：阶段化心跳文案，按已等待时长升级（思考中 → 处理中(30s) → 任务较复杂(1m) → 仍在执行(2m+)，完成后会主动推送）
 * - "heartbeat"：v2.8.16 及之前的固定"⏳ 正在思考中..."，每 3s 重发，120s 后停
 * - "delayed"：默认沉默；超过 30s（可由 progressDelayedMs 调整）才发 1 条提示，不循环
 * - "off"：完全不发占位（高级用户用，依赖 LLM partial chunk 自身可见性）
 */
export type WecomProgressMode = "progress" | "heartbeat" | "delayed" | "off";

export type WecomDmConfig = {
  policy?: WecomDmPolicy;
  allowFrom?: Array<string | number>;
};

export type WecomMediaConfig = {
  tempDir?: string;
  retentionHours?: number;
  cleanupOnStart?: boolean;
  maxBytes?: number;
  downloadTimeoutMs?: number;
  localRoots?: string[];
};

export type WecomNetworkConfig = {
  egressProxyUrl?: string;
  timeoutMs?: number;
  mediaDownloadTimeoutMs?: number;
};

export type WecomRoutingConfig = {
  failClosedOnDefaultRoute?: boolean;
};

export type WecomBotWsConfig = {
  botId: string;
  secret: string;
};

export type WecomBotWebhookConfig = {
  token: string;
  encodingAESKey: string;
  receiveId?: string;
};

export type WecomBotConfig = {
  primaryTransport?: WecomBotPrimaryTransport;
  streamPlaceholderContent?: string;
  welcomeText?: string;
  /**
   * v2.8.17+：长任务进度反馈模式。默认 "progress"（阶段化文案）。
   * 仅 bot-ws 通道生效；bot-webhook 自有 long-task rescue 机制（v2.8.14）。
   */
  progressMode?: WecomProgressMode;
  /**
   * v2.8.17+：progressMode="delayed" 时，沉默多少毫秒后发提示。默认 30000（30s）。
   */
  progressDelayedMs?: number;
  dm?: WecomDmConfig;
  /**
   * Deprecated compatibility fields kept only while old webhook helpers are
   * being extracted into transport adapters.
   */
  aibotid?: string;
  botIds?: string[];
  ws?: WecomBotWsConfig;
  webhook?: WecomBotWebhookConfig;
};

/**
 * 上下游企业配置
 * 根据企业微信文档，只需要配置下游企业的 CorpID 和 AgentID
 * 不需要下游企业的 agentSecret，使用主企业的 corpSecret 获取下游企业的 access_token
 */
export type WecomUpstreamCorpConfig = {
  corpId: string;
  agentId: number;
};

export type WecomAgentConfig = {
  corpId: string;
  agentSecret?: string;
  /**
   * Deprecated compatibility alias for old configs.
   * New configs should use `agentSecret`.
   */
  corpSecret?: string;
  agentId?: number | string;
  token: string;
  encodingAESKey: string;
  welcomeText?: string;
  dm?: WecomDmConfig;
  /**
   * 上下游企业配置映射
   * key: 配置名称（可自定义）
   * value: 下游企业的 CorpID 和 AgentID
   * 
   * 注意：不需要配置 agentSecret，使用主企业的 corpSecret 获取下游企业的 access_token
   */
  upstreamCorps?: Record<string, WecomUpstreamCorpConfig>;
};

export type WecomDynamicAgentsConfig = {
  enabled?: boolean;
  dmCreateAgent?: boolean;
  groupEnabled?: boolean;
  adminUsers?: string[];
};

export type WecomKefuWebhookConfig = {
  token: string;
  encodingAESKey: string;
};

/**
 * 微信客服（WeCom Kefu）账号配置
 * 对应企业微信"微信客服"产品，用于对接外部微信用户咨询。
 *
 * access_token 复用企业应用（Agent API）：需要 corpId + corpSecret。
 * 允许独立配置（不强依赖同账号下的 agent 段）。
 */
export type WecomKefuConfig = {
  corpId: string;
  corpSecret: string;
  /** 绑定的客服账号 openKfId 列表；允许单账号绑多个客服账号分流 */
  openKfIds: string[];
  webhook: WecomKefuWebhookConfig;
  welcomeText?: string;
  dm?: WecomDmConfig;
};

export type WecomAccountConfig = {
  enabled?: boolean;
  name?: string;
  mediaMaxMb?: number;
  bot?: WecomBotConfig;
  agent?: WecomAgentConfig;
  kefu?: WecomKefuConfig;
};

export type WecomConfig = {
  enabled?: boolean;
  mediaMaxMb?: number;
  mediaDownloadTimeoutMs?: number;
  bot?: WecomBotConfig;
  agent?: WecomAgentConfig;
  kefu?: WecomKefuConfig;
  accounts?: Record<string, WecomAccountConfig>;
  defaultAccount?: string;
  media?: WecomMediaConfig;
  network?: WecomNetworkConfig;
  routing?: WecomRoutingConfig;
  dynamicAgents?: WecomDynamicAgentsConfig;
};
