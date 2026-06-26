import { describe, expect, it } from "vitest";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import {
  detectMode,
  isWechatServiceEnabled,
  listWechatServiceAccountIds,
  resolveDefaultWechatServiceAccountId,
  resolveWechatServiceAccount,
  resolveWechatServiceAccounts,
} from "./accounts.js";

function makeCfg(overrides: Record<string, unknown>): OpenClawConfig {
  return {
    channels: {
      "wechat-service": overrides,
    },
  } as unknown as OpenClawConfig;
}

describe("wechat-service accounts", () => {
  it("detects disabled when no accounts", () => {
    expect(detectMode(undefined)).toBe("disabled");
    expect(detectMode({})).toBe("disabled");
    expect(detectMode({ accounts: {} })).toBe("disabled");
  });

  it("detects matrix mode when accounts are configured", () => {
    expect(
      detectMode({
        accounts: { main: { appId: "a", appSecret: "b", token: "c" } },
      }),
    ).toBe("matrix");
  });

  it("resolves a fully configured account in safe mode", () => {
    const cfg = makeCfg({
      accounts: {
        main: {
          appId: "wx123",
          appSecret: "secret",
          token: "tok",
          encodingAESKey: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ",
          originalId: "gh_abc",
        },
      },
      defaultAccount: "main",
    });
    const resolved = resolveWechatServiceAccount({ cfg, accountId: "main" });
    expect(resolved.configured).toBe(true);
    expect(resolved.encryptMode).toBe("safe");
    expect(resolved.replyMode).toBe("async");
  });

  it("marks account unconfigured when token missing", () => {
    const cfg = makeCfg({
      accounts: {
        main: { appId: "wx", appSecret: "secret" },
      },
    });
    expect(resolveWechatServiceAccount({ cfg, accountId: "main" }).configured).toBe(false);
  });

  it("returns plain mode when encodingAESKey omitted", () => {
    const cfg = makeCfg({
      accounts: {
        main: { appId: "wx", appSecret: "s", token: "t" },
      },
    });
    const acc = resolveWechatServiceAccount({ cfg, accountId: "main" });
    expect(acc.encryptMode).toBe("plain");
    expect(acc.configured).toBe(true);
  });

  it("lists account ids sorted", () => {
    const cfg = makeCfg({
      accounts: {
        beta: { appId: "b", appSecret: "s", token: "t" },
        alpha: { appId: "a", appSecret: "s", token: "t" },
      },
    });
    expect(listWechatServiceAccountIds(cfg)).toEqual(["alpha", "beta"]);
  });

  it("picks default account from defaultAccount when set", () => {
    const cfg = makeCfg({
      defaultAccount: "beta",
      accounts: {
        alpha: { appId: "a", appSecret: "s", token: "t" },
        beta: { appId: "b", appSecret: "s", token: "t" },
      },
    });
    expect(resolveDefaultWechatServiceAccountId(cfg)).toBe("beta");
  });

  it("reports enabled when at least one account configured", () => {
    const cfg = makeCfg({
      accounts: {
        main: { appId: "a", appSecret: "s", token: "t" },
      },
    });
    expect(isWechatServiceEnabled(cfg)).toBe(true);
  });

  it("merges top-level routing into per-account routing", () => {
    const cfg = makeCfg({
      routing: { events: { subscribe: "welcome-agent" } },
      accounts: {
        main: {
          appId: "a",
          appSecret: "s",
          token: "t",
          routing: { events: { click: "menu-agent" } },
        },
      },
    });
    const acc = resolveWechatServiceAccounts(cfg).accounts.main!;
    expect(acc.routing.events?.subscribe).toBe("welcome-agent");
    expect(acc.routing.events?.click).toBe("menu-agent");
  });
});
