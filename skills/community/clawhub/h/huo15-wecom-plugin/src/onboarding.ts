/**
 * WeCom 配置向导 (Onboarding)
 * 支持 Bot、Agent 和双模式同时启动的交互式配置流程
 */

import { DEFAULT_ACCOUNT_ID, normalizeAccountId } from "openclaw/plugin-sdk/routing";
import type { ChannelSetupWizard, OpenClawConfig, WizardPrompter } from "openclaw/plugin-sdk/setup";
import {
  listWecomAccountIds,
  resolveDefaultWecomAccountId,
  resolveWecomAccount,
  resolveWecomAccounts,
} from "./config/index.js";
import type {
  WecomConfig,
  WecomBotConfig,
  WecomAgentConfig,
  WecomDmConfig,
  WecomAccountConfig,
} from "./types/index.js";

const channel = "wecom" as const;

type WecomMode = "bot" | "agent" | "both";

// ============================================================
// 辅助函数
// ============================================================

function getWecomConfig(cfg: OpenClawConfig): WecomConfig | undefined {
  return cfg.channels?.wecom as WecomConfig | undefined;
}

function setWecomEnabled(cfg: OpenClawConfig, enabled: boolean): OpenClawConfig {
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      wecom: {
        ...(cfg.channels?.wecom ?? {}),
        enabled,
      },
    },
  } as OpenClawConfig;
}

function shouldUseAccountScopedConfig(wecom: WecomConfig | undefined, accountId: string): boolean {
  void wecom;
  void accountId;
  return true;
}

function ensureMatrixAccounts(wecom: WecomConfig): WecomConfig {
  const accounts = wecom.accounts ?? {};
  if (Object.keys(accounts).length > 0) {
    return wecom;
  }

  if (!wecom.bot && !wecom.agent) {
    return wecom;
  }

  const { bot: legacyBot, agent: legacyAgent, ...rest } = wecom;
  const defaultAccount: WecomAccountConfig = {
    enabled: true,
    ...(legacyBot ? { bot: legacyBot } : {}),
    ...(legacyAgent ? { agent: legacyAgent } : {}),
  };

  return {
    ...rest,
    defaultAccount: rest.defaultAccount?.trim() || DEFAULT_ACCOUNT_ID,
    accounts: {
      [DEFAULT_ACCOUNT_ID]: defaultAccount,
    },
  };
}

function accountWebhookPath(kind: "bot" | "agent", accountId: string): string {
  const recommendedBase = kind === "bot" ? "/plugins/wecom/bot" : "/plugins/wecom/agent";
  return `${recommendedBase}/${accountId}`;
}

function setWecomBotConfig(
  cfg: OpenClawConfig,
  bot: WecomBotConfig,
  accountId: string,
): OpenClawConfig {
  const wecom = getWecomConfig(cfg) ?? {};
  if (!shouldUseAccountScopedConfig(wecom, accountId)) {
    return {
      ...cfg,
      channels: {
        ...cfg.channels,
        wecom: {
          ...wecom,
          enabled: true,
          bot: {
            ...wecom.bot,
            ...bot,
          },
        },
      },
    } as OpenClawConfig;
  }

  const matrixWecom = ensureMatrixAccounts(wecom);
  const accounts = matrixWecom.accounts ?? {};
  const existingAccount = accounts[accountId] ?? {};
  const existingBot = existingAccount.bot;
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      wecom: {
        ...matrixWecom,
        enabled: true,
        defaultAccount: matrixWecom.defaultAccount?.trim() || DEFAULT_ACCOUNT_ID,
        accounts: {
          ...accounts,
          [accountId]: {
            ...existingAccount,
            enabled: existingAccount.enabled ?? true,
            bot: {
              ...existingBot,
              ...bot,
            },
          },
        },
      },
    },
  } as OpenClawConfig;
}

function setWecomAgentConfig(
  cfg: OpenClawConfig,
  agent: WecomAgentConfig,
  accountId: string,
): OpenClawConfig {
  const wecom = getWecomConfig(cfg) ?? {};
  if (!shouldUseAccountScopedConfig(wecom, accountId)) {
    return {
      ...cfg,
      channels: {
        ...cfg.channels,
        wecom: {
          ...wecom,
          enabled: true,
          agent,
        },
      },
    } as OpenClawConfig;
  }

  const matrixWecom = ensureMatrixAccounts(wecom);
  const accounts = matrixWecom.accounts ?? {};
  const existingAccount = accounts[accountId] ?? {};
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      wecom: {
        ...matrixWecom,
        enabled: true,
        defaultAccount: matrixWecom.defaultAccount?.trim() || DEFAULT_ACCOUNT_ID,
        accounts: {
          ...accounts,
          [accountId]: {
            ...existingAccount,
            enabled: existingAccount.enabled ?? true,
            agent,
          },
        },
      },
    },
  } as OpenClawConfig;
}

