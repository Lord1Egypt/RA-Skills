/**
 * **角色权限系统（v2.2.0+）**
 *
 * 当 `dynamicAgents.permissionMode = "role-based"` 时启用。
 *
 * 核心流程：
 *  1. 从 cfg 读取 roles 映射（角色 → openid 列表）
 *  2. 根据 openid 查找其角色（未匹配则用 defaultRole，默认 "customer"）
 *  3. 从 cfg.rolePermissions 或内置默认权限中获取该角色的 tool/action 白名单
 *  4. 调用 checkRoleAuthorization 判断是否放行
 *
 * 内置默认角色：
 *  - superadmin / admin：全部 tool/action
 *  - editor：内容管理（article*, material*, menu{get,try_match}, message{list*,get*}）
 *  - operator：客服运营（message{send_*,typing,list*,get*} + user{get*,list*} + analytics* + oauth* + jssdk* + qrcode.fetch）
 *  - customer：最小权限（oauth* + jssdk.sign + analytics.list_metrics）
 */

import type { OpenClawConfig } from "openclaw/plugin-sdk";

import { CONFIG_SECTION_KEY, LEGACY_CONFIG_SECTION_KEY } from "../config/index.js";
import type { RoleToolPermissions } from "../types.js";
import { categorizeAction } from "./authorization.js";
import type { AuthorizationDecision } from "./authorization.js";

// ============================================================================
// 内置默认角色权限
// ============================================================================

const DEFAULT_ROLE_PERMISSIONS = Object.freeze<Record<string, RoleToolPermissions>>({
  superadmin: Object.freeze({
    tools: { "*": "*" },
  }),
  admin: Object.freeze({
    tools: { "*": "*" },
  }),
  editor: Object.freeze({
    tools: {
      wechat_service_article: "*",
      wechat_service_material: "*",
      wechat_service_menu: ["get", "try_match"],
      wechat_service_message: [
        "list_templates",
        "list_template_library",
        "get_template_library_item",
        "get_industry",
      ],
    },
  }),
  operator: Object.freeze({
    tools: {
      wechat_service_message: [
        "send_text",
        "send_image",
        "send_voice",
        "send_video",
        "send_news",
        "send_mpnews",
        "send_menu",
        "send_miniprogram",
        "typing",
        "list_templates",
        "list_template_library",
        "get_template_library_item",
        "get_industry",
      ],
      wechat_service_user: [
        "get_info",
        "list_followers",
        "get_user_tags",
        "get_unionid",
        "list_tags",
        "list_tag_users",
      ],
      wechat_service_analytics: "*",
      wechat_service_oauth: "*",
      wechat_service_jssdk: ["sign", "get_ticket"],
      wechat_service_qrcode: ["fetch"],
      wechat_service_intelligent: ["list_visions", "run"],
    },
  }),
  customer: Object.freeze({
    tools: {
      wechat_service_oauth: "*",
      wechat_service_jssdk: ["sign"],
      wechat_service_analytics: ["list_metrics"],
    },
  }),
});

// ============================================================================
// 配置读取
// ============================================================================

function readDynamicAgentsSection(
  cfg: OpenClawConfig,
): Record<string, unknown> | undefined {
  const channels = (cfg as { channels?: Record<string, unknown> })?.channels;
  return (
    (channels?.[CONFIG_SECTION_KEY] as Record<string, unknown> | undefined) ??
    (channels?.[LEGACY_CONFIG_SECTION_KEY] as Record<string, unknown> | undefined)
  );
}

function readDynamicAgentsConfig(
  cfg: OpenClawConfig,
): Record<string, unknown> | undefined {
  const section = readDynamicAgentsSection(cfg);
  return section?.dynamicAgents as Record<string, unknown> | undefined;
}

// ============================================================================
// 角色解析
// ============================================================================

/**
 * 读取用户配置的角色映射（角色名 → openid 列表）。
 */
export function getUserRoles(
  cfg: OpenClawConfig,
): Record<string, string[]> {
  const da = readDynamicAgentsConfig(cfg) ?? {};
  const roles = da.roles;
  const result: Record<string, string[]> = {};

  if (roles && typeof roles === "object") {
    for (const [role, openids] of Object.entries(roles as Record<string, unknown>)) {
      if (Array.isArray(openids)) {
        result[role] = openids.map((v) => String(v).trim()).filter(Boolean);
      }
    }
  }

  // 向后兼容：adminUsers 映射为 superadmin 角色
  const adminUsers = da.adminUsers;
  if (Array.isArray(adminUsers) && adminUsers.length > 0) {
    const existing = result["superadmin"] ?? [];
    const adminList = adminUsers.map((v) => String(v).trim()).filter(Boolean);
    result["superadmin"] = [...new Set([...existing, ...adminList])];
  }

  return result;
}

/**
 * 读取用户配置的角色权限（角色名 → RoleToolPermissions）。
 */
export function getUserRolePermissions(
  cfg: OpenClawConfig,
): Record<string, RoleToolPermissions> {
  const da = readDynamicAgentsConfig(cfg) ?? {};
  const rp = da.rolePermissions;
  if (!rp || typeof rp !== "object") return {};
  return rp as Record<string, RoleToolPermissions>;
}

/**
 * 获取默认角色名（未匹配用户的兜底角色）。
 */
