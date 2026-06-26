import type { OpenClawConfig, WizardPrompter } from "openclaw/plugin-sdk";
import type { RuntimeEnv } from "openclaw/plugin-sdk";
import { describe, expect, it, vi } from "vitest";
import { buildChannelSetupWizardAdapterFromSetupWizard } from "../../../src/channels/plugins/setup-wizard.js";
import { wecomPlugin } from "./channel.js";

const wecomSetupAdapter = buildChannelSetupWizardAdapterFromSetupWizard({
  plugin: wecomPlugin,
  wizard: wecomPlugin.setupWizard!,
});

function createPrompter(overrides: Partial<WizardPrompter>): WizardPrompter {
  return {
    intro: vi.fn(async () => {}),
    outro: vi.fn(async () => {}),
    note: vi.fn(async () => {}),
    select: vi.fn(async () => "bot") as WizardPrompter["select"],
    multiselect: vi.fn(async () => []),
    text: vi.fn(async () => "") as WizardPrompter["text"],
    confirm: vi.fn(async () => false),
    progress: vi.fn(() => ({ update: vi.fn(), stop: vi.fn() })),
    ...overrides,
  };
}

function createRuntime(): RuntimeEnv {
  return {
    log: vi.fn(),
    error: vi.fn(),
    exit: vi.fn((_: number) => undefined),
  } as unknown as RuntimeEnv;
}

