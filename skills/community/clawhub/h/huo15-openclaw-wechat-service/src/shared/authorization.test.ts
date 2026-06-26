/**
 * 权限控制（authorization）回归测试。
 *
 * 关键不变量：
 *  1. permissionMode 默认 "open" → 全部放行（v0.x ~ v2.0 backward-compat）
 *  2. permissionMode = "admin-only" 下 read action 放行，write action 仅 main / admin
 *  3. main agent 识别（"main" / 不匹配 dynamic 模式 / wechat-service-...-no-dm）都视为 main
 *  4. dynamic agentId 解析 openid 与 generateAgentId() 同 sanitize 策略
 *  5. adminUsers 大小写不敏感匹配
 *  6. requesterSenderId（trusted）优先于 agentId 解析的 openid
 *  7. senderIsOwner=true 直接放行
 *  8. legacy "wechatService" key（v1.0.0 之前）也读取（兜底）
 */
import { describe, expect, it } from "vitest";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import {
  categorizeAction,
  checkAuthorization,
  extractOpenidFromAgentId,
  getPermissionMode,
  isAdminUser,
  isMainAgent,
  TOOL_ACTION_CATEGORIES,
} from "./authorization.js";

function cfgWithDynamicAgents(overrides: Record<string, unknown>): OpenClawConfig {
  return {
    channels: {
      "wechat-service": {
        dynamicAgents: overrides,
      },
    },
  } as unknown as OpenClawConfig;
}

function cfgWithLegacyKey(overrides: Record<string, unknown>): OpenClawConfig {
  return {
    channels: {
      wechatService: { dynamicAgents: overrides },
    },
  } as unknown as OpenClawConfig;
}

// ============================================================================

describe("isMainAgent", () => {
  it('"main" → true', () => expect(isMainAgent("main")).toBe(true));
  it('"MAIN" 大小写不敏感', () => expect(isMainAgent("MAIN")).toBe(true));
  it('"wechat-service-main" → true', () =>
    expect(isMainAgent("wechat-service-main")).toBe(true));
  it("非 wechat-service 前缀的 agent → 视为 main（外部 agent）", () => {
    expect(isMainAgent("agent-x")).toBe(true);
    expect(isMainAgent("plugin-agent")).toBe(true);
  });
  it("wechat-service-{acc}-dm-{openid} → false（dynamic agent）", () => {
    expect(isMainAgent("wechat-service-default-dm-oabc123")).toBe(false);
  });
  it("wechat-service-something-没有-dm- → 不是 dynamic → main", () => {
    expect(isMainAgent("wechat-service-default")).toBe(true);
  });
  it("空 / undefined → false（保守）", () => {
    expect(isMainAgent(undefined)).toBe(false);
    expect(isMainAgent("")).toBe(false);
    expect(isMainAgent(null)).toBe(false);
  });
});

describe("extractOpenidFromAgentId", () => {
  it("standard pattern → 解出 openid", () => {
    expect(extractOpenidFromAgentId("wechat-service-default-dm-oABC123", "default")).toBe(
      "oabc123",
    );
  });
  it("非 default 账号", () => {
    expect(extractOpenidFromAgentId("wechat-service-shop-a-dm-xyz789", "shop-a")).toBe(
      "xyz789",
    );
  });
  it("accountId 走相同 sanitize（大小写 + 非 [a-z0-9_-] → _）", () => {
    expect(
      extractOpenidFromAgentId("wechat-service-shop_a-dm-xyz", "Shop_A"),
    ).toBe("xyz");
  });
  it("非 dynamic agent → undefined", () => {
    expect(extractOpenidFromAgentId("main", "default")).toBeUndefined();
    expect(extractOpenidFromAgentId("plugin-agent", "default")).toBeUndefined();
  });
  it("空 → undefined", () => {
    expect(extractOpenidFromAgentId(undefined, "default")).toBeUndefined();
    expect(extractOpenidFromAgentId("", "default")).toBeUndefined();
  });
});

