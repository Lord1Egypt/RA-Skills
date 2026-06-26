/**
 * 微信服务号（公众号）配置向导。
 *
 * 因为公众号的配置项比较直白（appId/appSecret/token/encodingAESKey + 可选 originalId），
 * 我们没有把每个凭据拆成 ChannelSetupWizardCredential，而是用一个 finalize 把所有字段问完。
 * 这样 UX 更像"填表"而非"一行一行凭据交换"。
 */

import type {
  ChannelSetupAdapter,
  ChannelSetupInput,
  ChannelSetupWizard,
  OpenClawConfig,
  WizardPrompter,
} from "openclaw/plugin-sdk/setup";

import {
  CONFIG_SECTION_KEY,
  DEFAULT_ACCOUNT_ID,
  listWechatServiceAccountIds,
  resolveDefaultWechatServiceAccountId,
  resolveWechatServiceAccount,
  resolveDerivedPathSummary,
} from "./config/index.js";
import type {
  WechatServiceAccountConfig,
  WechatServiceConfig,
  WechatServiceEncryptMode,
} from "./types.js";

const channel = "wechat-service" as const;

function getChannelConfig(cfg: OpenClawConfig): WechatServiceConfig | undefined {
  const raw = (cfg.channels as Record<string, unknown> | undefined)?.[CONFIG_SECTION_KEY];
  return raw as WechatServiceConfig | undefined;
}

function setChannelConfig(
  cfg: OpenClawConfig,
  next: WechatServiceConfig,
): OpenClawConfig {
  return {
    ...cfg,
    channels: {
      ...(cfg.channels ?? {}),
      [CONFIG_SECTION_KEY]: next,
    },
  } as OpenClawConfig;
}

function upsertAccount(
  cfg: OpenClawConfig,
  accountId: string,
  patch: Partial<WechatServiceAccountConfig>,
): OpenClawConfig {
  const current = getChannelConfig(cfg) ?? {};
  const accounts = current.accounts ?? {};
  const existing: Partial<WechatServiceAccountConfig> = accounts[accountId] ?? {};
  const nextAccounts = {
    ...accounts,
    [accountId]: {
      ...existing,
      ...patch,
      enabled: patch.enabled ?? existing.enabled ?? true,
    } as WechatServiceAccountConfig,
  };
  return setChannelConfig(cfg, {
    ...current,
    enabled: true,
    defaultAccount:
      current.defaultAccount?.trim() || accountId,
    accounts: nextAccounts,
  });
}

async function promptAccountId(params: {
  cfg: OpenClawConfig;
  prompter: WizardPrompter;
  accountOverride?: string;
  shouldPromptAccountIds: boolean;
}): Promise<string> {
  const { cfg, prompter, accountOverride, shouldPromptAccountIds } = params;
  if (accountOverride?.trim()) return accountOverride.trim();

  const existing = listWechatServiceAccountIds(cfg);
  const defaultId = resolveDefaultWechatServiceAccountId(cfg);

  if (!shouldPromptAccountIds) {
    return existing[0] ?? defaultId ?? DEFAULT_ACCOUNT_ID;
  }

  if (existing.length === 0) {
    const entered = await prompter.text({
      message: "为这个微信服务号账号起一个 ID（会出现在 webhook 路径里）",
      placeholder: "default",
      initialValue: DEFAULT_ACCOUNT_ID,
    });
    const value = typeof entered === "string" ? entered.trim() : "";
    return value || DEFAULT_ACCOUNT_ID;
  }

  const options = [
    ...existing.map((id) => ({ value: id, label: id + (id === defaultId ? "（默认）" : "") })),
    { value: "__new__", label: "➕ 新增账号" },
  ];
  const picked = await prompter.select({
    message: "选择要配置的账号",
    options,
    initialValue: defaultId,
  });
  if (picked === "__new__") {
    const entered = await prompter.text({
      message: "新账号 ID",
      placeholder: "wx-account-2",
    });
    const value = typeof entered === "string" ? entered.trim() : "";
    return value || `wx-account-${existing.length + 1}`;
  }
  return typeof picked === "string" ? picked : defaultId;
}

async function showWelcome(
  prompter: WizardPrompter,
  accountId: string,
): Promise<void> {
  const paths = resolveDerivedPathSummary(accountId);
  const lines = [
    "接下来需要在「微信公众平台 → 基本配置 / 开发者中心」里拿到：",
    "  • AppID / AppSecret",
    "  • 服务器 Token",
    "  • （可选）EncodingAESKey（加密模式必填）",
    "",
    `此账号的 webhook 路径（填到公众号后台：服务器 URL）：`,
    `  https://你的域名${paths.primary}`,
  ];
  await prompter.note?.(lines.join("\n"), "微信服务号配置");
}