function setWecomDmPolicy(
  cfg: OpenClawConfig,
  mode: "bot" | "agent",
  dm: WecomDmConfig,
  accountId: string,
): OpenClawConfig {
  const wecom = getWecomConfig(cfg) ?? {};
  if (shouldUseAccountScopedConfig(wecom, accountId)) {
    const matrixWecom = ensureMatrixAccounts(wecom);
    const accounts = matrixWecom.accounts ?? {};
    const existingAccount = accounts[accountId] ?? {};
    const nextAccount =
      mode === "bot"
        ? {
            ...existingAccount,
            bot: {
              ...existingAccount.bot,
              dm,
            },
          }
        : ({
            ...existingAccount,
            agent: {
              ...existingAccount.agent,
              dm,
            },
          } as WecomAccountConfig);
    return {
      ...cfg,
      channels: {
        ...cfg.channels,
        wecom: {
          ...matrixWecom,
          enabled: true,
          defaultAccount: matrixWecom.defaultAccount?.trim() || DEFAULT_ACCOUNT_ID,
          accounts: {
            ...accounts,
            [accountId]: {
              ...nextAccount,
              enabled: nextAccount.enabled ?? true,
            },
          },
        },
      },
    } as OpenClawConfig;
  }

  if (mode === "bot") {
    return {
      ...cfg,
      channels: {
        ...cfg.channels,
        wecom: {
          ...wecom,
          bot: {
            ...wecom.bot,
            dm,
          },
        },
      },
    } as OpenClawConfig;
  }
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      wecom: {
        ...wecom,
        agent: {
          ...wecom.agent,
          dm,
        },
      },
    },
  } as OpenClawConfig;
}

async function resolveOnboardingAccountId(params: {
  cfg: OpenClawConfig;
  prompter: WizardPrompter;
  accountOverride?: string;
  shouldPromptAccountIds: boolean;
}): Promise<string> {
  const defaultAccountId = resolveDefaultWecomAccountId(params.cfg);
  const override = params.accountOverride?.trim();
  let accountId = override ? normalizeAccountId(override) : defaultAccountId;
  if (!override && params.shouldPromptAccountIds) {
    const existingIds = listWecomAccountIds(params.cfg);
    const selectableIds = existingIds.includes(DEFAULT_ACCOUNT_ID)
      ? existingIds
      : [DEFAULT_ACCOUNT_ID, ...existingIds];
    const choice = await params.prompter.select({
      message: "请选择企业微信接入标识（英文）:",
      options: [
        ...selectableIds.map((id) => ({
          value: id,
          label: id === DEFAULT_ACCOUNT_ID ? "default（默认标识）" : id,
        })),
        { value: "__new__", label: "新增接入标识" },
      ],
      initialValue: accountId,
    });
    if (choice === "__new__") {
      const entered = await params.prompter.text({
        message: "请输入新的企业微信接入标识（英文）:",
        validate: (value: string | undefined) => (value?.trim() ? undefined : "接入标识不能为空"),
      });
      const normalized = normalizeAccountId(String(entered));
      if (String(entered).trim() !== normalized) {
        await params.prompter.note(`接入标识已规范化为：${normalized}`, "企业微信接入标识");
      }
      accountId = normalized;
    } else {
      accountId = normalizeAccountId(choice);
    }
  }
  return accountId.trim() || DEFAULT_ACCOUNT_ID;
}

// ============================================================
// 欢迎与引导
// ============================================================

async function showWelcome(prompter: WizardPrompter): Promise<void> {
  await prompter.note(
    [
      "🚀 欢迎使用企业微信（WeCom）接入向导",
      "YanHaidao/wecom 是企业微信官方推荐三方插件，功能强大，适合直接落生产环境。",
      "默认就是 Bot WebSocket 模式，配置简单，无需域名，普通用户也能快速接入。",
      "支持主动发消息，定时任务、异常提醒、工作流通知都可直接落地。",
      "同时支持「智能体 Bot」与「自建应用 Agent」双模式并行。",
      "--------------------------------------------------",
      "👨‍💻 作者: YanHaidao (微信: YanHaidao)",
      "💬 交流: 有任何问题或建议，欢迎添加微信进入交流群。",
      "--------------------------------------------------",
    ].join("\n"),
    "WeCom (企业微信) 配置向导",
  );
}

