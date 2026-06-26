import type {
  WecomAccountConfig,
  WecomAgentConfig,
  WecomBotConfig,
  WecomBotPrimaryTransport,
  WecomKefuConfig,
  WecomNetworkConfig,
} from "./config.js";

export type ResolvedMode = "disabled" | "legacy" | "matrix";

export type ResolvedBotWsTransport = {
  botId: string;
  secret: string;
};

export type ResolvedBotWebhookTransport = {
  token: string;
  encodingAESKey: string;
  receiveId: string;
};

export type ResolvedBotAccount = {
  accountId: string;
  configured: boolean;
  primaryTransport: WecomBotPrimaryTransport;
  wsConfigured: boolean;
  webhookConfigured: boolean;
  config: WecomBotConfig;
  network?: WecomNetworkConfig;
  ws?: ResolvedBotWsTransport;
  webhook?: ResolvedBotWebhookTransport;
  // Compatibility flattening for old webhook-centric helpers.
  token: string;
  encodingAESKey: string;
  receiveId: string;
  botId: string;
  secret: string;
};

export type ResolvedAgentAccount = {
  accountId: string;
  configured: boolean;
  callbackConfigured: boolean;
  apiConfigured: boolean;
  corpId: string;
  corpSecret: string;
  agentId?: number;
  token: string;
  encodingAESKey: string;
  config: WecomAgentConfig;
  network?: WecomNetworkConfig;
};

export type ResolvedKefuAccount = {
  accountId: string;
  configured: boolean;
  callbackConfigured: boolean;
  apiConfigured: boolean;
  corpId: string;
  corpSecret: string;
  openKfIds: string[];
  token: string;
  encodingAESKey: string;
  config: WecomKefuConfig;
  network?: WecomNetworkConfig;
};

export type ResolvedWecomAccount = {
  accountId: string;
  name?: string;
  enabled: boolean;
  configured: boolean;
  config: WecomAccountConfig;
  bot?: ResolvedBotAccount;
  agent?: ResolvedAgentAccount;
  kefu?: ResolvedKefuAccount;
};

export type ResolvedWecomAccounts = {
  mode: ResolvedMode;
  defaultAccountId: string;
  accounts: Record<string, ResolvedWecomAccount>;
  bot?: ResolvedBotAccount;
  agent?: ResolvedAgentAccount;
  kefu?: ResolvedKefuAccount;
};