async function promptString(
  prompter: WizardPrompter,
  message: string,
  options?: { initialValue?: string; placeholder?: string; required?: boolean },
): Promise<string> {
  const result = await prompter.text({
    message,
    placeholder: options?.placeholder,
    initialValue: options?.initialValue,
  });
  const value = typeof result === "string" ? result.trim() : "";
  if (options?.required && !value) {
    await prompter.note?.("必填项不能为空。", "错误");
    return promptString(prompter, message, options);
  }
  return value;
}

async function runSetupFlow(params: {
  cfg: OpenClawConfig;
  accountId: string;
  prompter: WizardPrompter;
}): Promise<OpenClawConfig> {
  const { accountId, prompter } = params;
  let cfg = params.cfg;
  const current = resolveWechatServiceAccount({ cfg, accountId });

  await showWelcome(prompter, accountId);

  const appId = await promptString(prompter, "AppID", {
    initialValue: current.appId,
    placeholder: "wx1234567890abcdef",
    required: true,
  });
  const appSecret = await promptString(prompter, "AppSecret", {
    initialValue: current.appSecret,
    placeholder: "32 位字符串",
    required: true,
  });
  const token = await promptString(prompter, "服务器 Token（与公众号后台一致）", {
    initialValue: current.token,
    placeholder: "与公众号后台 URL 对应",
    required: true,
  });

  const encryptModeRaw = await prompter.select({
    message: "加密模式（推荐：安全模式）",
    options: [
      { value: "safe", label: "安全模式（推荐，需要 EncodingAESKey）" },
      { value: "compatible", label: "兼容模式（同时接受明文和加密）" },
      { value: "plain", label: "明文模式（仅测试用）" },
    ],
    initialValue: current.encryptMode ?? "safe",
  });
  const encryptMode =
    (typeof encryptModeRaw === "string"
      ? encryptModeRaw
      : "safe") as WechatServiceEncryptMode;

  let encodingAESKey = current.encodingAESKey;
  if (encryptMode !== "plain") {
    encodingAESKey = await promptString(prompter, "EncodingAESKey（43 位）", {
      initialValue: current.encodingAESKey,
      placeholder: "公众号后台：消息加解密密钥",
      required: true,
    });
  }

  const originalId = await promptString(prompter, "公众号原始 ID（gh_xxx，可选）", {
    initialValue: current.originalId,
    placeholder: "gh_xxxxxxxxxx",
  });

  const name = await promptString(prompter, "公众号名称（展示用，可选）", {
    initialValue: current.name ?? "",
    placeholder: "我的公众号",
  });

  cfg = upsertAccount(cfg, accountId, {
    appId,
    appSecret,
    token,
    encryptMode,
    encodingAESKey: encodingAESKey || undefined,
    originalId: originalId || undefined,
    name: name || undefined,
    enabled: true,
  });

  const paths = resolveDerivedPathSummary(accountId);
  await prompter.note?.(
    [
      `✅ 账号 ${accountId} 已配置。`,
      "",
      "接下来要在公众号后台 → 服务器配置 里填：",
      `  URL:            https://你的域名${paths.primary}`,
      `  Token:          ${token}`,
      `  EncodingAESKey: ${encodingAESKey || "（明文模式下留空）"}`,
      `  消息加解密方式: ${encryptMode === "safe" ? "安全模式" : encryptMode === "compatible" ? "兼容模式" : "明文模式"}`,
      "",
      "保存时公众平台会给 /webhook 发一次 GET（echostr 校验），确保 gateway 在线。",
    ].join("\n"),
    "下一步",
  );

  return cfg;
}

export const wechatServiceSetupWizard: ChannelSetupWizard = {
  channel,
  status: {
    configuredLabel: "已配置",
    unconfiguredLabel: "需要配置",
    configuredHint: "configured",
    unconfiguredHint: "公众号 AppID/Secret/Token/AESKey",
    configuredScore: 1,
    unconfiguredScore: 12,
    resolveConfigured: ({ cfg, accountId }) => {
      const ids = accountId ? [accountId] : listWechatServiceAccountIds(cfg);
      return ids.some((id) => resolveWechatServiceAccount({ cfg, accountId: id }).configured);
    },
    resolveStatusLines: ({ cfg, accountId, configured }) => {
      const id = accountId || resolveDefaultWechatServiceAccountId(cfg);
      const account = resolveWechatServiceAccount({ cfg, accountId: id });
      return [
        `账号 ${id}: ${configured ? "已配置" : "需要配置"} (appId=${account.appId || "∅"} encryptMode=${account.encryptMode})`,
      ];
    },
  },
  resolveAccountIdForConfigure: async ({
    cfg,
    prompter,
    accountOverride,
    shouldPromptAccountIds,
  }) => {
    return promptAccountId({
      cfg,
      prompter,
      accountOverride,
      shouldPromptAccountIds,
    });
  },
  credentials: [],
  finalize: async ({ cfg, accountId, prompter }) => ({
    cfg: await runSetupFlow({
      cfg,
      accountId,
      prompter,
    }),
  }),
  disable: (cfg) => {
    const current = getChannelConfig(cfg);
    if (!current) return cfg;
    return setChannelConfig(cfg, { ...current, enabled: false });
  },
};