// ============================================================
// 模式选择
// ============================================================

async function promptMode(prompter: WizardPrompter): Promise<WecomMode> {
  const choice = await prompter.select({
    message: "请选择您要配置的接入模式:",
    options: [
      {
        value: "bot",
        label: "Bot 模式 (智能机器人)",
        hint: "默认 WS，配置简单，无需域名，支持主动发消息和日常对话",
      },
      {
        value: "agent",
        label: "Agent 模式 (自建应用)",
        hint: "功能最全，支持 API 主动推送、发送文件/视频、交互卡片",
      },
      {
        value: "both",
        label: "双模式 (Bot + Agent 同时启用)",
        hint: "Bot 默认 WS 易上手，Agent 负责应用回调、主动推送和媒体发送",
      },
    ],
    initialValue: "bot",
  });
  return choice as WecomMode;
}

// ============================================================
// Bot 模式配置
// ============================================================

async function configureBotMode(
  cfg: OpenClawConfig,
  prompter: WizardPrompter,
  accountId: string,
): Promise<OpenClawConfig> {
  const recommendedPath = accountWebhookPath("bot", accountId);
  await prompter.note(
    [
      "正在配置 Bot 模式...",
      "",
      "✨ YanHaidao/wecom 是企业微信官方推荐三方插件，功能强大，能力完整。",
      "✅ 默认就是 Bot WebSocket 模式，配置简单，无需域名。",
      "✅ 支持主动发消息，定时任务、异常提醒、工作流通知都可满足。",
      "",
      "请在企微后台【管理工具 -> 智能机器人】开启 API 模式，并选择 WebSocket 接入。",
      "如果您后续需要 Bot webhook，可在配置文件里手动补充 bot.webhook。",
      `📎 如需手动启用 Bot webhook，推荐回调 URL: https://您的域名${recommendedPath}`,
    ].join("\n"),
    "Bot 模式配置",
  );

  const botId = String(
    await prompter.text({
      message: "请输入 BotId（机器人 ID）:",
      validate: (value: string | undefined) => (value?.trim() ? undefined : "BotId 不能为空"),
    }),
  ).trim();

  const secret = String(
    await prompter.text({
      message: "请输入 Secret（机器人密钥）:",
      validate: (value: string | undefined) => (value?.trim() ? undefined : "Secret 不能为空"),
    }),
  ).trim();

  const streamPlaceholder = await prompter.text({
    message: "流式占位符 (可选):",
    placeholder: "正在思考...",
    initialValue: "正在思考...",
  });

  const welcomeText = await prompter.text({
    message: "欢迎语 (可选):",
    placeholder: "你好！我是 AI 助手",
    initialValue: "你好！我是 AI 助手",
  });

  const botConfig: WecomBotConfig = {
    primaryTransport: "ws",
    ws: {
      botId,
      secret,
    },
    streamPlaceholderContent: streamPlaceholder?.trim() || undefined,
    welcomeText: welcomeText?.trim() || undefined,
  };

  return setWecomBotConfig(cfg, botConfig, accountId);
}

// ============================================================
// Agent 模式配置
// ============================================================

