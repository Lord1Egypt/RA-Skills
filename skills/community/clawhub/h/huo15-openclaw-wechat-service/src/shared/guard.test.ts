/**
 * AI 对话护栏模块回归测试。
 *
 * 关键不变量：
 *  1. buildRoleGuardPrompt 为不同角色生成不同护栏
 *  2. superadmin/admin 护栏包含"全部管理权限"
 *  3. customer 护栏包含"仅限管理员使用"
 *  4. editor/operator 护栏包含允许和禁止的能力清单
 *  5. resolveAgentInstructions 仅在 role-based 模式下返回护栏
 *  6. injectGuardToEnvelope 在 role-based 模式下拼接护栏
 *  7. open/admin-only 模式下不注入护栏
 */
import { describe, expect, it } from "vitest";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import {
  buildRoleGuardPrompt,
  injectGuardToEnvelope,
  resolveAgentInstructions,
} from "./guard.js";

function makeCfg(overrides: Record<string, unknown> = {}): OpenClawConfig {
  return {
    channels: {
      "wechat-service": { dynamicAgents: overrides },
    },
  } as unknown as OpenClawConfig;
}

// ============================================================================
// buildRoleGuardPrompt
// ============================================================================

describe("buildRoleGuardPrompt", () => {
  it("superadmin 护栏包含全部管理权限", () => {
    const prompt = buildRoleGuardPrompt({
      roleName: "superadmin",
      cfg: makeCfg(),
      accountName: "测试号",
    });
    expect(prompt).toContain("AI 超级管理员");
    expect(prompt).toContain("测试号");
    expect(prompt).toContain("全部管理权限");
    expect(prompt).toContain("自定义菜单");
    expect(prompt).toContain("群发");
  });

  it("admin 护栏与 superadmin 类似", () => {
    const prompt = buildRoleGuardPrompt({
      roleName: "admin",
      cfg: makeCfg(),
      accountName: "测试号",
    });
    expect(prompt).toContain("AI 管理员");
    expect(prompt).toContain("全部管理权限");
  });

  it("customer 护栏包含拒绝话术", () => {
    const prompt = buildRoleGuardPrompt({
      roleName: "customer",
      cfg: makeCfg(),
      accountName: "测试号",
    });
    expect(prompt).toContain("AI 客服助手");
    expect(prompt).toContain("普通用户");
    expect(prompt).toContain("仅限管理员使用");
    expect(prompt).toContain("后台管理操作需要管理员权限");
    // 不应该包含管理权限内容
    expect(prompt).not.toContain("自定义菜单");
  });

  it("editor 护栏包含内容管理和拒绝话术", () => {
    const prompt = buildRoleGuardPrompt({
      roleName: "editor",
      cfg: makeCfg(),
      accountName: "测试号",
    });
    expect(prompt).toContain("内容编辑");
    expect(prompt).toContain("内容编辑助手");
    expect(prompt).toContain("不能执行");
  });

  it("operator 护栏包含客服运营边界", () => {
    const prompt = buildRoleGuardPrompt({
      roleName: "operator",
      cfg: makeCfg(),
      accountName: "测试号",
    });
    expect(prompt).toContain("客服运营");
    expect(prompt).toContain("客服运营助手");
    expect(prompt).toContain("不能执行");
  });

  it("未知角色按 customer 处理", () => {
    const prompt = buildRoleGuardPrompt({
      roleName: "unknown-xyz",
      cfg: makeCfg(),
      accountName: "测试号",
    });
    expect(prompt).toContain("AI 客服助手");
    expect(prompt).toContain("普通用户");
  });

  it("默认公众号名称", () => {
    const prompt = buildRoleGuardPrompt({
      roleName: "customer",
      cfg: makeCfg(),
    });
    expect(prompt).toContain("此公众号");
  });
});

// ============================================================================
// resolveAgentInstructions
// ============================================================================

describe("resolveAgentInstructions", () => {
  it("role-based 模式下返回护栏 prompt", () => {
    const instructions = resolveAgentInstructions({
      openid: "oCustomer",
      accountId: "default",
      cfg: makeCfg({ permissionMode: "role-based" }),
      accountName: "测试号",
    });
    expect(instructions).toBeDefined();
    expect(instructions).toContain("AI 客服助手");
  });

  // v2.3.0 起：non-role-based 模式默认注入 IT 学习客服 persona
  it("admin-only 模式下注入默认 IT persona（v2.3.0+）", () => {
    const instructions = resolveAgentInstructions({
      openid: "oUser",
      accountId: "default",
      cfg: makeCfg({ permissionMode: "admin-only" }),
    });
    expect(instructions).toBeDefined();
    expect(instructions).toContain("IT 领域学习陪伴客服");
  });

  it("open 模式下注入默认 IT persona（v2.3.0+）", () => {
    const instructions = resolveAgentInstructions({
      openid: "oUser",
      accountId: "default",
      cfg: makeCfg({ permissionMode: "open" }),
    });
    expect(instructions).toBeDefined();
    expect(instructions).toContain("OpenClaw");
  });

  it("默认（无 permissionMode）注入默认 IT persona（v2.3.0+）", () => {
    const instructions = resolveAgentInstructions({
      openid: "oUser",
      accountId: "default",
      cfg: makeCfg({}),
    });
    expect(instructions).toBeDefined();
    expect(instructions).toContain("IT");
  });

  it("defaultInstructionsPreset='none' 时不注入 persona", () => {
    const instructions = resolveAgentInstructions({
      openid: "oUser",
      accountId: "default",
      cfg: makeCfg({ permissionMode: "open", defaultInstructionsPreset: "none" }),
    });
    expect(instructions).toBeUndefined();
  });

  it("admin 用户返回全权限护栏", () => {
    const instructions = resolveAgentInstructions({
      openid: "oAdmin",
      accountId: "default",
      cfg: makeCfg({
        permissionMode: "role-based",
        adminUsers: ["oAdmin"],
      }),
    });
    expect(instructions).toBeDefined();
    expect(instructions).toContain("全部管理权限");
  });
});

// ============================================================================
// injectGuardToEnvelope
// ============================================================================

describe("injectGuardToEnvelope", () => {
  it("role-based 模式下 customer 消息拼接护栏", () => {
    const result = injectGuardToEnvelope({
      body: "帮我改下菜单",
      openid: "oCustomer",
      cfg: makeCfg({ permissionMode: "role-based" }),
      accountName: "测试号",
    });
    expect(result).toContain("AI 客服助手");
    expect(result).toContain("用户消息：帮我改下菜单");
    expect(result).toContain("---");
  });

  it("role-based 模式下 admin 消息不注入护栏", () => {
    const result = injectGuardToEnvelope({
      body: "帮我改下菜单",
      openid: "oAdmin",
      cfg: makeCfg({
        permissionMode: "role-based",
        adminUsers: ["oAdmin"],
      }),
    });
    // admin 不需要护栏，直接返回原消息
    expect(result).toBe("帮我改下菜单");
    expect(result).not.toContain("AI 客服助手");
  });

  it("open 模式下不注入护栏", () => {
    const result = injectGuardToEnvelope({
      body: "hello",
      openid: "oUser",
      cfg: makeCfg({ permissionMode: "open" }),
    });
    expect(result).toBe("hello");
  });

  it("admin-only 模式下不注入护栏", () => {
    const result = injectGuardToEnvelope({
      body: "hello",
      openid: "oUser",
      cfg: makeCfg({ permissionMode: "admin-only" }),
    });
    expect(result).toBe("hello");
  });
});