// ============================================================================
// Channel Setup Adapter (CLI `openclaw channels add` 入口)
// ============================================================================
//
// `setupWizard` 是给 OpenClaw 主会话的交互向导（/setup wechat-service）；
// 这里的 `wechatServiceSetupAdapter` 是给 CLI `channels add` 用的非交互入口。
//
// 由于公众号需要 4 个核心凭据（AppID / AppSecret / Token / EncodingAESKey），
// 而 OpenClaw `ChannelSetupInput` 只暴露通用 flag（`--name` / `--token` / `--use-env` 等），
// 我们的适配策略：
//   - `--name` → 账号显示名
//   - `--token` → 微信服务器 Token（不是 access_token）
//   - 其余 3 项凭据从环境变量读取（约定式）：
//     `WECHAT_SERVICE_APP_ID` / `WECHAT_SERVICE_APP_SECRET` / `WECHAT_SERVICE_ENCODING_AES_KEY`
//     非 default 账号用 `WECHAT_SERVICE_<ACCOUNTID>_APP_ID` 这种带 accountId 的前缀
//   - 如果环境变量缺失，账号会先以 enabled:true 但 configured:false 写入；用户后续
//     可在 OpenClaw 主会话跑 `/setup wechat-service` 完整填写
//
// 这个设计让 CI / Docker 部署能用 env vars 一键完成 channel add，而交互场景仍能
// 通过 wizard 走完整 UX。
// ============================================================================

function envKey(accountId: string, suffix: string): string {
  const prefix = "WECHAT_SERVICE";
  if (accountId === DEFAULT_ACCOUNT_ID) return `${prefix}_${suffix}`;
  return `${prefix}_${accountId.toUpperCase().replace(/[^A-Z0-9]/g, "_")}_${suffix}`;
}

function readEnvCredentials(accountId: string): {
  appId?: string;
  appSecret?: string;
  encodingAESKey?: string;
  originalId?: string;
} {
  const env = process.env;
  return {
    appId: env[envKey(accountId, "APP_ID")]?.trim() || env.WECHAT_SERVICE_APP_ID?.trim(),
    appSecret:
      env[envKey(accountId, "APP_SECRET")]?.trim() || env.WECHAT_SERVICE_APP_SECRET?.trim(),
    encodingAESKey:
      env[envKey(accountId, "ENCODING_AES_KEY")]?.trim() ||
      env.WECHAT_SERVICE_ENCODING_AES_KEY?.trim(),
    originalId:
      env[envKey(accountId, "ORIGINAL_ID")]?.trim() || env.WECHAT_SERVICE_ORIGINAL_ID?.trim(),
  };
}

export const wechatServiceSetupAdapter: ChannelSetupAdapter = {
  resolveAccountId: ({ accountId }) => (accountId?.trim() || DEFAULT_ACCOUNT_ID),

  validateInput: ({ input }) => {
    // input.token 是 wechat 服务器 Token；不强制（用户可能后续走 wizard 填）
    // 这里只做基础校验：accountId 长度 / name 长度
    if (input.name && input.name.length > 60) {
      return "name 太长（最多 60 字符）";
    }
    return null;
  },

  applyAccountConfig: ({ cfg, accountId, input }) => {
    const env = readEnvCredentials(accountId);
    const token = input.token?.trim();
    const name = input.name?.trim();

    const patch: Partial<WechatServiceAccountConfig> = {
      enabled: true,
    };
    if (name) patch.name = name;
    if (token) patch.token = token;
    if (env.appId) patch.appId = env.appId;
    if (env.appSecret) patch.appSecret = env.appSecret;
    if (env.encodingAESKey) {
      patch.encodingAESKey = env.encodingAESKey;
      patch.encryptMode = "safe";
    } else {
      // 没有 AESKey 默认走 plain（仅测试用，不推荐生产）
      patch.encryptMode = "plain";
    }
    if (env.originalId) patch.originalId = env.originalId;

    return upsertAccount(cfg, accountId, patch);
  },

  applyAccountName: ({ cfg, accountId, name }) => {
    if (!name?.trim()) return cfg;
    return upsertAccount(cfg, accountId, { name: name.trim() });
  },
};