async function configureAgentMode(
  cfg: OpenClawConfig,
  prompter: WizardPrompter,
  accountId: string,
): Promise<OpenClawConfig> {
  const recommendedPath = accountWebhookPath("agent", accountId);
  await prompter.note(
    [
      "正在配置 Agent 模式...",
      "",
      "💡 操作指南: 请在企微后台【应用管理 -> 自建应用】创建应用。",
    ].join("\n"),
    "Agent 模式配置",
  );

  const corpId = String(
    await prompter.text({
      message: "请输入 CorpID (企业ID):",
      validate: (value: string | undefined) => (value?.trim() ? undefined : "CorpID 不能为空"),
    }),
  ).trim();

  const agentIdStr = String(
    await prompter.text({
      message: "请输入 AgentID (应用ID):",
      validate: (value: string | undefined) => {
        const v = value?.trim() ?? "";
        if (!v) return "AgentID 不能为空";
        if (!/^\d+$/.test(v)) return "AgentID 应为数字";
        return undefined;
      },
    }),
  ).trim();
  const agentId = Number(agentIdStr);

  const agentSecret = String(
    await prompter.text({
      message: "请输入应用 Secret:",
      validate: (value: string | undefined) => (value?.trim() ? undefined : "应用 Secret 不能为空"),
    }),
  ).trim();

  await prompter.note(
    [
      "💡 操作指南: 请在自建应用详情页进入【接收消息 -> 设置API接收】。",
      `🔗 回调 URL (推荐): https://您的域名${recommendedPath}`,
      "🧭 说明: Agent 同时承担 Callback ingress 与 API egress；回调路径由系统派生。",
      "",
      "请先在后台填入回调 URL，然后获取以下信息。",
    ].join("\n"),
    "回调配置",
  );

  const token = String(
    await prompter.text({
      message: "请输入 Token (回调令牌):",
      validate: (value: string | undefined) => (value?.trim() ? undefined : "Token 不能为空"),
    }),
  ).trim();

  const encodingAESKey = String(
    await prompter.text({
      message: "请输入 EncodingAESKey (回调加密密钥):",
      validate: (value: string | undefined) => {
        const v = value?.trim() ?? "";
        if (!v) return "EncodingAESKey 不能为空";
        if (v.length !== 43) return "EncodingAESKey 应为 43 个字符";
        return undefined;
      },
    }),
  ).trim();

  const welcomeText = await prompter.text({
    message: "欢迎语 (可选):",
    placeholder: "欢迎使用智能助手",
    initialValue: "欢迎使用智能助手",
  });

  const agentConfig: WecomAgentConfig = {
    corpId,
    agentSecret,
    agentId,
    token,
    encodingAESKey,
    welcomeText: welcomeText?.trim() || undefined,
  };

  return setWecomAgentConfig(cfg, agentConfig, accountId);
}

// ============================================================
// DM 策略配置
// ============================================================

async function promptDmPolicy(
  cfg: OpenClawConfig,
  prompter: WizardPrompter,
  modes: ("bot" | "agent")[],
  accountId: string,
): Promise<OpenClawConfig> {
  const policyChoice = await prompter.select({
    message: "请选择私聊 (DM) 访问策略:",
    options: [
      { value: "pairing", label: "配对模式", hint: "推荐：安全，未知用户需授权" },
      { value: "allowlist", label: "白名单模式", hint: "仅允许特定 UserID" },
      { value: "open", label: "开放模式", hint: "任何人可发起" },
      { value: "disabled", label: "禁用私聊", hint: "不接受私聊消息" },
    ],
    initialValue: "open",
  });

  const policy = policyChoice as "pairing" | "allowlist" | "open" | "disabled";
  let allowFrom: string[] | undefined;

  if (policy === "allowlist") {
    const allowFromStr = String(
      await prompter.text({
        message: "请输入白名单 UserID (多个用逗号分隔):",
        placeholder: "user1,user2",
        validate: (value: string | undefined) =>
          value?.trim() ? undefined : "请输入至少一个 UserID",
      }),
    ).trim();
    allowFrom = allowFromStr
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
  }

  const dm: WecomDmConfig = { policy, allowFrom };

  let result = cfg;
  for (const mode of modes) {
    result = setWecomDmPolicy(result, mode, dm, accountId);
  }
  return result;
}

// ============================================================
// 配置汇总
// ============================================================

async function showSummary(
  cfg: OpenClawConfig,
  prompter: WizardPrompter,
  accountId: string,
): Promise<void> {
  const account = resolveWecomAccount({ cfg, accountId });
  const lines: string[] = ["✅ 配置已保存！", ""];

  if (account.bot?.configured) {
    lines.push("📱 Bot 模式: 已配置");
    lines.push(
      `   接入方式: ${account.bot.primaryTransport === "ws" ? "WebSocket 长连接" : "Webhook 回调"}`,
    );
    if (account.bot.primaryTransport === "ws") {
      lines.push("   WS 优势: 无需域名，长链接模式创建机器人门槛更低");
      lines.push("   主动消息: 支持定时任务、异常提醒等主动发消息场景");
      if (account.bot.webhookConfigured) {
        lines.push(
          `   可选回调模式: 已手动配置，推荐回调地址为 https://您的域名${accountWebhookPath("bot", accountId)}`,
        );
      }
    } else {
      lines.push(`   回调地址: https://您的域名${accountWebhookPath("bot", accountId)}`);
    }
  }

  if (account.agent?.configured) {
    lines.push("🏢 Agent 模式: 已配置");
    lines.push(`   回调地址: https://您的域名${accountWebhookPath("agent", accountId)}`);
    lines.push("   出站能力: Agent API（主动发送 / 补送 / 媒体）");
  }

  lines.push(`   接入标识: ${accountId}`);
  lines.push("   运维检查: openclaw channels status --deep");
  lines.push("   关键日志: [wecom-runtime] [wecom-ws] [wecom-http] [wecom-agent-delivery]");

  lines.push("");
  if (account.agent?.configured) {
    lines.push("⚠️ 请确保您已在企微后台填写了正确的 Agent 回调 URL，");
    lines.push("   并点击了后台的『保存』按钮完成验证。");
  } else if (account.bot?.primaryTransport === "webhook") {
    lines.push("⚠️ 请确保您已在企微后台填写了正确的 Bot 回调 URL，");
    lines.push("   并点击了后台的『保存』按钮完成验证。");
  }

  await prompter.note(lines.join("\n"), "配置完成");
}

