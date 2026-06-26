import type { OpenClawConfig } from "openclaw/plugin-sdk";
import { describe, expect, it } from "vitest";

import { resolveWecomAccount } from "./accounts.js";

describe("resolveWecomAccount", () => {
  const cfg: OpenClawConfig = {
    channels: {
      wecom: {
        enabled: true,
        defaultAccount: "acct-a",
        accounts: {
          "acct-a": {
            enabled: true,
            bot: {
              primaryTransport: "webhook",
              webhook: {
                token: "token-a",
                encodingAESKey: "aes-a",
              },
            },
          },
        },
      },
    },
  } as OpenClawConfig;

  it("does not fall back when explicit accountId does not exist", () => {
    const account = resolveWecomAccount({ cfg, accountId: "missing" });
    expect(account.accountId).toBe("missing");
    expect(account.enabled).toBe(false);
    expect(account.configured).toBe(false);
  });

  it("uses configured default account when accountId is omitted", () => {
    const account = resolveWecomAccount({ cfg });
    expect(account.accountId).toBe("acct-a");
    expect(account.enabled).toBe(true);
    expect(account.configured).toBe(true);
  });

  it("treats literal default as an alias for configured default account", () => {
    const account = resolveWecomAccount({ cfg, accountId: "default" });
    expect(account.accountId).toBe("acct-a");
    expect(account.enabled).toBe(true);
    expect(account.configured).toBe(true);
  });

  it("accepts agentSecret for fresh configs and normalizes it for runtime use", () => {
    const agentCfg: OpenClawConfig = {
      channels: {
        wecom: {
          enabled: true,
          defaultAccount: "acct-agent",
          accounts: {
            "acct-agent": {
              enabled: true,
              agent: {
                corpId: "corp-id",
                agentSecret: "agent-secret",
                agentId: 1000001,
                token: "token",
                encodingAESKey: "1234567890123456789012345678901234567890123",
              },
            },
          },
        },
      },
    } as OpenClawConfig;

    const account = resolveWecomAccount({ cfg: agentCfg });
    expect(account.agent?.apiConfigured).toBe(true);
    expect(account.agent?.corpSecret).toBe("agent-secret");
  });
});
