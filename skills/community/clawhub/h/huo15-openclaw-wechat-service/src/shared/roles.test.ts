/**
 * 角色权限系统回归测试。
 *
 * 关键不变量：
 *  1. resolveUserRole 正确匹配 openid → 角色
 *  2. adminUsers 向后兼容 → superadmin
 *  3. 未匹配用户使用 defaultRole（默认 "customer"）
 *  4. 内置默认角色权限定义完整
 *  5. checkRoleAuthorization 正确放行/拒绝
 *  6. 用户自定义 rolePermissions 覆盖内置默认
 *  7. "*" 通配符 tool/action 正确工作
 */
import { describe, expect, it } from "vitest";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import {
  checkRoleAuthorization,
  getDefaultRole,
  getRolePermissions,
  getUserRoles,
  resolveUserRole,
} from "./roles.js";

function makeCfg(overrides: Record<string, unknown> = {}): OpenClawConfig {
  return {
    channels: {
      "wechat-service": { dynamicAgents: overrides },
    },
  } as unknown as OpenClawConfig;
}

function makeCfgLegacy(overrides: Record<string, unknown> = {}): OpenClawConfig {
  return {
    channels: {
      wechatService: { dynamicAgents: overrides },
    },
  } as unknown as OpenClawConfig;
}

// ============================================================================
// resolveUserRole
// ============================================================================

describe("resolveUserRole", () => {
  it("匹配 roles 中的 openid → 返回对应角色", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      roles: { editor: ["oEditor1"], operator: ["oOp1"] },
    });
    expect(resolveUserRole(cfg, "oEditor1")).toBe("editor");
    expect(resolveUserRole(cfg, "oOp1")).toBe("operator");
  });

  it("openid 大小写不敏感匹配", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      roles: { editor: ["oEditor1"] },
    });
    expect(resolveUserRole(cfg, "OEDITOR1")).toBe("editor");
  });

  it("未匹配 → 返回 defaultRole（默认 customer）", () => {
    const cfg = makeCfg({ permissionMode: "role-based" });
    expect(resolveUserRole(cfg, "oUnknown")).toBe("customer");
  });

  it("自定义 defaultRole", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      defaultRole: "operator",
    });
    expect(resolveUserRole(cfg, "oUnknown")).toBe("operator");
  });

  it("空 openid → 返回 defaultRole", () => {
    const cfg = makeCfg({ permissionMode: "role-based" });
    expect(resolveUserRole(cfg, "")).toBe("customer");
    expect(resolveUserRole(cfg, null)).toBe("customer");
    expect(resolveUserRole(cfg, undefined)).toBe("customer");
  });

  it("adminUsers 向后兼容 → 自动映射为 superadmin", () => {
    const cfg = makeCfg({
      permissionMode: "admin-only",
      adminUsers: ["oAdmin1"],
    });
    expect(resolveUserRole(cfg, "oAdmin1")).toBe("superadmin");
  });

  it("roles 和 adminUsers 同时配置时不冲突", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      adminUsers: ["oAdmin1"],
      roles: { editor: ["oEditor1"] },
    });
    expect(resolveUserRole(cfg, "oAdmin1")).toBe("superadmin");
    expect(resolveUserRole(cfg, "oEditor1")).toBe("editor");
  });

  it("legacy 'wechatService' key 也读取", () => {
    const cfg = makeCfgLegacy({
      permissionMode: "role-based",
      roles: { editor: ["oEditor1"] },
    });
    expect(resolveUserRole(cfg, "oEditor1")).toBe("editor");
  });
});

// ============================================================================
// getUserRoles
// ============================================================================

describe("getUserRoles", () => {
  it("返回角色映射", () => {
    const roles = getUserRoles(makeCfg({
      roles: { admin: ["oA", "oB"], editor: ["oC"] },
    }));
    expect(roles).toEqual({ admin: ["oA", "oB"], editor: ["oC"] });
  });

  it("adminUsers 合并到 superadmin", () => {
    const roles = getUserRoles(makeCfg({
      adminUsers: ["oA", "oB"],
      roles: { editor: ["oC"] },
    }));
    expect(roles.superadmin).toEqual(["oA", "oB"]);
    expect(roles.editor).toEqual(["oC"]);
  });

  it("adminUsers 与已有 superadmin 去重合并", () => {
    const roles = getUserRoles(makeCfg({
      adminUsers: ["oA", "oB"],
      roles: { superadmin: ["oA", "oC"] },
    }));
    expect(roles.superadmin).toEqual(["oA", "oC", "oB"]);
  });

  it("空配置返回空对象", () => {
    expect(getUserRoles(makeCfg({}))).toEqual({});
  });
});

// ============================================================================
// getDefaultRole
// ============================================================================

describe("getDefaultRole", () => {
  it("默认 'customer'", () => {
    expect(getDefaultRole(makeCfg())).toBe("customer");
  });

  it("自定义 defaultRole", () => {
    expect(getDefaultRole(makeCfg({ defaultRole: "operator" }))).toBe("operator");
  });
});

// ============================================================================
// getRolePermissions
// ============================================================================

