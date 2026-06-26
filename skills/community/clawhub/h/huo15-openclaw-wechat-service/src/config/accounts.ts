import type { OpenClawConfig } from "openclaw/plugin-sdk";

import type {
  ResolvedMode,
  ResolvedWechatServiceAccount,
  ResolvedWechatServiceAccounts,
  WechatServiceAccountConfig,
  WechatServiceConfig,
  WechatServiceEncryptMode,
  WechatServiceReplyMode,
  WechatServiceRoutingConfig,
} from "../types.js";

export const DEFAULT_ACCOUNT_ID = "default";
/**
 * Config section key —— **必须等于 channel id**（OpenClaw validator 直接拿 `Object.keys(cfg.channels)`
 * 跟 registered channel id 比对，错位就抛 `unknown channel id`）。
 * 历史 bug：v0.1.0 起一直用 `"wechatService"`（camelCase），但 channel id 是 `"wechat-service"`（kebab）。
 * v1.0.1 修正为 kebab，旧配置（`channels.wechatService`）需要迁移成 `channels["wechat-service"]`。
 */
export const CONFIG_SECTION_KEY = "wechat-service" as const;
/** 兼容性常量：v0.1 ~ v1.0.0 使用过的旧 key，仅用于读旧配置时的回退 */
export const LEGACY_CONFIG_SECTION_KEY = "wechatService" as const;

export type WechatServiceAccountConflict = {
  type: "duplicate_appid" | "duplicate_original_id";
  accountId: string;
  ownerAccountId: string;
  message: string;
};

function asString(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function mergeRouting(
  base: WechatServiceRoutingConfig | undefined,
  entry: WechatServiceRoutingConfig | undefined,
): WechatServiceRoutingConfig {
  const merged: WechatServiceRoutingConfig = {
    defaultAgent: entry?.defaultAgent ?? base?.defaultAgent,
    events: {
      ...(base?.events ?? {}),
      ...(entry?.events ?? {}),
    },
    failClosedOnDefaultRoute:
      entry?.failClosedOnDefaultRoute ?? base?.failClosedOnDefaultRoute,
  };
  return merged;
}

function toResolvedAccount(params: {
  accountId: string;
  topLevel: WechatServiceConfig;
  raw: WechatServiceAccountConfig;
}): ResolvedWechatServiceAccount {
  const { accountId, topLevel, raw } = params;
  const appId = asString(raw.appId);
  const appSecret = asString(raw.appSecret);
  const token = asString(raw.token);
  const encodingAESKey = asString(raw.encodingAESKey);
  const originalId = asString(raw.originalId);
  const encryptMode: WechatServiceEncryptMode =
    raw.encryptMode ?? (encodingAESKey ? "safe" : "plain");
  const replyMode: WechatServiceReplyMode = raw.replyMode ?? "async";
  const replyPlaceholderText =
    raw.replyPlaceholderText?.trim() || "收到，正在为你处理...";
  const welcomeText = raw.welcomeText?.trim() || "你好，我是 AI 助手，有什么可以帮你？";
  const routing = mergeRouting(topLevel.routing, raw.routing);
  const network = { ...(topLevel.network ?? {}), ...(raw.network ?? {}) };

  const secureModeReady = encryptMode === "plain" ? true : Boolean(encodingAESKey);
  const configured = Boolean(appId && appSecret && token && secureModeReady);

  return {
    accountId,
    name: raw.name,
    enabled: topLevel.enabled !== false && raw.enabled !== false,
    configured,
    appId,
    appSecret,
    token,
    encodingAESKey,
    encryptMode,
    originalId,
    replyMode,
    replyPlaceholderText,
    welcomeText,
    routing,
    dm: raw.dm,
    knowledgeSync: raw.knowledgeSync ?? topLevel.knowledgeSync,
    network,
    config: raw,
  };
}

export function detectMode(wechat: WechatServiceConfig | undefined): ResolvedMode {
  if (!wechat || wechat.enabled === false) return "disabled";
  if (wechat.accounts && Object.keys(wechat.accounts).length > 0) return "matrix";
  return "disabled";
}

let warnedLegacyKey = false;

function getWechatServiceConfig(cfg: OpenClawConfig): WechatServiceConfig | undefined {
  const channels = cfg.channels as Record<string, unknown> | undefined;
  // 优先读 v1.0.1+ 的正确 key
  const primary = channels?.[CONFIG_SECTION_KEY];
  if (primary !== undefined) {
    return primary as WechatServiceConfig;
  }
  // 兼容性回退：v0.1 ~ v1.0.0 使用过 `wechatService` (camelCase)。
  // 现在 OpenClaw validator 会先拒掉错误的 channel id（unknown channel id: wechatService），
  // 一般走不到这里 —— 但万一调用方用 raw 配置（非 validator 路径），仍兜底读一次并打 warn。
  const legacy = channels?.[LEGACY_CONFIG_SECTION_KEY];
  if (legacy !== undefined) {
    if (!warnedLegacyKey) {
      console.warn(
        `[wechat-service] config key "channels.${LEGACY_CONFIG_SECTION_KEY}" is deprecated since v1.0.1; ` +
          `please rename to "channels.${CONFIG_SECTION_KEY}" (kebab-case must equal channel id). ` +
          `OpenClaw config validator will reject the legacy key.`,
      );
      warnedLegacyKey = true;
    }
    return legacy as WechatServiceConfig;
  }
  return undefined;
}

export function resolveWechatServiceAccounts(
  cfg: OpenClawConfig,
): ResolvedWechatServiceAccounts {
  const topLevel = getWechatServiceConfig(cfg) ?? {};
  const mode = detectMode(topLevel);
  const accounts: Record<string, ResolvedWechatServiceAccount> = {};

  if (mode === "matrix") {
    for (const [rawId, entry] of Object.entries(topLevel.accounts ?? {})) {
      const accountId = rawId.trim();
      if (!accountId || !entry) continue;
      accounts[accountId] = toResolvedAccount({
        accountId,
        topLevel,
        raw: entry,
      });
    }
  }

  const defaultAccountId = resolveDefaultWechatServiceAccountId(cfg);
  return { mode, defaultAccountId, accounts };
}

export function listWechatServiceAccountIds(cfg: OpenClawConfig): string[] {
  const topLevel = getWechatServiceConfig(cfg);
  if (!topLevel?.accounts) return [];
  return Object.keys(topLevel.accounts)
    .map((value) => value.trim())
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b));
}

