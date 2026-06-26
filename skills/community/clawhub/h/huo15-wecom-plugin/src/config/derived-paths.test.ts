import { describe, expect, it } from "vitest";

import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";

import { resolveDerivedPathSummary } from "./derived-paths.js";
import {
  hasMatrixExplicitRoutesRegistered,
  registerAgentWebhookTarget,
  registerWecomWebhookTarget,
} from "../transport/http/registry.js";
import type { ResolvedAgentAccount, ResolvedBotAccount } from "../types/index.js";

function createBotAccount(accountId: string): ResolvedBotAccount {
  return {
    accountId,
    configured: true,
    primaryTransport: "webhook",
    wsConfigured: false,
    webhookConfigured: true,
    config: {} as ResolvedBotAccount["config"],
    token: "token",
    encodingAESKey: "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG",
    receiveId: "",
    botId: "",
    secret: "",
    webhook: {
      token: "token",
      encodingAESKey: "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG",
      receiveId: "",
    },
  };
}

function createAgentAccount(accountId: string): ResolvedAgentAccount {
  return {
    accountId,
    configured: true,
    callbackConfigured: true,
    apiConfigured: true,
    corpId: `corp-${accountId}`,
    corpSecret: `secret-${accountId}`,
    agentId: 1001,
    token: "token",
    encodingAESKey: "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG",
    config: {} as ResolvedAgentAccount["config"],
  };
}

const emptyConfig = {} as OpenClawConfig;
const emptyCore = {} as PluginRuntime;

describe("resolveDerivedPathSummary", () => {
  it("registers scoped aliases first for the default account", () => {
    expect(resolveDerivedPathSummary("default")).toEqual({
      botWebhook: [
        "/plugins/wecom/bot/default",
        "/wecom/bot/default",
        "/plugins/wecom/bot",
        "/wecom",
        "/wecom/bot",
      ],
      agentCallback: [
        "/plugins/wecom/agent/default",
        "/wecom/agent/default",
        "/plugins/wecom/agent",
        "/wecom/agent",
      ],
      kefu: [
        "/plugins/wecom/kefu/default",
        "/wecom/kefu/default",
        "/plugins/wecom/kefu",
        "/wecom/kefu",
      ],
    });
  });
});

describe("hasMatrixExplicitRoutesRegistered", () => {
  it("ignores default-account scoped aliases", () => {
    const unregisterBot = registerWecomWebhookTarget({
      account: createBotAccount("default"),
      config: emptyConfig,
      runtime: {},
      core: emptyCore,
      path: "/plugins/wecom/bot/default",
    });
    const unregisterAgent = registerAgentWebhookTarget({
      agent: createAgentAccount("default"),
      config: emptyConfig,
      runtimeEnv: {},
      path: "/plugins/wecom/agent/default",
    });

    try {
      expect(hasMatrixExplicitRoutesRegistered()).toBe(false);
    } finally {
      unregisterAgent();
      unregisterBot();
    }
  });

  it("detects non-default explicit account routes", () => {
    const unregister = registerWecomWebhookTarget({
      account: createBotAccount("acct-a"),
      config: emptyConfig,
      runtime: {},
      core: emptyCore,
      path: "/plugins/wecom/bot/acct-a",
    });

    try {
      expect(hasMatrixExplicitRoutesRegistered()).toBe(true);
    } finally {
      unregister();
    }
  });
});