export function getDefaultRole(cfg: OpenClawConfig): string {
  const da = readDynamicAgentsConfig(cfg) ?? {};
  const defaultRole = da.defaultRole;
  if (typeof defaultRole === "string" && defaultRole.trim()) {
    return defaultRole.trim();
  }
  return "customer";
}

/**
 * 根据 openid 解析用户角色。
 *
 * 查找顺序：
 *  1. 遍历 roles 映射，找到包含该 openid 的角色
 *  2. 检查 adminUsers 列表（向后兼容 → superadmin）
 *  3. 未匹配 → 返回 defaultRole（默认 "customer"）
 */
export function resolveUserRole(
  cfg: OpenClawConfig,
  openid: string | null | undefined,
): string {
  const trimmed = openid?.trim();
  if (!trimmed) return getDefaultRole(cfg);

  const roles = getUserRoles(cfg);
  const target = trimmed.toLowerCase();
  for (const [role, openids] of Object.entries(roles)) {
    if (openids.some((id) => id.toLowerCase() === target)) {
      return role;
    }
  }

  return getDefaultRole(cfg);
}

// ============================================================================
// 角色权限查询
// ============================================================================

/**
 * 获取某个角色的最终权限（用户配置优先，fallback 到内置默认）。
 */
export function getRolePermissions(
  cfg: OpenClawConfig,
  roleName: string,
): RoleToolPermissions {
  const userDefined = getUserRolePermissions(cfg);
  const explicit = userDefined[roleName];
  if (explicit) return explicit;

  const builtin = DEFAULT_ROLE_PERMISSIONS[roleName];
  if (builtin) return builtin as RoleToolPermissions;

  // 未知角色 → 回退到 customer 权限（最安全）
  return DEFAULT_ROLE_PERMISSIONS["customer"] as RoleToolPermissions;
}

/**
 * 列出某个角色能访问的 tool action 列表（用于护栏 prompt 生成）。
 */
export function listRoleAllowedActions(
  cfg: OpenClawConfig,
  roleName: string,
): Array<{ toolName: string; actions: string[] }> {
  const perms = getRolePermissions(cfg, roleName);
  const tools = perms.tools ?? {};
  const result: Array<{ toolName: string; actions: string[] }> = [];
  for (const [toolName, actions] of Object.entries(tools)) {
    if (toolName === "*") continue; // * 键代表全部 tool，展开无意义
    result.push({
      toolName,
      actions: actions === "*" ? ["*"] : actions,
    });
  }
  return result;
}

// ============================================================================
// 角色鉴权决策
// ============================================================================

export type RoleCheckParams = {
  cfg: OpenClawConfig;
  toolName: string;
  action: string;
  openid: string | null | undefined;
  agentId?: string | null;
};

/**
 * **checkRoleAuthorization** —— 基于角色的 tool 权限决策。
 *
 * 决策流程：
 *  1. 解析 openid → 角色
 *  2. 获取该角色的权限白名单
 *  3. 白名单 tools 中有 "*" 键 → 全部 tool 放行
 *  4. 白名单 tools 中有 toolName → 如果 action 值为 "*" 或包含该 action → 放行
 *  5. 否则 → 拒绝
 *
 * 注意：write action 默认不单独放行 — 只有白名单里显式列出的才能通过。
 */
export function checkRoleAuthorization(params: RoleCheckParams): AuthorizationDecision {
  const { cfg, toolName, action, openid } = params;
  const role = resolveUserRole(cfg, openid);
  const perms = getRolePermissions(cfg, role);
  const tools = perms.tools ?? {};

  // roles 的 tools 支持 "*" 通配符 key：该角色可以操作所有 tool
  const hasGlobalWildcard =
    Object.prototype.hasOwnProperty.call(tools, "*") && tools["*"] === "*";
  if (hasGlobalWildcard) {
    return { allowed: true };
  }

  // 查找该 tool 的白名单
  const toolPerm = tools[toolName];
  if (toolPerm === undefined) {
    return {
      allowed: false,
      reason:
        `[wechat-service] 角色 "${role}" 无权使用 tool "${toolName}"。` +
        `当前权限模式为 role-based，该 tool 不在角色白名单中。` +
        `如需放行，请在 channels["wechat-service"].dynamicAgents.rolePermissions.${role}.tools 中添加 "${toolName}"。`,
    };
  }

  if (toolPerm === "*") {
    return { allowed: true };
  }

  if (Array.isArray(toolPerm) && toolPerm.includes(action)) {
    return { allowed: true };
  }

  return {
    allowed: false,
    reason:
      `[wechat-service] 角色 "${role}" 无权执行 "${toolName}.${action}"。` +
      `该角色在 "${toolName}" 上允许的 action：${Array.isArray(toolPerm) ? toolPerm.join(", ") : "(none)"}。` +
      `如需放行，请在 channels["wechat-service"].dynamicAgents.rolePermissions.${role}.tools.${toolName} 中添加 "${action}"。`,
  };
}

/**
 * 角色名的人类可读中文标签。
 */
export function getRoleLabel(roleName: string): string {
  const labels: Record<string, string> = {
    superadmin: "超级管理员",
    admin: "管理员",
    editor: "内容编辑",
    operator: "客服运营",
    customer: "普通用户",
  };
  return labels[roleName] ?? roleName;
}
