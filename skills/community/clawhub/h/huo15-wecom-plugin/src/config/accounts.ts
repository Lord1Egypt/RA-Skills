import type { OpenClawConfig } from "openclaw/plugin-sdk";

import type {
  ResolvedAgentAccount,
  ResolvedBotAccount,
  ResolvedKefuAccount,
  ResolvedMode,
  ResolvedWecomAccount,
  ResolvedWecomAccounts,
  WecomAccountConfig,
  WecomAgentConfig,
  WecomBotConfig,
  WecomConfig,
  WecomKefuConfig,
  WecomNetworkConfig,
} from "../types/index.js";

export const DEFAULT_ACCOUNT_ID = "default";

export type WecomAccountConflict = {
  type: "duplicate_bot_id" | "duplicate_agent_id" | "duplicate_kefu_id";
  accountId: string;
  ownerAccountId: string;
  message: string;
};

function toNumber(value: number | string | undefined): number | undefined {
  if (value == null) return undefined;
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : undefined;
}

function resolveBotAccount(
  accountId: string,
  config: WecomBotConfig,
  network?: WecomNetworkConfig,
): ResolvedBotAccount {
  const primaryTransport = config.primaryTransport ?? (config.ws ? "ws" : "webhook");
  const wsConfigured = Boolean(config.ws?.botId && config.ws?.secret);
  const webhookConfigured = Boolean(config.webhook?.token && config.webhook?.encodingAESKey);
  const configured = primaryTransport === "ws" ? wsConfigured : webhookConfigured;
  return {
    accountId,
    configured,
    primaryTransport,
    wsConfigured,
    webhookConfigured,
    config,
    network,
    ws: config.ws
      ? {
          botId: config.ws.botId,
          secret: config.ws.secret,
        }
      : undefined,
    webhook: config.webhook
      ? {
          token: config.webhook.token,
          encodingAESKey: config.webhook.encodingAESKey,
          receiveId: config.webhook.receiveId?.trim() ?? "",
        }
      : undefined,
    token: config.webhook?.token ?? "",
    encodingAESKey: config.webhook?.encodingAESKey ?? "",
    receiveId: config.webhook?.receiveId?.trim() ?? "",
    botId: config.ws?.botId ?? "",
    secret: config.ws?.secret ?? "",
  };
}

function resolveAgentAccount(
  accountId: string,
  config: WecomAgentConfig,
  network?: WecomNetworkConfig,
): ResolvedAgentAccount {
  const agentId = toNumber(config.agentId);
  const callbackConfigured = Boolean(config.token && config.encodingAESKey);
  const normalizedAgentSecret = config.agentSecret?.trim() || config.corpSecret?.trim() || "";
  const apiConfigured = Boolean(config.corpId && normalizedAgentSecret && agentId);
  return {
    accountId,
    configured: callbackConfigured || apiConfigured,
    callbackConfigured,
    apiConfigured,
    corpId: config.corpId,
    corpSecret: normalizedAgentSecret,
    agentId,
    token: config.token,
    encodingAESKey: config.encodingAESKey,
    config,
    network,
  };
}

function resolveKefuAccount(
  accountId: string,
  config: WecomKefuConfig,
  network?: WecomNetworkConfig,
): ResolvedKefuAccount {
  const openKfIds = (config.openKfIds ?? [])
    .map((id) => String(id ?? "").trim())
    .filter(Boolean);
  const callbackConfigured = Boolean(config.webhook?.token && config.webhook?.encodingAESKey);
  const apiConfigured = Boolean(config.corpId?.trim() && config.corpSecret?.trim());
  return {
    accountId,
    configured: (callbackConfigured || apiConfigured) && openKfIds.length > 0,
    callbackConfigured,
    apiConfigured,
    corpId: config.corpId?.trim() ?? "",
    corpSecret: config.corpSecret?.trim() ?? "",
    openKfIds,
    token: config.webhook?.token ?? "",
    encodingAESKey: config.webhook?.encodingAESKey ?? "",
    config,
    network,
  };
}

