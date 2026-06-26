/**
 * 微信服务号 ChannelPlugin 装配。
 *
 * 把 config adapter / outbound / gateway lifecycle / setup wizard 串起来，
 * 真正执行逻辑散落在：
 *  - ./config/*         — 账号解析、路径推导
 *  - ./outbound.ts      — 客服消息主动下发
 *  - ./gateway-monitor  — startAccount
 *  - ./onboarding       — 配置向导
 *  - ./transport/webhook/  — webhook inbound
 */

import type {
  ChannelAccountSnapshot,
  ChannelPlugin,
  OpenClawConfig,
} from "openclaw/plugin-sdk";
import {
  deleteAccountFromConfigSection,
  setAccountEnabledInConfigSection,
} from "openclaw/plugin-sdk/core";

import {
  CONFIG_SECTION_KEY,
  DEFAULT_ACCOUNT_ID,
  listWechatServiceAccountIds,
  resolveDefaultWechatServiceAccountId,
  resolveDerivedPathSummary,
  resolveWechatServiceAccount,
  resolveWechatServiceAccountConflict,
} from "./config/index.js";
import { monitorWechatServiceProvider } from "./gateway-monitor.js";
import { wechatServiceSetupAdapter, wechatServiceSetupWizard } from "./onboarding.js";
import { wechatServiceOutbound } from "./outbound.js";
import type { ResolvedWechatServiceAccount } from "./types.js";

const meta = {
  id: "wechat-service",
  label: "微信服务号（公众号）",
  selectionLabel: "微信服务号（公众号）",
  detailLabel: "微信服务号（公众号）",
  docsPath: "/channels/wechat-service",
  docsLabel: "微信服务号",
  blurb: "接入微信服务号/公众号：菜单、客服/模板/订阅消息、图文发布、标签群发、JS-SDK，支持多账号多 Agent 隔离。",
  selectionDocsPrefix: "文档：",
  aliases: ["wechat", "mp", "offiaccount", "服务号", "公众号", "微信公众号"],
  order: 86,
  quickstartAllowFrom: false,
};

function normalizeTarget(raw: string): string | undefined {
  const trimmed = raw.trim();
  if (!trimmed) return undefined;
  const stripped = trimmed
    .replace(/^(wechat-service|wechat|mp|offiaccount|服务号|公众号):(user|direct):/i, "")
    .trim();
  return stripped || trimmed;
}

function resolveAccountWebhookPath(account: ResolvedWechatServiceAccount): string {
  return resolveDerivedPathSummary(account.accountId).primary;
}

export const wechatServicePlugin: ChannelPlugin<ResolvedWechatServiceAccount> = {
  id: "wechat-service",
  meta,
  setupWizard: wechatServiceSetupWizard,
  /**
   * v2.0.0+ —— `setup.applyAccountConfig` 让 CLI `openclaw channels add --channel wechat-service`
   * 能正常工作（v1.x 之前没暴露这个 adapter，CLI 会报 "Channel does not support add."）。
   *
   * 凭据策略：`--name` / `--token` 走 CLI flag；AppID / AppSecret / EncodingAESKey 走环境变量
   * （详见 `onboarding.ts:wechatServiceSetupAdapter`）。
   */
  setup: wechatServiceSetupAdapter,
  capabilities: {
    chatTypes: ["direct"],
    media: true,
    reactions: false,
    threads: false,
    polls: false,
    nativeCommands: false,
    blockStreaming: false,
  },
  reload: { configPrefixes: [`channels.${CONFIG_SECTION_KEY}`] },
  configSchema: {
    schema: {
      type: "object",
      additionalProperties: true,
      properties: {},
    },
  },
  config: {
    listAccountIds: (cfg) => listWechatServiceAccountIds(cfg as OpenClawConfig),
    resolveAccount: (cfg, accountId) =>
      resolveWechatServiceAccount({
        cfg: cfg as OpenClawConfig,
        accountId,
      }),
    defaultAccountId: (cfg) =>
      resolveDefaultWechatServiceAccountId(cfg as OpenClawConfig),
    setAccountEnabled: ({ cfg, accountId, enabled }) =>
      setAccountEnabledInConfigSection({
        cfg: cfg as OpenClawConfig,
        sectionKey: CONFIG_SECTION_KEY,
        accountId,
        enabled,
        allowTopLevel: true,
      }),
    deleteAccount: ({ cfg, accountId }) =>
      deleteAccountFromConfigSection({
        cfg: cfg as OpenClawConfig,
        sectionKey: CONFIG_SECTION_KEY,
        accountId,
      }),
    isConfigured: (account, cfg) => {
      if (!account.configured) return false;
      return !resolveWechatServiceAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      });
    },
    unconfiguredReason: (account, cfg) =>
      resolveWechatServiceAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      })?.message ?? "not configured",
    describeAccount: (account, cfg): ChannelAccountSnapshot => {
      const conflict = resolveWechatServiceAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      });
      return {
        accountId: account.accountId,
        name: account.name,
        enabled: account.enabled,
        configured: account.configured && !conflict,
        webhookPath: resolveAccountWebhookPath(account),
      };
    },
    resolveAllowFrom: ({ cfg, accountId }) => {
      const account = resolveWechatServiceAccount({
        cfg: cfg as OpenClawConfig,
        accountId,
      });
      const allowFrom = account.dm?.allowFrom ?? [];
      return allowFrom.map((entry) => String(entry));
    },
    formatAllowFrom: ({ allowFrom }) =>
      allowFrom
        .map((entry) => String(entry).trim())
        .filter(Boolean)
        .map((entry) => entry.toLowerCase()),
  },
  groups: {
    resolveRequireMention: () => false,
  },
  threading: {
    resolveReplyToMode: () => "off",
  },
  messaging: {
    normalizeTarget,
    targetResolver: {
      looksLikeId: (raw) => Boolean(raw.trim()),
      hint: "<openid>",
    },
  },
  outbound: { ...wechatServiceOutbound },
  status: {
    defaultRuntime: {
      accountId: DEFAULT_ACCOUNT_ID,
      running: false,
      lastStartAt: null,
      lastStopAt: null,
      lastError: null,
    },
    buildChannelSummary: ({ snapshot }) => ({
      configured: snapshot.configured ?? false,
      running: snapshot.running ?? false,
      webhookPath: snapshot.webhookPath ?? null,
      lastStartAt: snapshot.lastStartAt ?? null,
      lastStopAt: snapshot.lastStopAt ?? null,
      lastInboundAt: snapshot.lastInboundAt ?? null,
      lastOutboundAt: snapshot.lastOutboundAt ?? null,
      lastError: snapshot.lastError ?? null,
    }),
    probeAccount: async () => ({ ok: true }),
    buildAccountSnapshot: ({ account, runtime, cfg }) => {
      const conflict = resolveWechatServiceAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      });
      return {
        accountId: account.accountId,
        name: account.name,
        enabled: account.enabled,
        configured: account.configured && !conflict,
        webhookPath: resolveAccountWebhookPath(account),
        running: runtime?.running ?? false,
        lastStartAt: runtime?.lastStartAt ?? null,
        lastStopAt: runtime?.lastStopAt ?? null,
        lastInboundAt: runtime?.lastInboundAt ?? null,
        lastOutboundAt: runtime?.lastOutboundAt ?? null,
        lastError: runtime?.lastError ?? conflict?.message ?? null,
      };
    },
  },
  gateway: {
    startAccount: monitorWechatServiceProvider,
    stopAccount: async (ctx) => {
      ctx.setStatus({
        accountId: ctx.account.accountId,
        running: false,
        lastStopAt: Date.now(),
      });
    },
  },
};