export function resolveDefaultWechatServiceAccountId(cfg: OpenClawConfig): string {
  const topLevel = getWechatServiceConfig(cfg);
  const ids = listWechatServiceAccountIds(cfg);
  if (topLevel?.defaultAccount && ids.includes(topLevel.defaultAccount)) {
    return topLevel.defaultAccount;
  }
  return ids[0] ?? DEFAULT_ACCOUNT_ID;
}

export function resolveWechatServiceAccount(params: {
  cfg: OpenClawConfig;
  accountId?: string | null;
}): ResolvedWechatServiceAccount {
  const resolved = resolveWechatServiceAccounts(params.cfg);
  const explicitAccountId = params.accountId?.trim();
  const accountId = explicitAccountId || resolved.defaultAccountId;
  const direct = resolved.accounts[accountId];
  if (direct) return direct;

  if (explicitAccountId === DEFAULT_ACCOUNT_ID) {
    const fallback = resolved.accounts[resolved.defaultAccountId];
    if (fallback) return fallback;
  }

  return {
    accountId,
    enabled: false,
    configured: false,
    appId: "",
    appSecret: "",
    token: "",
    encodingAESKey: "",
    encryptMode: "plain",
    originalId: "",
    replyMode: "async",
    replyPlaceholderText: "收到，正在为你处理...",
    welcomeText: "你好，我是 AI 助手，有什么可以帮你？",
    routing: {},
    config: {
      appId: "",
      appSecret: "",
      token: "",
    },
  };
}

export function resolveWechatServiceAccountConflict(params: {
  cfg: OpenClawConfig;
  accountId: string;
}): WechatServiceAccountConflict | undefined {
  const resolved = resolveWechatServiceAccounts(params.cfg);
  const appIdOwners = new Map<string, string>();
  const originalIdOwners = new Map<string, string>();

  const sortedIds = Object.keys(resolved.accounts).sort((a, b) => a.localeCompare(b));
  for (const id of sortedIds) {
    const account = resolved.accounts[id];
    if (!account || !account.enabled) continue;
    const appIdKey = account.appId.trim().toLowerCase();
    if (appIdKey) {
      const owner = appIdOwners.get(appIdKey);
      if (owner && owner !== id && id === params.accountId) {
        return {
          type: "duplicate_appid",
          accountId: id,
          ownerAccountId: owner,
          message: `Duplicate WeChat Service appId: account "${id}" shares appId with account "${owner}". Keep one owner per appId.`,
        };
      }
      if (!owner) appIdOwners.set(appIdKey, id);
    }
    const originalKey = account.originalId.trim().toLowerCase();
    if (originalKey) {
      const owner = originalIdOwners.get(originalKey);
      if (owner && owner !== id && id === params.accountId) {
        return {
          type: "duplicate_original_id",
          accountId: id,
          ownerAccountId: owner,
          message: `Duplicate WeChat Service originalId: account "${id}" shares originalId with account "${owner}".`,
        };
      }
      if (!owner) originalIdOwners.set(originalKey, id);
    }
  }
  return undefined;
}

export function isWechatServiceEnabled(cfg: OpenClawConfig): boolean {
  const resolved = resolveWechatServiceAccounts(cfg);
  return Object.values(resolved.accounts).some((a) => a.enabled && a.configured);
}