function toResolvedAccount(params: {
  accountId: string;
  enabled: boolean;
  name?: string;
  config: WecomAccountConfig;
  network?: WecomNetworkConfig;
}): ResolvedWecomAccount {
  const bot = params.config.bot
    ? resolveBotAccount(params.accountId, params.config.bot, params.network)
    : undefined;
  const agent = params.config.agent
    ? resolveAgentAccount(params.accountId, params.config.agent, params.network)
    : undefined;
  const kefu = params.config.kefu
    ? resolveKefuAccount(params.accountId, params.config.kefu, params.network)
    : undefined;
  return {
    accountId: params.accountId,
    name: params.name,
    enabled: params.enabled,
    configured: Boolean(bot?.configured || agent?.configured || kefu?.configured),
    config: params.config,
    bot,
    agent,
    kefu,
  };
}

function createMissingResolvedAccount(accountId: string): ResolvedWecomAccount {
  return {
    accountId,
    enabled: false,
    configured: false,
    config: {},
  };
}

export function detectMode(config: WecomConfig | undefined): ResolvedMode {
  if (!config || config.enabled === false) return "disabled";
  if (config.accounts && Object.keys(config.accounts).length > 0) {
    return "matrix";
  }
  if (config.bot || config.agent || config.kefu) {
    return "legacy";
  }
  return "disabled";
}

function resolveMatrixAccounts(wecom: WecomConfig): Record<string, ResolvedWecomAccount> {
  const resolved: Record<string, ResolvedWecomAccount> = {};
  for (const [rawId, entry] of Object.entries(wecom.accounts ?? {})) {
    const accountId = rawId.trim();
    if (!accountId || !entry) continue;
    resolved[accountId] = toResolvedAccount({
      accountId,
      enabled: wecom.enabled !== false && entry.enabled !== false,
      name: entry.name,
      config: entry,
      network: wecom.network,
    });
  }
  return resolved;
}

function resolveLegacyAccounts(wecom: WecomConfig): Record<string, ResolvedWecomAccount> {
  const config: WecomAccountConfig = {
    bot: wecom.bot,
    agent: wecom.agent,
    kefu: wecom.kefu,
  };
  return {
    [DEFAULT_ACCOUNT_ID]: toResolvedAccount({
      accountId: DEFAULT_ACCOUNT_ID,
      enabled: wecom.enabled !== false,
      config,
      network: wecom.network,
    }),
  };
}

function normalizeKey(value: string): string {
  return value.trim().toLowerCase();
}

function collectWecomAccountConflicts(cfg: OpenClawConfig): Map<string, WecomAccountConflict> {
  const resolved = resolveWecomAccounts(cfg);
  const conflicts = new Map<string, WecomAccountConflict>();
  const botOwners = new Map<string, string>();
  const agentOwners = new Map<string, string>();
  const kefuOwners = new Map<string, string>();

  for (const accountId of Object.keys(resolved.accounts).sort((a, b) => a.localeCompare(b))) {
    const account = resolved.accounts[accountId];
    if (!account || account.enabled === false) continue;

    const botId = account.bot?.botId?.trim();
    if (botId) {
      const key = normalizeKey(botId);
      const owner = botOwners.get(key);
      if (owner && owner !== accountId) {
        conflicts.set(accountId, {
          type: "duplicate_bot_id",
          accountId,
          ownerAccountId: owner,
          message:
            `Duplicate WeCom botId: account "${accountId}" shares botId with account "${owner}". ` +
            "Keep one owner account per botId.",
        });
      } else {
        botOwners.set(key, accountId);
      }
    }

    const corpId = account.agent?.corpId?.trim();
    const agentId = account.agent?.agentId;
    if (corpId && typeof agentId === "number") {
      const key = `${normalizeKey(corpId)}:${agentId}`;
      const owner = agentOwners.get(key);
      if (owner && owner !== accountId) {
        conflicts.set(accountId, {
          type: "duplicate_agent_id",
          accountId,
          ownerAccountId: owner,
          message:
            `Duplicate WeCom agent identity: account "${accountId}" shares corpId/agentId (${corpId}/${agentId}) with account "${owner}". ` +
            "Keep one owner account per corpId/agentId pair.",
        });
      } else {
        agentOwners.set(key, accountId);
      }
    }

    for (const rawKfId of account.kefu?.openKfIds ?? []) {
      const kfId = rawKfId.trim();
      if (!kfId) continue;
      const key = normalizeKey(kfId);
      const owner = kefuOwners.get(key);
      if (owner && owner !== accountId) {
        conflicts.set(accountId, {
          type: "duplicate_kefu_id",
          accountId,
          ownerAccountId: owner,
          message:
            `Duplicate WeCom kefu openKfId: account "${accountId}" shares openKfId "${kfId}" with account "${owner}". ` +
            "Keep one owner account per openKfId.",
        });
      } else {
        kefuOwners.set(key, accountId);
      }
    }
  }

  return conflicts;
}

