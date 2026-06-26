import type { ChannelAccountSnapshot, ChannelPlugin, OpenClawConfig } from "openclaw/plugin-sdk";
import {
  deleteAccountFromConfigSection,
  setAccountEnabledInConfigSection,
} from "openclaw/plugin-sdk/core";
import {
  DEFAULT_ACCOUNT_ID,
  listWecomAccountIds,
  resolveDerivedPathSummary,
  resolveDefaultWecomAccountId,
  resolveWecomAccount,
  resolveWecomAccountConflict,
} from "./config/index.js";
import { monitorWecomProvider } from "./gateway-monitor.js";
import { wecomSetupWizard } from "./onboarding.js";
import { wecomOutbound } from "./outbound.js";
import type { ResolvedWecomAccount } from "./types/index.js";

const meta = {
  id: "wecom",
  label: "WeCom (企业微信)",
  selectionLabel: "WeCom (企业微信)",
  docsPath: "/channels/wecom",
  docsLabel: "企业微信",
  blurb: "企业微信官方推荐三方插件，默认 Bot WS 配置简单，支持主动发消息与 Agent 全能力。",
  selectionDocsPrefix: "文档：",
  aliases: ["wechatwork", "wework", "qywx", "企微", "企业微信"],
  order: 85,
  quickstartAllowFrom: true,
};

function resolveAccountInboundPath(account: ResolvedWecomAccount): string | undefined {
  const derivedPaths = resolveDerivedPathSummary(account.accountId);
  if (account.bot?.primaryTransport === "webhook" && account.bot.webhookConfigured) {
    return derivedPaths.botWebhook[0];
  }
  if (account.agent?.callbackConfigured) {
    return derivedPaths.agentCallback[0];
  }
  if (account.kefu?.callbackConfigured) {
    return derivedPaths.kefu[0];
  }
  return undefined;
}

function normalizeWecomMessagingTarget(raw: string): string | undefined {
  const trimmed = raw.trim();
  if (!trimmed) return undefined;
  if (/^wecom-agent(?:-upstream)?:/i.test(trimmed)) {
    return trimmed;
  }
  if (/^(wecom|wechatwork|wework|qywx):(user|group|chat|party|dept|tag|context):/i.test(trimmed)) {
    return trimmed;
  }
  return trimmed.replace(/^(wecom|wechatwork|wework|qywx):/i, "").trim() || undefined;
}

