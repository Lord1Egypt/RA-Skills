/**
 * **权限控制（authorization）模块**
 *
 * 设计目标：让"主 agent"或 `dynamicAgents.adminUsers` 列表中的 openid 才能执行
 * **写/admin 类操作**（发文章 / 群发 / 改菜单 / 改用户标签 / 创建卡券 / 给任意用户发消息等），
 * 其他 openid（普通粉丝在动态 agent 里）只能跑**读类操作**（list / get / OCR / OAuth flow / analytics）。
 *
 * **不影响"自然对话"路径**：
 * 当用户和公众号正常对话时，agent 的回复经由 `runtime/dispatcher.ts:dispatchInboundEvent`
 * 直接调 `sendCustomerServiceMessage`，**不走 tool**，因此本模块的 tool 层权限检查不会
 * 阻止粉丝跟公众号正常聊天。
 *
 * 配置（`channels["wechat-service"].dynamicAgents.permissionMode`）:
 *   - `"open"`（默认）—— 所有 agent 可执行所有 action（v0.x ~ v2.0 行为）
 *   - `"admin-only"` —— 写操作仅 main agent 或 adminUsers；读操作放行
 *
 * @since v2.1.0
 */

import type { OpenClawConfig } from "openclaw/plugin-sdk";

import { CONFIG_SECTION_KEY, LEGACY_CONFIG_SECTION_KEY } from "../config/index.js";
import { checkRoleAuthorization } from "./roles.js";

export type PermissionMode = "open" | "admin-only" | "role-based";
export type ActionCategory = "read" | "write";

// ============================================================================
// Tool action 分类
// ============================================================================

/**
 * **TOOL_ACTION_CATEGORIES** —— 12 个 agent tool 的 action 权限分类。
 *
 * 默认值（map 中没列的 action）回退到 `"write"`，更安全。
 * 调整原则：
 *   - read = 不修改 wechat 侧状态、不消耗 / 触发 user 可见动作
 *   - write = 任何修改、发送、群发、CRUD、OCR/Vision（消耗 quota）
 */
export const TOOL_ACTION_CATEGORIES: Readonly<
  Record<string, Readonly<Record<string, ActionCategory>>>
> = Object.freeze({
  wechat_service_message: Object.freeze({
    list_templates: "read",
    list_template_library: "read",
    get_template_library_item: "read",
    get_industry: "read",
    subscribe_get_category: "read",
    subscribe_pub_titles: "read",
    subscribe_pub_keywords: "read",
    subscribe_list_templates: "read",
    // 其余（send_text/image/voice/video/news/mpnews/menu/miniprogram, typing,
    //   send_template, send_subscribe_once, send_subscribe, add_template,
    //   delete_template, set_industry, subscribe_add_template,
    //   subscribe_delete_template）→ write
  }),
  wechat_service_menu: Object.freeze({
    get: "read",
    try_match: "read",
    get_self_menu: "read",
    // create / delete / create_conditional / delete_conditional → write
  }),
  wechat_service_material: Object.freeze({
    list: "read",
    count: "read",
    get_temp: "read",
    get: "read",
    // upload_temp / upload_perm / upload_image / upload_news / update_news / delete_perm → write
  }),
  wechat_service_article: Object.freeze({
    list: "read",
    get: "read",
    batchget: "read",
    count: "read",
    get_publish_status: "read",
    get_published_article: "read",
    // add / update / delete / publish → write
  }),
  wechat_service_user: Object.freeze({
    get_info: "read",
    list_followers: "read",
    list_tag_users: "read",
    get_user_tags: "read",
    get_unionid: "read",
    list_tags: "read",
    // create_tag / update_tag / delete_tag / batch_tag / batch_untag /
    // set_remark / blacklist_users / unblacklist_users → write
  }),
  wechat_service_qrcode: Object.freeze({
    shorten: "read",
    fetch: "read",
    // create → write
  }),
  // wechat_service_mass_send: 全部 write（preview / send_by_openid / send_by_tag / undo）
  wechat_service_jssdk: Object.freeze({
    sign: "read",
    get_ticket: "read",
    // invalidate_ticket → write
  }),
  wechat_service_oauth: Object.freeze({
    // OAuth 是用户自己的授权流程，所有 action 都视为 read（粉丝自己用网页授权登录是合理的）
    build_authorize_url: "read",
    code_to_token: "read",
    refresh_token: "read",
    userinfo: "read",
    validate: "read",
  }),
  wechat_service_analytics: Object.freeze({
    list_metrics: "read",
    query: "read",
  }),
  wechat_service_intelligent: Object.freeze({
    // OCR / 图像处理是无副作用读操作（消耗 wechat 侧 quota，但不修改公众号状态）
    list_visions: "read",
    run: "read",
  }),
  wechat_service_card: Object.freeze({
    get: "read",
    batchget: "read",
    decrypt: "read",
    // create / delete / consume → write
  }),
});