describe("isAdminUser", () => {
  it("openid 在 list 里 → true", () => {
    const cfg = cfgWithDynamicAgents({ adminUsers: ["oABC", "oDEF"] });
    expect(isAdminUser(cfg, "oABC")).toBe(true);
  });
  it("大小写不敏感", () => {
    const cfg = cfgWithDynamicAgents({ adminUsers: ["oABC"] });
    expect(isAdminUser(cfg, "OABC")).toBe(true);
    expect(isAdminUser(cfg, "oabc")).toBe(true);
  });
  it("不在 list → false", () => {
    const cfg = cfgWithDynamicAgents({ adminUsers: ["oABC"] });
    expect(isAdminUser(cfg, "oXYZ")).toBe(false);
  });
  it("空 list → false", () => {
    expect(isAdminUser(cfgWithDynamicAgents({}), "oABC")).toBe(false);
    expect(isAdminUser(cfgWithDynamicAgents({ adminUsers: [] }), "oABC")).toBe(false);
  });
  it("空 openid → false", () => {
    expect(isAdminUser(cfgWithDynamicAgents({ adminUsers: ["oABC"] }), "")).toBe(false);
  });
  it("legacy 'wechatService' key 也读", () => {
    const cfg = cfgWithLegacyKey({ adminUsers: ["oABC"] });
    expect(isAdminUser(cfg, "oABC")).toBe(true);
  });
});

describe("getPermissionMode", () => {
  it("默认 'open'", () => {
    expect(getPermissionMode({} as OpenClawConfig)).toBe("open");
    expect(getPermissionMode(cfgWithDynamicAgents({}))).toBe("open");
  });
  it("显式 'admin-only'", () => {
    expect(
      getPermissionMode(cfgWithDynamicAgents({ permissionMode: "admin-only" })),
    ).toBe("admin-only");
  });
  it("无效值 fallback 到 'open'", () => {
    expect(
      getPermissionMode(cfgWithDynamicAgents({ permissionMode: "yolo" } as unknown as Record<string, unknown>)),
    ).toBe("open");
  });
  it("legacy key", () => {
    expect(getPermissionMode(cfgWithLegacyKey({ permissionMode: "admin-only" }))).toBe(
      "admin-only",
    );
  });
});

describe("categorizeAction", () => {
  it("已注册的 read action → read", () => {
    expect(categorizeAction("wechat_service_message", "list_templates")).toBe("read");
    expect(categorizeAction("wechat_service_menu", "get")).toBe("read");
    expect(categorizeAction("wechat_service_oauth", "build_authorize_url")).toBe("read");
  });
  it("未注册的 action 默认 write（more conservative）", () => {
    expect(categorizeAction("wechat_service_message", "send_text")).toBe("write");
    expect(categorizeAction("wechat_service_mass_send", "send_by_tag")).toBe("write");
    expect(categorizeAction("wechat_service_card", "create")).toBe("write");
  });
  it("未知 tool 默认 write", () => {
    expect(categorizeAction("wechat_service_unknown", "anything")).toBe("write");
  });
  it("REGISTRY 键名约束（防止笔误）", () => {
    expect(Object.keys(TOOL_ACTION_CATEGORIES)).toContain("wechat_service_message");
    expect(Object.keys(TOOL_ACTION_CATEGORIES)).toContain("wechat_service_oauth");
    expect(Object.keys(TOOL_ACTION_CATEGORIES)).toContain("wechat_service_analytics");
  });
});

// ============================================================================
// checkAuthorization 决策树（核心）
// ============================================================================

