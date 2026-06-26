import { beforeEach, describe, expect, it, vi } from "vitest";
import type { OpenClawConfig } from "openclaw/plugin-sdk";

import {
  buildAgentSessionTarget,
  ensureDynamicAgentListed,
  generateAgentId,
  getDynamicAgentConfig,
  resetEnsuredCache,
  shouldUseDynamicAgent,
} from "./dynamic-agent.js";

function makeConfig(dynamicAgents?: Record<string, unknown>): OpenClawConfig {
  return {
    channels: {
      "wechat-service": dynamicAgents ? { dynamicAgents } : {},
    },
  } as unknown as OpenClawConfig;
}

function makeLegacyConfig(dynamicAgents?: Record<string, unknown>): OpenClawConfig {
  // 模拟 v0.1 ~ v1.0.0 配置（legacy camelCase key），用于测试 backward-compat 兜底
  return {
    channels: {
      wechatService: dynamicAgents ? { dynamicAgents } : {},
    },
  } as unknown as OpenClawConfig;
}

describe("wechat-service dynamic-agent", () => {
  beforeEach(() => {
    resetEnsuredCache();
  });

  describe("getDynamicAgentConfig defaults", () => {
    // v2.3.0 起：默认 enabled=true（开箱即用，每位粉丝独立 agent）+ defaultInstructionsPreset='it-support'
    it("returns enabled=true by default when nothing is configured (v2.3.0+)", () => {
      const cfg = getDynamicAgentConfig(makeConfig());
      expect(cfg.enabled).toBe(true);
      expect(cfg.dmCreateAgent).toBe(true);
      expect(cfg.groupEnabled).toBe(false);
      expect(cfg.adminUsers).toEqual([]);
      expect(cfg.defaultInstructionsPreset).toBe("it-support");
    });

    it("respects user-provided fields", () => {
      const cfg = getDynamicAgentConfig(
        makeConfig({
          enabled: false,
          dmCreateAgent: false,
          groupEnabled: true,
          adminUsers: ["oABC", "oDEF"],
          defaultInstructionsPreset: "none",
        }),
      );
      expect(cfg).toEqual({
        enabled: false,
        dmCreateAgent: false,
        groupEnabled: true,
        adminUsers: ["oABC", "oDEF"],
        defaultInstructionsPreset: "none",
      });
    });

    it("does not crash when channels[wechat-service] is missing entirely", () => {
      const cfg = getDynamicAgentConfig({} as OpenClawConfig);
      // 空配置走默认（v2.3.0 enabled=true）
      expect(cfg.enabled).toBe(true);
      expect(cfg.defaultInstructionsPreset).toBe("it-support");
    });

    it("falls back to legacy 'wechatService' key (v0.1 ~ v1.0.0)", () => {
      const cfg = getDynamicAgentConfig(
        makeLegacyConfig({ enabled: true, dmCreateAgent: true }),
      );
      expect(cfg.enabled).toBe(true);
      expect(cfg.dmCreateAgent).toBe(true);
    });

    it("kebab key takes precedence over legacy key when both present", () => {
      const cfg = getDynamicAgentConfig({
        channels: {
          "wechat-service": { dynamicAgents: { enabled: true } },
          wechatService: { dynamicAgents: { enabled: false } },
        },
      } as unknown as OpenClawConfig);
      expect(cfg.enabled).toBe(true);
    });
  });

  describe("generateAgentId naming", () => {
    it("produces wechat-service-<account>-<type>-<peer>", () => {
      expect(generateAgentId("dm", "oABC123", "default")).toBe(
        "wechat-service-default-dm-oabc123",
      );
    });

    it("preserves underscore and hyphen, sanitizes others", () => {
      // openid 通常长这样 oABC1d2_3-XYZ —— `_-` 应被保留
      expect(generateAgentId("dm", "oABC1d2_3-XYZ", "shop_a")).toBe(
        "wechat-service-shop_a-dm-oabc1d2_3-xyz",
      );
    });

    it("replaces non-[a-z0-9_-] with underscore", () => {
      expect(generateAgentId("dm", "user@with.dots+plus", "acct")).toBe(
        "wechat-service-acct-dm-user_with_dots_plus",
      );
    });

    it("falls back to default account when omitted", () => {
      expect(generateAgentId("dm", "oABC")).toBe("wechat-service-default-dm-oabc");
    });

    it("falls back to unknown when peer is empty", () => {
      expect(generateAgentId("dm", "", "default")).toBe(
        "wechat-service-default-dm-unknown",
      );
    });

    it("supports group chat type even though 公众号 doesn't use it", () => {
      // 字段保留 —— schema 兼容 wecom，不能在 generateAgentId 层面禁掉
      expect(generateAgentId("group", "wr123", "default")).toBe(
        "wechat-service-default-group-wr123",
      );
    });
  });

  describe("buildAgentSessionTarget", () => {
    it("builds wechat-service:<accountId>:user:<openid>", () => {
      expect(buildAgentSessionTarget("oABC123", "shopA")).toBe(
        "wechat-service:shopa:user:oABC123",
      );
    });

    it("preserves openid case (only accountId is sanitized)", () => {
      // openid 在外部是 case-sensitive 的标识，不能小写
      expect(buildAgentSessionTarget("oABC", "DEFAULT")).toBe(
        "wechat-service:default:user:oABC",
      );
    });

    it("falls back to default account", () => {
      expect(buildAgentSessionTarget("oABC")).toBe(
        "wechat-service:default:user:oABC",
      );
    });
  });

  describe("shouldUseDynamicAgent", () => {
    it("returns false when disabled", () => {
      expect(
        shouldUseDynamicAgent({
          chatType: "dm",
          senderId: "oUser1",
          config: makeConfig({ enabled: false, dmCreateAgent: true }),
        }),
      ).toBe(false);
    });

    it("returns true for dm when enabled + dmCreateAgent", () => {
      expect(
        shouldUseDynamicAgent({
          chatType: "dm",
          senderId: "oUser1",
          config: makeConfig({ enabled: true, dmCreateAgent: true }),
        }),
      ).toBe(true);
    });

    it("returns false for dm when dmCreateAgent is false", () => {
      expect(
        shouldUseDynamicAgent({
          chatType: "dm",
          senderId: "oUser1",
          config: makeConfig({ enabled: true, dmCreateAgent: false }),
        }),
      ).toBe(false);
    });

    it("respects groupEnabled for group chat type", () => {
      expect(
        shouldUseDynamicAgent({
          chatType: "group",
          senderId: "oUser1",
          config: makeConfig({ enabled: true, groupEnabled: true }),
        }),
      ).toBe(true);
      expect(
        shouldUseDynamicAgent({
          chatType: "group",
          senderId: "oUser1",
          config: makeConfig({ enabled: true, groupEnabled: false }),
        }),
      ).toBe(false);
    });

    it("admin users bypass dynamic routing (case-insensitive)", () => {
      const cfg = makeConfig({
        enabled: true,
        dmCreateAgent: true,
        adminUsers: ["oAdmin1", "oAdmin2"],
      });
      expect(
        shouldUseDynamicAgent({ chatType: "dm", senderId: "oAdmin1", config: cfg }),
      ).toBe(false);
      expect(
        shouldUseDynamicAgent({ chatType: "dm", senderId: "OADMIN1", config: cfg }),
      ).toBe(false);
      expect(
        shouldUseDynamicAgent({ chatType: "dm", senderId: "oNormalUser", config: cfg }),
      ).toBe(true);
    });
  });

  describe("ensureDynamicAgentListed", () => {
    it("writes new agent id to agents.list and seeds main on first call", async () => {
      const stored: { value: Record<string, unknown> } = { value: {} };
      const runtime = {
        config: {
          loadConfig: () => stored.value,
          writeConfigFile: vi.fn(async (next: unknown) => {
            stored.value = next as Record<string, unknown>;
          }),
        },
      };

      await ensureDynamicAgentListed("wechat-service-default-dm-oabc", runtime);

      expect(runtime.config.writeConfigFile).toHaveBeenCalledTimes(1);
      const list = (stored.value.agents as { list: Array<{ id: string }> }).list;
      expect(list.map((e) => e.id)).toEqual([
        "main",
        "wechat-service-default-dm-oabc",
      ]);
    });

    it("is idempotent — second call with same id is a no-op", async () => {
      const stored: { value: Record<string, unknown> } = {
        value: { agents: { list: [{ id: "main" }] } },
      };
      const runtime = {
        config: {
          loadConfig: () => stored.value,
          writeConfigFile: vi.fn(async (next: unknown) => {
            stored.value = next as Record<string, unknown>;
          }),
        },
      };

      await ensureDynamicAgentListed("wechat-service-default-dm-oabc", runtime);
      await ensureDynamicAgentListed("wechat-service-default-dm-oabc", runtime);

      expect(runtime.config.writeConfigFile).toHaveBeenCalledTimes(1);
    });

    it("does not seed main when list already exists", async () => {
      const stored: { value: Record<string, unknown> } = {
        value: { agents: { list: [{ id: "main" }, { id: "secondary" }] } },
      };
      const runtime = {
        config: {
          loadConfig: () => stored.value,
          writeConfigFile: vi.fn(async (next: unknown) => {
            stored.value = next as Record<string, unknown>;
          }),
        },
      };

      await ensureDynamicAgentListed("wechat-service-default-dm-onew", runtime);
      const list = (stored.value.agents as { list: Array<{ id: string }> }).list;
      expect(list.map((e) => e.id)).toEqual([
        "main",
        "secondary",
        "wechat-service-default-dm-onew",
      ]);
    });

    it("silently skips when runtime has no config helpers", async () => {
      // 不应抛错；plugin 在某些 OpenClaw 版本上可能拿不到 config helpers
      await expect(
        ensureDynamicAgentListed("foo", {} as unknown),
      ).resolves.toBeUndefined();
    });

    it("writes agent with instructions when provided", async () => {
      const stored: { value: Record<string, unknown> } = { value: {} };
      const runtime = {
        config: {
          loadConfig: () => stored.value,
          writeConfigFile: vi.fn(async (next: unknown) => {
            stored.value = next as Record<string, unknown>;
          }),
        },
      };

      await ensureDynamicAgentListed(
        "wechat-service-default-dm-oabc",
        runtime,
        "你是客服助手，只能回答常见问题。",
      );

      const list = (stored.value.agents as { list: Array<{ id: string; instructions?: string }> }).list;
      const entry = list.find((e) => e.id === "wechat-service-default-dm-oabc");
      expect(entry).toBeDefined();
      expect(entry!.instructions).toBe("你是客服助手，只能回答常见问题。");
    });

    it("updates instructions when they change on existing agent", async () => {
      const stored: { value: Record<string, unknown> } = {
        value: {
          agents: {
            list: [
              { id: "main" },
              { id: "wechat-service-default-dm-oabc", instructions: "old instructions" },
            ],
          },
        },
      };
      const runtime = {
        config: {
          loadConfig: () => stored.value,
          writeConfigFile: vi.fn(async (next: unknown) => {
            stored.value = next as Record<string, unknown>;
          }),
        },
      };

      await ensureDynamicAgentListed(
        "wechat-service-default-dm-oabc",
        runtime,
        "new instructions",
      );

      expect(runtime.config.writeConfigFile).toHaveBeenCalledTimes(1);
      const list = (stored.value.agents as { list: Array<{ id: string; instructions?: string }> }).list;
      const entry = list.find((e) => e.id === "wechat-service-default-dm-oabc");
      expect(entry!.instructions).toBe("new instructions");
    });

    it("does not re-write when instructions unchanged", async () => {
      const stored: { value: Record<string, unknown> } = {
        value: {
          agents: {
            list: [
              { id: "main" },
              { id: "wechat-service-default-dm-oabc", instructions: "same instructions" },
            ],
          },
        },
      };
      const runtime = {
        config: {
          loadConfig: () => stored.value,
          writeConfigFile: vi.fn(async (next: unknown) => {
            stored.value = next as Record<string, unknown>;
          }),
        },
      };

      resetEnsuredCache();
      await ensureDynamicAgentListed(
        "wechat-service-default-dm-oabc",
        runtime,
        "same instructions",
      );

      expect(runtime.config.writeConfigFile).not.toHaveBeenCalled();
    });
  });
});