/**
 * 给定 toolName + action 返回分类。未列出的 action 默认 `"write"`（more conservative）。
 */
export function categorizeAction(toolName: string, action: string): ActionCategory {
  return TOOL_ACTION_CATEGORIES[toolName]?.[action] ?? "write";
}

// ============================================================================
// Identity & permission helpers
// ============================================================================

/**
 * 判断 agentId 是否为"主 agent"（非动态派生的）。
 *
 * 规则：
 *   1. 空 / undefined → 不当 main（保守）
 *   2. 字面 "main" / "wechat-service-main" → main
 *   3. 不以 `wechat-service-` 开头 → 视为外部主 agent（譬如 OpenClaw 全局 main）
 *   4. 以 `wechat-service-` 开头但**不**含 `-dm-` → 不是 dynamic agent，按 main 处理
 *   5. 否则 → dynamic agent（按粉丝隔离的）
 */
export function isMainAgent(agentId: string | undefined | null): boolean {
  if (!agentId) return false;
  const lowered = agentId.trim().toLowerCase();
  if (!lowered) return false;
  if (lowered === "main" || lowered === "wechat-service-main") return true;
  if (!lowered.startsWith("wechat-service-")) return true;
  return !lowered.includes("-dm-");
}

/**
 * 从动态 agentId（`wechat-service-{accountId}-dm-{openid}`）抽取 openid。
 * 非 dynamic agent / 模式不匹配 → undefined。
 */
export function extractOpenidFromAgentId(
  agentId: string | undefined | null,
  accountId: string,
): string | undefined {
  if (!agentId) return undefined;
  const lowered = agentId.trim().toLowerCase();
  const sanitizedAccountId = accountId
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_-]/g, "_");
  const prefix = `wechat-service-${sanitizedAccountId}-dm-`;
  if (!lowered.startsWith(prefix)) return undefined;
  const openid = lowered.slice(prefix.length);
  return openid || undefined;
}

/**
 * openid 是否在 `dynamicAgents.adminUsers` 列表里（大小写不敏感）。
 */
export function isAdminUser(
  cfg: OpenClawConfig,
  openid: string | null | undefined,
): boolean {
  const trimmed = openid?.trim();
  if (!trimmed) return false;
  const channels = cfg.channels as Record<string, unknown> | undefined;
  const section =
    (channels?.[CONFIG_SECTION_KEY] as { dynamicAgents?: { adminUsers?: string[] } } | undefined) ??
    (channels?.[LEGACY_CONFIG_SECTION_KEY] as
      | { dynamicAgents?: { adminUsers?: string[] } }
      | undefined);
  const adminUsers = section?.dynamicAgents?.adminUsers ?? [];
  const target = trimmed.toLowerCase();
  return adminUsers.some((u) => String(u).trim().toLowerCase() === target);
}

/**
 * 读取 `dynamicAgents.permissionMode`，默认 `"open"`（v2.0.x 之前的行为）。
 */