export function resolveWecomAccountConflict(params: {
  cfg: OpenClawConfig;
  accountId: string;
}): WecomAccountConflict | undefined {
  return collectWecomAccountConflicts(params.cfg).get(params.accountId);
}

export function listWecomAccountIds(cfg: OpenClawConfig): string[] {
  const wecom = cfg.channels?.wecom as WecomConfig | undefined;
  const mode = detectMode(wecom);
  if (mode === "matrix") {
    return Object.keys(wecom?.accounts ?? {})
      .map((value) => value.trim())
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b));
  }
  if (mode === "legacy") {
    return [DEFAULT_ACCOUNT_ID];
  }
  return [];
}

export function resolveDefaultWecomAccountId(cfg: OpenClawConfig): string {
  const wecom = cfg.channels?.wecom as WecomConfig | undefined;
  const ids = listWecomAccountIds(cfg);
  if (wecom?.defaultAccount && ids.includes(wecom.defaultAccount)) {
    return wecom.defaultAccount;
  }
  return ids[0] ?? DEFAULT_ACCOUNT_ID;
}

export function resolveWecomAccounts(cfg: OpenClawConfig): ResolvedWecomAccounts {
  const wecom = (cfg.channels?.wecom as WecomConfig | undefined) ?? {};
  const mode = detectMode(wecom);
  const accounts = mode === "matrix" ? resolveMatrixAccounts(wecom) : mode === "legacy" ? resolveLegacyAccounts(wecom) : {};
  const defaultAccountId = resolveDefaultWecomAccountId(cfg);
  return {
    mode,
    defaultAccountId,
    accounts,
    bot: accounts[defaultAccountId]?.bot,
    agent: accounts[defaultAccountId]?.agent,
    kefu: accounts[defaultAccountId]?.kefu,
  };
}

export function resolveWecomAccount(params: {
  cfg: OpenClawConfig;
  accountId?: string | null;
}): ResolvedWecomAccount {
  const resolved = resolveWecomAccounts(params.cfg);
  const explicitAccountId = params.accountId?.trim();
  const accountId = explicitAccountId || resolved.defaultAccountId;
  const direct = resolved.accounts[accountId];
  if (direct) {
    return direct;
  }

  // Treat the literal "default" as an alias for the configured default account.
  // This keeps generic onboarding flows working even when the first WeCom account
  // was created under a custom id like "haidao" instead of a literal "default".
  if (explicitAccountId === DEFAULT_ACCOUNT_ID) {
    const fallback = resolved.accounts[resolved.defaultAccountId];
    if (fallback) {
      return fallback;
    }
  }

  return createMissingResolvedAccount(accountId);
}

export function isWecomEnabled(cfg: OpenClawConfig): boolean {
  const resolved = resolveWecomAccounts(cfg);
  return Object.values(resolved.accounts).some((account) => account.enabled && account.configured);
}