export const wecomPlugin: ChannelPlugin<ResolvedWecomAccount> = {
  id: "wecom",
  meta,
  setupWizard: wecomSetupWizard,
  capabilities: {
    chatTypes: ["direct", "group"],
    media: true,
    reactions: false,
    threads: false,
    polls: false,
    nativeCommands: false,
    blockStreaming: false,
  },
  reload: { configPrefixes: ["channels.wecom"] },
  // A permissive schema keeps config UX working while preventing startup failures.
  configSchema: {
    schema: {
      type: "object",
      additionalProperties: true,
      properties: {},
    },
  },
  config: {
    listAccountIds: (cfg) => listWecomAccountIds(cfg as OpenClawConfig),
    resolveAccount: (cfg, accountId) =>
      resolveWecomAccount({ cfg: cfg as OpenClawConfig, accountId }),
    defaultAccountId: (cfg) => resolveDefaultWecomAccountId(cfg as OpenClawConfig),
    setAccountEnabled: ({ cfg, accountId, enabled }) =>
      setAccountEnabledInConfigSection({
        cfg: cfg as OpenClawConfig,
        sectionKey: "wecom",
        accountId,
        enabled,
        allowTopLevel: true,
      }),
    deleteAccount: ({ cfg, accountId }) =>
      deleteAccountFromConfigSection({
        cfg: cfg as OpenClawConfig,
        sectionKey: "wecom",
        accountId,
        clearBaseFields: ["bot", "agent", "kefu"],
      }),
    isConfigured: (account, cfg) => {
      if (!account.configured) {
        return false;
      }
      return !resolveWecomAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      });
    },
    unconfiguredReason: (account, cfg) =>
      resolveWecomAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      })?.message ?? "not configured",
    describeAccount: (account, cfg): ChannelAccountSnapshot => {
      const conflict = resolveWecomAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      });
      return {
        accountId: account.accountId,
        name: account.name,
        enabled: account.enabled,
        configured: account.configured && !conflict,
        webhookPath: resolveAccountInboundPath(account),
      };
    },
    resolveAllowFrom: ({ cfg, accountId }) => {
      const account = resolveWecomAccount({
        cfg: cfg as OpenClawConfig,
        accountId,
      });
      // 与其他渠道保持一致：直接返回 allowFrom，空则允许所有人
      const allowFrom =
        account.agent?.config.dm?.allowFrom ?? account.bot?.config.dm?.allowFrom ?? [];
      return allowFrom.map((entry) => String(entry));
    },
    formatAllowFrom: ({ allowFrom }) =>
      allowFrom
        .map((entry) => String(entry).trim())
        .filter(Boolean)
        .map((entry) => entry.toLowerCase()),
  },
  // security 配置在 WeCom 中不需要，框架会通过 resolveAllowFrom 自动判断
  groups: {
    // WeCom bots are usually mention-gated by the platform in groups already.
    // Set to false so the framework doesn't inject "trigger-only" activation
    // prompt that causes the LLM to stay silent in group chats.
    resolveRequireMention: () => false,
  },
  threading: {
    resolveReplyToMode: () => "off",
  },
  messaging: {
    normalizeTarget: normalizeWecomMessagingTarget,
    targetResolver: {
      looksLikeId: (raw) => Boolean(raw.trim()),
      hint: "<userid|chatid>",
    },
  },
  outbound: {
    ...wecomOutbound,
  },
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
      transport: (snapshot as { transport?: string }).transport ?? null,
      ownerId: (snapshot as { ownerId?: string }).ownerId ?? null,
      health: (snapshot as { health?: string }).health ?? "idle",
      ownerDriftAt: (snapshot as { ownerDriftAt?: number | null }).ownerDriftAt ?? null,
      connected: (snapshot as { connected?: boolean }).connected,
      authenticated: (snapshot as { authenticated?: boolean }).authenticated,
      lastStartAt: snapshot.lastStartAt ?? null,
      lastStopAt: snapshot.lastStopAt ?? null,
      lastError: snapshot.lastError ?? null,
      lastErrorAt: (snapshot as { lastErrorAt?: number | null }).lastErrorAt ?? null,
      lastInboundAt: snapshot.lastInboundAt ?? null,
      lastOutboundAt: snapshot.lastOutboundAt ?? null,
      recentInboundSummary:
        (snapshot as { recentInboundSummary?: string | null }).recentInboundSummary ?? null,
      recentOutboundSummary:
        (snapshot as { recentOutboundSummary?: string | null }).recentOutboundSummary ?? null,
      recentIssueCategory:
        (snapshot as { recentIssueCategory?: string | null }).recentIssueCategory ?? null,
      recentIssueSummary:
        (snapshot as { recentIssueSummary?: string | null }).recentIssueSummary ?? null,
      transportSessions: (snapshot as { transportSessions?: string[] }).transportSessions ?? [],
      probe: snapshot.probe,
      lastProbeAt: snapshot.lastProbeAt ?? null,
    }),
    probeAccount: async () => ({ ok: true }),
    buildAccountSnapshot: ({ account, runtime, cfg }) => {
      const conflict = resolveWecomAccountConflict({
        cfg: cfg as OpenClawConfig,
        accountId: account.accountId,
      });
      return {
        accountId: account.accountId,
        name: account.name,
        enabled: account.enabled,
        configured: account.configured && !conflict,
        webhookPath: resolveAccountInboundPath(account),
        primaryTransport:
          account.bot?.primaryTransport ?? (account.agent ? "agent-callback" : null),
        transport: (runtime as { transport?: string } | undefined)?.transport ?? null,
        ownerId: (runtime as { ownerId?: string } | undefined)?.ownerId ?? null,
        health: (runtime as { health?: string } | undefined)?.health ?? "idle",
        ownerDriftAt:
          (runtime as { ownerDriftAt?: number | null } | undefined)?.ownerDriftAt ?? null,
        connected: (runtime as { connected?: boolean } | undefined)?.connected,
        authenticated: (runtime as { authenticated?: boolean } | undefined)?.authenticated,
        running: runtime?.running ?? false,
        lastStartAt: runtime?.lastStartAt ?? null,
        lastStopAt: runtime?.lastStopAt ?? null,
        lastError: runtime?.lastError ?? conflict?.message ?? null,
        lastErrorAt: (runtime as { lastErrorAt?: number | null } | undefined)?.lastErrorAt ?? null,
        lastInboundAt: runtime?.lastInboundAt ?? null,
        lastOutboundAt: runtime?.lastOutboundAt ?? null,
        recentInboundSummary:
          (runtime as { recentInboundSummary?: string | null } | undefined)?.recentInboundSummary ??
          null,
        recentOutboundSummary:
          (runtime as { recentOutboundSummary?: string | null } | undefined)
            ?.recentOutboundSummary ?? null,
        recentIssueCategory:
          (runtime as { recentIssueCategory?: string | null } | undefined)?.recentIssueCategory ??
          null,
        recentIssueSummary:
          (runtime as { recentIssueSummary?: string | null } | undefined)?.recentIssueSummary ??
          null,
        transportSessions:
          (runtime as { transportSessions?: string[] } | undefined)?.transportSessions ?? [],
        dmPolicy: account.bot?.config.dm?.policy ?? "pairing",
      };
    },
  },
  gateway: {
    /**
     * **startAccount (启动账号)**
     *
     * WeCom lifecycle is long-running: keep webhook targets active until
     * gateway stop/reload aborts the account.
     */
    startAccount: monitorWecomProvider,
    stopAccount: async (ctx) => {
      ctx.setStatus({
        accountId: ctx.account.accountId,
        running: false,
        lastStopAt: Date.now(),
      });
    },
  },
};