export function getPermissionMode(cfg: OpenClawConfig): PermissionMode {
  const channels = cfg.channels as Record<string, unknown> | undefined;
  const section =
    (channels?.[CONFIG_SECTION_KEY] as { dynamicAgents?: { permissionMode?: string } } | undefined) ??
    (channels?.[LEGACY_CONFIG_SECTION_KEY] as
      | { dynamicAgents?: { permissionMode?: string } }
      | undefined);
  const mode = section?.dynamicAgents?.permissionMode;
  if (mode === "admin-only") return "admin-only";
  if (mode === "role-based") return "role-based";
  return "open";
}

// ============================================================================
// Authorization decision
// ============================================================================

export type AuthorizationContext = {
  cfg: OpenClawConfig;
  toolContext: {
    agentId?: string;
    /** Trusted sender openid from inbound runtime context */
    requesterSenderId?: string;
    /** Whether the trusted sender is registered as OpenClaw owner */
    senderIsOwner?: boolean;
  };
  accountId: string;
  toolName: string;
  action: string;
};

export type AuthorizationDecision =
  | { allowed: true; reason?: never }
  | { allowed: false; reason: string };

/**
 * **checkAuthorization** —— 统一权限决策。
 *
 * 决策树：
 *   1. permissionMode === "open" → 全部放行
 *   2. action 是 read 类 → 放行
 *   3. write/admin 类，依次尝试以下白名单：
 *      a. agent 是 main → 放行
 *      b. requesterSenderId（trusted）在 adminUsers → 放行
 *      c. senderIsOwner === true（OpenClaw 全局 owner）→ 放行
 *      d. 从 agentId 解析出的 openid 在 adminUsers → 放行（fallback path）
 *   4. 否则 → 拒绝，附带可读的 reason
 */
export function checkAuthorization(ctx: AuthorizationContext): AuthorizationDecision {
  const mode = getPermissionMode(ctx.cfg);
  if (mode === "open") {
    return { allowed: true };
  }

  // role-based：按角色权限白名单判定（不依赖 read/write 分类）
  if (mode === "role-based") {
    const senderOpenid = ctx.toolContext.requesterSenderId;
    const openidFromAgent = extractOpenidFromAgentId(
      ctx.toolContext.agentId,
      ctx.accountId,
    );
    const effectiveOpenid = senderOpenid ?? openidFromAgent;
    return checkRoleAuthorization({
      cfg: ctx.cfg,
      toolName: ctx.toolName,
      action: ctx.action,
      openid: effectiveOpenid,
      agentId: ctx.toolContext.agentId,
    });
  }

  // admin-only：read 放行，write 仅 main/adminUsers/owner
  const category = categorizeAction(ctx.toolName, ctx.action);
  if (category === "read") {
    return { allowed: true };
  }

  // write/admin: 依次试白名单
  if (isMainAgent(ctx.toolContext.agentId)) {
    return { allowed: true };
  }
  if (
    ctx.toolContext.requesterSenderId &&
    isAdminUser(ctx.cfg, ctx.toolContext.requesterSenderId)
  ) {
    return { allowed: true };
  }
  if (ctx.toolContext.senderIsOwner === true) {
    return { allowed: true };
  }
  const openidFromAgent = extractOpenidFromAgentId(
    ctx.toolContext.agentId,
    ctx.accountId,
  );
  if (openidFromAgent && isAdminUser(ctx.cfg, openidFromAgent)) {
    return { allowed: true };
  }

  // 拒绝
  const senderHint = ctx.toolContext.requesterSenderId ?? openidFromAgent ?? "unknown";
  const agentHint = ctx.toolContext.agentId ?? "unknown";
  return {
    allowed: false,
    reason:
      `[wechat-service] action "${ctx.toolName}.${ctx.action}" 是 admin/write 操作，` +
      `仅"主 agent"或 dynamicAgents.adminUsers 列表中的 openid 可执行（permissionMode=admin-only）。` +
      `当前 agentId=${agentHint} sender=${senderHint}。` +
      `如需放行该用户，请把 openid 加入 channels["wechat-service"].dynamicAgents.adminUsers。`,
  };
}