describe("getRolePermissions", () => {
  it("superadmin 拥有全部权限（tools: {'*': '*'}）", () => {
    const perms = getRolePermissions(makeCfg(), "superadmin");
    expect(perms.tools).toBeDefined();
    expect(perms.tools!["*"]).toBe("*");
  });

  it("customer 只有最小权限", () => {
    const perms = getRolePermissions(makeCfg(), "customer");
    expect(perms.tools!["wechat_service_oauth"]).toBe("*");
    expect(perms.tools!["wechat_service_jssdk"]).toEqual(["sign"]);
  });

  it("用户自定义覆盖内置默认", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      rolePermissions: {
        customer: { tools: { wechat_service_message: ["list_templates"] } },
      },
    });
    const perms = getRolePermissions(cfg, "customer");
    // 用户自定义完全覆盖
    expect(perms.tools!["wechat_service_message"]).toEqual(["list_templates"]);
    expect(perms.tools!["wechat_service_oauth"]).toBeUndefined();
  });

  it("未知角色回退到 customer 权限", () => {
    const perms = getRolePermissions(makeCfg(), "unknown-role");
    expect(perms.tools!["wechat_service_oauth"]).toBe("*");
  });
});

// ============================================================================
// checkRoleAuthorization
// ============================================================================

describe("checkRoleAuthorization", () => {
  it("superadmin 放行任意 tool/action", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      adminUsers: ["oAdmin"],
    });
    const result = checkRoleAuthorization({
      cfg,
      toolName: "wechat_service_mass_send",
      action: "send_by_tag",
      openid: "oAdmin",
    });
    expect(result.allowed).toBe(true);
  });

  it("customer 拒绝写操作", () => {
    const cfg = makeCfg({ permissionMode: "role-based" });
    const result = checkRoleAuthorization({
      cfg,
      toolName: "wechat_service_mass_send",
      action: "send_by_tag",
      openid: "oCustomer",
    });
    expect(result.allowed).toBe(false);
    if (!result.allowed) {
      expect(result.reason).toContain("customer");
      expect(result.reason).toContain("wechat_service_mass_send");
    }
  });

  it("customer 放行 oauth", () => {
    const cfg = makeCfg({ permissionMode: "role-based" });
    const result = checkRoleAuthorization({
      cfg,
      toolName: "wechat_service_oauth",
      action: "build_authorize_url",
      openid: "oCustomer",
    });
    expect(result.allowed).toBe(true);
  });

  it("editor 放行 article 操作", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      roles: { editor: ["oEditor"] },
    });
    const result = checkRoleAuthorization({
      cfg,
      toolName: "wechat_service_article",
      action: "add",
      openid: "oEditor",
    });
    expect(result.allowed).toBe(true);
  });

  it("editor 拒绝 mass_send 操作", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      roles: { editor: ["oEditor"] },
    });
    const result = checkRoleAuthorization({
      cfg,
      toolName: "wechat_service_mass_send",
      action: "send_by_tag",
      openid: "oEditor",
    });
    expect(result.allowed).toBe(false);
  });

  it("operator 可以 send_text（客服回复）但不能改菜单", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      roles: { operator: ["oOp"] },
    });
    expect(
      checkRoleAuthorization({
        cfg,
        toolName: "wechat_service_message",
        action: "send_text",
        openid: "oOp",
      }).allowed,
    ).toBe(true);

    expect(
      checkRoleAuthorization({
        cfg,
        toolName: "wechat_service_menu",
        action: "create",
        openid: "oOp",
      }).allowed,
    ).toBe(false);
  });

  it("用户自定义 rolePermissions 生效", () => {
    const cfg = makeCfg({
      permissionMode: "role-based",
      roles: { custom: ["oCustom"] },
      rolePermissions: {
        custom: { tools: { wechat_service_menu: "*", wechat_service_article: ["list", "get"] } },
      },
    });
    expect(
      checkRoleAuthorization({
        cfg,
        toolName: "wechat_service_menu",
        action: "create",
        openid: "oCustom",
      }).allowed,
    ).toBe(true);
    expect(
      checkRoleAuthorization({
        cfg,
        toolName: "wechat_service_article",
        action: "list",
        openid: "oCustom",
      }).allowed,
    ).toBe(true);
    expect(
      checkRoleAuthorization({
        cfg,
        toolName: "wechat_service_article",
        action: "publish",
        openid: "oCustom",
      }).allowed,
    ).toBe(false);
  });

  it("拒绝时给出清晰的原因", () => {
    const cfg = makeCfg({ permissionMode: "role-based" });
    const result = checkRoleAuthorization({
      cfg,
      toolName: "wechat_service_menu",
      action: "create",
      openid: "oCustomer",
    });
    expect(result.allowed).toBe(false);
    if (!result.allowed) {
      expect(result.reason).toContain("customer");
      expect(result.reason).toContain("wechat_service_menu");
      expect(result.reason).toContain("rolePermissions");
    }
  });

  it("空 openid 按 customer 处理", () => {
    const cfg = makeCfg({ permissionMode: "role-based" });
    const result = checkRoleAuthorization({
      cfg,
      toolName: "wechat_service_mass_send",
      action: "send_by_tag",
      openid: "",
    });
    expect(result.allowed).toBe(false);
  });
});