describe("wecom onboarding", () => {
  it("configures bot mode with ws transport by default", async () => {
    const prompter = createPrompter({
      select: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请选择您要配置的接入模式:") {
          return "bot";
        }
        if (message === "请选择私聊 (DM) 访问策略:") {
          return "pairing";
        }
        throw new Error(`Unexpected select prompt: ${message}`);
      }) as WizardPrompter["select"],
      text: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请输入 BotId（机器人 ID）:") {
          return "bot-id-123";
        }
        if (message === "请输入 Secret（机器人密钥）:") {
          return "bot-secret-456";
        }
        if (message === "流式占位符 (可选):") {
          return "正在思考...";
        }
        if (message === "欢迎语 (可选):") {
          return "你好，我是企业微信机器人";
        }
        throw new Error(`Unexpected text prompt: ${message}`);
      }) as WizardPrompter["text"],
    });

    const result = await wecomSetupAdapter.configure({
      cfg: {} as OpenClawConfig,
      runtime: createRuntime(),
      prompter,
      options: {},
      accountOverrides: {},
      shouldPromptAccountIds: false,
      forceAllowFrom: false,
    });

    const bot = result.cfg.channels?.wecom?.accounts?.default?.bot;
    expect(result.accountId).toBe("default");
    expect(bot?.primaryTransport).toBe("ws");
    expect(bot?.ws).toEqual({
      botId: "bot-id-123",
      secret: "bot-secret-456",
    });
    expect(bot?.webhook).toBeUndefined();

    const noteText = (prompter.note as ReturnType<typeof vi.fn>).mock.calls
      .map(([message]) => String(message))
      .join("\n");
    expect(noteText).toContain(
      "YanHaidao/wecom 是企业微信官方推荐三方插件，功能强大，适合直接落生产环境。",
    );
    expect(noteText).toContain(
      "默认就是 Bot WebSocket 模式，配置简单，无需域名，普通用户也能快速接入。",
    );
    expect(noteText).toContain("支持主动发消息，定时任务、异常提醒、工作流通知都可直接落地。");
  });

  it("preserves manually configured bot webhook when rerunning onboarding", async () => {
    const prompter = createPrompter({
      select: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请选择您要配置的接入模式:") {
          return "bot";
        }
        if (message === "请选择私聊 (DM) 访问策略:") {
          return "pairing";
        }
        throw new Error(`Unexpected select prompt: ${message}`);
      }) as WizardPrompter["select"],
      text: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请输入 BotId（机器人 ID）:") {
          return "bot-id-next";
        }
        if (message === "请输入 Secret（机器人密钥）:") {
          return "bot-secret-next";
        }
        if (message === "流式占位符 (可选):") {
          return "正在思考...";
        }
        if (message === "欢迎语 (可选):") {
          return "你好";
        }
        throw new Error(`Unexpected text prompt: ${message}`);
      }) as WizardPrompter["text"],
    });

    const initialCfg: OpenClawConfig = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "default",
          accounts: {
            default: {
              enabled: true,
              bot: {
                primaryTransport: "webhook",
                webhook: {
                  token: "manual-token",
                  encodingAESKey: "1234567890123456789012345678901234567890123",
                  receiveId: "manual-receive-id",
                },
              },
            },
          },
        },
      },
    };

    const result = await wecomSetupAdapter.configure({
      cfg: initialCfg,
      runtime: createRuntime(),
      prompter,
      options: {},
      accountOverrides: {},
      shouldPromptAccountIds: false,
      forceAllowFrom: false,
    });

    const bot = result.cfg.channels?.wecom?.accounts?.default?.bot;
    expect(bot?.primaryTransport).toBe("ws");
    expect(bot?.ws).toEqual({
      botId: "bot-id-next",
      secret: "bot-secret-next",
    });
    expect(bot?.webhook).toEqual({
      token: "manual-token",
      encodingAESKey: "1234567890123456789012345678901234567890123",
      receiveId: "manual-receive-id",
    });
  });

  it("reports chinese status copy for channel selection", async () => {
    const status = await wecomSetupAdapter.getStatus({
      cfg: {} as OpenClawConfig,
      options: {},
      accountOverrides: {},
    });

    expect(status.statusLines).toEqual(["WeCom (企业微信): 需要配置"]);
    expect(status.selectionHint).toBe("官方推荐 · 功能强大 · 上手简单");
  });

  it("uses plugin-owned chinese account selection and no generic dm adapter", async () => {
    const prompter = createPrompter({
      select: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请选择企业微信接入标识（英文）:") {
          return "__new__";
        }
        if (message === "请选择您要配置的接入模式:") {
          return "bot";
        }
        if (message === "请选择私聊 (DM) 访问策略:") {
          return "disabled";
        }
        throw new Error(`Unexpected select prompt: ${message}`);
      }) as WizardPrompter["select"],
      text: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请输入新的企业微信接入标识（英文）:") {
          return "HaiDao";
        }
        if (message === "请输入 BotId（机器人 ID）:") {
          return "bot-id";
        }
        if (message === "请输入 Secret（机器人密钥）:") {
          return "bot-secret";
        }
        if (message === "流式占位符 (可选):") {
          return "正在思考...";
        }
        if (message === "欢迎语 (可选):") {
          return "你好";
        }
        throw new Error(`Unexpected text prompt: ${message}`);
      }) as WizardPrompter["text"],
    });

    const result = await wecomSetupAdapter.configure({
      cfg: {} as OpenClawConfig,
      runtime: createRuntime(),
      prompter,
      options: {},
      accountOverrides: {},
      shouldPromptAccountIds: true,
      forceAllowFrom: false,
    });

    expect(result.accountId).toBe("haidao");
    const noteText = (prompter.note as ReturnType<typeof vi.fn>).mock.calls
      .map(([message]) => String(message))
      .join("\n");
    expect(noteText).toContain("接入标识已规范化为：haidao");
    expect(wecomSetupAdapter.dmPolicy).toBeUndefined();
  });

  it("offers default account selection when config has no accounts", async () => {
    const prompter = createPrompter({
      select: vi.fn(
        async ({
          message,
          options,
        }: {
          message: string;
          options: Array<{ value: string; label: string }>;
        }) => {
          if (message === "请选择企业微信接入标识（英文）:") {
            expect(options.map((option) => option.value)).toEqual(["default", "__new__"]);
            expect(options[0]?.label).toBe("default（默认标识）");
            return "default";
          }
          if (message === "请选择您要配置的接入模式:") {
            return "bot";
          }
          if (message === "请选择私聊 (DM) 访问策略:") {
            return "pairing";
          }
          throw new Error(`Unexpected select prompt: ${message}`);
        },
      ) as WizardPrompter["select"],
      text: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请输入 BotId（机器人 ID）:") {
          return "bot-id-default";
        }
        if (message === "请输入 Secret（机器人密钥）:") {
          return "bot-secret-default";
        }
        if (message === "流式占位符 (可选):") {
          return "";
        }
        if (message === "欢迎语 (可选):") {
          return "";
        }
        throw new Error(`Unexpected text prompt: ${message}`);
      }) as WizardPrompter["text"],
    });

    const result = await wecomSetupAdapter.configure({
      cfg: {} as OpenClawConfig,
      runtime: createRuntime(),
      prompter,
      options: {},
      accountOverrides: {},
      shouldPromptAccountIds: true,
      forceAllowFrom: false,
    });

    expect(result.accountId).toBe("default");
    expect(result.cfg.channels?.wecom?.accounts?.default?.bot?.ws).toEqual({
      botId: "bot-id-default",
      secret: "bot-secret-default",
    });
  });

  it("writes agentSecret for fresh agent onboarding", async () => {
    const prompter = createPrompter({
      select: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请选择您要配置的接入模式:") {
          return "agent";
        }
        if (message === "请选择私聊 (DM) 访问策略:") {
          return "open";
        }
        throw new Error(`Unexpected select prompt: ${message}`);
      }) as WizardPrompter["select"],
      text: vi.fn(async ({ message }: { message: string }) => {
        if (message === "请输入 CorpID (企业ID):") {
          return "corp-id";
        }
        if (message === "请输入 AgentID (应用ID):") {
          return "1000001";
        }
        if (message === "请输入应用 Secret:") {
          return "agent-secret";
        }
        if (message === "请输入 Token (回调令牌):") {
          return "callback-token";
        }
        if (message === "请输入 EncodingAESKey (回调加密密钥):") {
          return "1234567890123456789012345678901234567890123";
        }
        if (message === "欢迎语 (可选):") {
          return "欢迎使用智能助手";
        }
        throw new Error(`Unexpected text prompt: ${message}`);
      }) as WizardPrompter["text"],
    });

    const result = await wecomSetupAdapter.configure({
      cfg: {} as OpenClawConfig,
      runtime: createRuntime(),
      prompter,
      options: {},
      accountOverrides: {},
      shouldPromptAccountIds: false,
      forceAllowFrom: false,
    });

    const agent = result.cfg.channels?.wecom?.accounts?.default?.agent;
    expect(agent?.agentSecret).toBe("agent-secret");
    expect(agent?.corpSecret).toBeUndefined();
  });
});