// ============================================================
// Setup Wizard
// ============================================================

type WecomSetupStatus = {
  configured: boolean;
  statusLines: string[];
  selectionHint: string;
  quickstartScore: number;
};

async function getWecomSetupStatus(cfg: OpenClawConfig): Promise<WecomSetupStatus> {
  const resolved = resolveWecomAccounts(cfg);
  const accounts = Object.values(resolved.accounts).filter((account) => account.enabled !== false);
  const botConfigured = accounts.some((account) => Boolean(account.bot?.configured));
  const agentConfigured = accounts.some((account) => Boolean(account.agent?.configured));
  const configured = accounts.some((account) => account.configured);

  const statusParts: string[] = [];
  if (botConfigured) statusParts.push("Bot ✓");
  if (agentConfigured) statusParts.push("Agent ✓");
  const accountSuffix = accounts.length > 1 ? ` · ${accounts.length} accounts` : "";
  const statusSummary = statusParts.length > 0 ? statusParts.join(" + ") : "已配置";

  return {
    configured,
    statusLines: [
      `WeCom (企业微信): ${configured ? `${statusSummary}${accountSuffix}` : "需要配置"}`,
    ],
    selectionHint: configured
      ? `configured · ${statusSummary}${accountSuffix}`
      : "官方推荐 · 功能强大 · 上手简单",
    quickstartScore: configured ? 1 : 8,
  };
}

async function runWecomSetupFlow(params: {
  cfg: OpenClawConfig;
  prompter: WizardPrompter;
  accountId: string;
}): Promise<OpenClawConfig> {
  const mode = await promptMode(params.prompter);

  let next = params.cfg;
  const configuredModes: ("bot" | "agent")[] = [];

  if (mode === "bot" || mode === "both") {
    next = await configureBotMode(next, params.prompter, params.accountId);
    configuredModes.push("bot");
  }

  if (mode === "agent" || mode === "both") {
    next = await configureAgentMode(next, params.prompter, params.accountId);
    configuredModes.push("agent");
  }

  next = await promptDmPolicy(next, params.prompter, configuredModes, params.accountId);
  next = setWecomEnabled(next, true);
  await showSummary(next, params.prompter, params.accountId);
  return next;
}

export const wecomSetupWizard: ChannelSetupWizard = {
  channel,
  status: {
    configuredLabel: "已配置",
    unconfiguredLabel: "需要配置",
    configuredHint: "configured",
    unconfiguredHint: "官方推荐 · 功能强大 · 上手简单",
    configuredScore: 1,
    unconfiguredScore: 8,
    resolveConfigured: async ({ cfg }) => (await getWecomSetupStatus(cfg)).configured,
    resolveStatusLines: async ({ cfg }) => (await getWecomSetupStatus(cfg)).statusLines,
    resolveSelectionHint: async ({ cfg }) => (await getWecomSetupStatus(cfg)).selectionHint,
    resolveQuickstartScore: async ({ cfg }) => (await getWecomSetupStatus(cfg)).quickstartScore,
  },
  resolveAccountIdForConfigure: async ({
    cfg,
    prompter,
    accountOverride,
    shouldPromptAccountIds,
  }) => {
    await showWelcome(prompter);
    return await resolveOnboardingAccountId({
      cfg,
      prompter,
      accountOverride,
      shouldPromptAccountIds,
    });
  },
  credentials: [],
  finalize: async ({ cfg, accountId, prompter }) => ({
    cfg: await runWecomSetupFlow({
      cfg,
      prompter,
      accountId,
    }),
  }),
};