describe("checkAuthorization decision tree", () => {
  describe("permissionMode = 'open'（默认）", () => {
    it("write action from dynamic agent → 放行（backward-compat）", () => {
      const result = checkAuthorization({
        cfg: cfgWithDynamicAgents({ adminUsers: [] }), // 没设 permissionMode
        toolContext: { agentId: "wechat-service-default-dm-oXYZ" },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(true);
    });
  });

  describe("permissionMode = 'admin-only' + read action", () => {
    it("read action 始终放行", () => {
      const result = checkAuthorization({
        cfg: cfgWithDynamicAgents({ permissionMode: "admin-only", adminUsers: [] }),
        toolContext: { agentId: "wechat-service-default-dm-oXYZ" },
        accountId: "default",
        toolName: "wechat_service_analytics",
        action: "query",
      });
      expect(result.allowed).toBe(true);
    });
  });

  describe("permissionMode = 'admin-only' + write action", () => {
    const cfg = cfgWithDynamicAgents({
      permissionMode: "admin-only",
      adminUsers: ["oADMIN"],
    });

    it("main agent → 放行", () => {
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "main" },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(true);
    });

    it("dynamic agent，sender 在 adminUsers → 放行", () => {
      const result = checkAuthorization({
        cfg,
        toolContext: {
          agentId: "wechat-service-default-dm-oadmin",
          requesterSenderId: "oADMIN",
        },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(true);
    });

    it("dynamic agent，sender NOT in adminUsers → 拒绝", () => {
      const result = checkAuthorization({
        cfg,
        toolContext: {
          agentId: "wechat-service-default-dm-onormal",
          requesterSenderId: "oNORMAL",
        },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(false);
      if (!result.allowed) {
        expect(result.reason).toContain("admin/write");
        expect(result.reason).toContain("oNORMAL");
        expect(result.reason).toContain("admin-only");
      }
    });

    it("senderIsOwner=true → 放行（OpenClaw 全局 owner）", () => {
      const result = checkAuthorization({
        cfg,
        toolContext: {
          agentId: "wechat-service-default-dm-onormal",
          senderIsOwner: true,
        },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(true);
    });

    it("agentId fallback 解析（无 requesterSenderId 时）→ 仍能从 agentId 拿 openid 比对", () => {
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "wechat-service-default-dm-oadmin" },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(true);
    });

    it("send_text（write）从普通 dynamic agent → 拒绝", () => {
      const result = checkAuthorization({
        cfg,
        toolContext: {
          agentId: "wechat-service-default-dm-onormal",
          requesterSenderId: "oNORMAL",
        },
        accountId: "default",
        toolName: "wechat_service_message",
        action: "send_text",
      });
      expect(result.allowed).toBe(false);
    });

    it("list_templates（read）从普通 dynamic agent → 放行", () => {
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "wechat-service-default-dm-onormal" },
        accountId: "default",
        toolName: "wechat_service_message",
        action: "list_templates",
      });
      expect(result.allowed).toBe(true);
    });
  });

  describe("跨账号 dynamic agent 解析", () => {
    it("agent 是 shop-a 账号的 dynamic，但 cfg 在 shop-a 配 adminUsers", () => {
      const cfg = {
        channels: {
          "wechat-service": {
            dynamicAgents: {
              permissionMode: "admin-only",
              adminUsers: ["oadmin"],
            },
          },
        },
      } as unknown as OpenClawConfig;
      // dynamicAgents 是全局的（跨账号），所以 shop-a 的 admin 解析到 oadmin
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "wechat-service-shop-a-dm-oadmin" },
        accountId: "shop-a",
        toolName: "wechat_service_card",
        action: "create",
      });
      expect(result.allowed).toBe(true);
    });

    it("role-based 未配置时继续使用 open 模式", () => {
      const cfg = { channels: { "wechat-service": { dynamicAgents: {} } } } as unknown as OpenClawConfig;
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "wechat-service-default-dm-onormal" },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(true);
    });
  });

  // ============================================================================
  // role-based 模式决策树
  // ============================================================================

  describe("permissionMode = 'role-based'", () => {
    it("superadmin（adminUsers fallback）放行写操作", () => {
      const cfg = {
        channels: {
          "wechat-service": {
            dynamicAgents: {
              permissionMode: "role-based",
              adminUsers: ["oAdmin"],
            },
          },
        },
      } as unknown as OpenClawConfig;
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "wechat-service-default-dm-oadmin" },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(true);
    });

    it("customer 角色拒绝写操作", () => {
      const cfg = {
        channels: {
          "wechat-service": {
            dynamicAgents: {
              permissionMode: "role-based",
            },
          },
        },
      } as unknown as OpenClawConfig;
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "wechat-service-default-dm-onormal" },
        accountId: "default",
        toolName: "wechat_service_mass_send",
        action: "send_by_tag",
      });
      expect(result.allowed).toBe(false);
    });

    it("customer 角色放行 oauth", () => {
      const cfg = {
        channels: {
          "wechat-service": {
            dynamicAgents: {
              permissionMode: "role-based",
            },
          },
        },
      } as unknown as OpenClawConfig;
      const result = checkAuthorization({
        cfg,
        toolContext: { agentId: "wechat-service-default-dm-onormal" },
        accountId: "default",
        toolName: "wechat_service_oauth",
        action: "build_authorize_url",
      });
      expect(result.allowed).toBe(true);
    });

    it("getPermissionMode 返回 'role-based'", () => {
      expect(
        getPermissionMode({
          channels: {
            "wechat-service": {
              dynamicAgents: { permissionMode: "role-based" },
            },
          },
        } as unknown as OpenClawConfig),
      ).toBe("role-based");
    });
  });
});
