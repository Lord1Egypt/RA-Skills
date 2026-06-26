/**
 * **AI 对话护栏模块（v2.2.0+）**
 *
 * 为动态 agent 生成角色感知的 system instructions，让 AI 在自然对话中就能
 * 判断用户权限，对越权请求给出礼貌的自然语言拒绝，而不是等到 tool 调用时才报技术错误。
 *
 * 护栏 prompt 通过两个路径注入：
 *  1. `resolveAgentInstructions()` → 写入 agent 条目的 `instructions` 字段（持久化）
 *  2. `injectGuardToEnvelope()` → 拼接到每条 inbound 消息的 envelope body 前（运行时）
 */

import type { OpenClawConfig } from "openclaw/plugin-sdk";

import { getRoleLabel, listRoleAllowedActions, resolveUserRole } from "./roles.js";
import { getPermissionMode } from "./authorization.js";
import { getDynamicAgentConfig } from "../dynamic-agent.js";
import { resolvePersonaInstructions } from "./personas/it-support.js";

// ============================================================================
// 护栏 prompt 生成
// ============================================================================

/**
 * 根据角色生成 agent system instructions。
 *
 * 策略：
 *  - customer → 严格客服护栏：只能聊天 + 查信息，管理请求礼貌拒绝
 *  - operator → 客服运营护栏：可回复用户 + 查看分析，但不能管理内容
 *  - editor → 内容编辑护栏：可管理文章/素材，不能操作用户/群发
 *  - admin/superadmin → 全权限，无护栏限制
 *  - 未知角色 → 按 customer 处理（安全兜底）
 */
export function buildRoleGuardPrompt(params: {
  roleName: string;
  cfg: OpenClawConfig;
  accountName?: string;
}): string {
  const { roleName, accountName } = params;
  const label = getRoleLabel(roleName);
  const account = accountName || "此公众号";

  switch (roleName) {
    case "superadmin":
    case "admin":
      return buildAdminGuard(label, account);

    case "editor":
      return buildEditorGuard(label, account, params.cfg);

    case "operator":
      return buildOperatorGuard(label, account, params.cfg);

    case "customer":
    default:
      return buildCustomerGuard(label, account);
  }
}

function buildAdminGuard(label: string, account: string): string {
  return [
    `你是「${account}」的 AI ${label}。`,
    `你拥有公众号的全部管理权限，包括：`,
    `- 管理自定义菜单`,
    `- 发送客服消息、模板消息、订阅通知`,
    `- 管理素材（图片/语音/视频/图文）`,
    `- 草稿箱与文章发布`,
    `- 用户标签管理与群发`,
    `- 数据统计与分析`,
    `- 卡券管理`,
    `- 网页授权与 JS-SDK`,
    ``,
    `请根据用户的具体需求，调用对应的工具完成任务。操作前请确认影响范围，避免误操作。`,
  ].join("\n");
}

function buildEditorGuard(
  label: string,
  account: string,
  cfg: OpenClawConfig,
): string {
  const allowed = listRoleAllowedActions(cfg, "editor");
  const toolList = formatAllowedTools(allowed);
  return [
    `你是「${account}」的 AI ${label}。`,
    `你可以执行以下操作：`,
    ...toolList,
    ``,
    `你不能执行以下操作（如用户请求，请礼貌拒绝）：`,
    `- 向用户发送消息`,
    `- 群发消息`,
    `- 管理用户标签或黑名单`,
    `- 创建卡券`,
    `- 修改用户备注`,
    ``,
    `拒绝话术示例："抱歉，我是内容编辑助手，无法执行此操作。如需群发或用户管理，请联系管理员。"`,
  ].join("\n");
}

function buildOperatorGuard(
  label: string,
  account: string,
  cfg: OpenClawConfig,
): string {
  const allowed = listRoleAllowedActions(cfg, "operator");
  const toolList = formatAllowedTools(allowed);
  return [
    `你是「${account}」的 AI ${label}。`,
    `你可以执行以下操作：`,
    ...toolList,
    ``,
    `你不能执行以下操作（如用户请求，请礼貌拒绝）：`,
    `- 修改自定义菜单`,
    `- 管理素材（上传/删除）`,
    `- 发布或删除文章`,
    `- 群发消息`,
    `- 修改用户标签或黑名单`,
    `- 创建卡券`,
    ``,
    `拒绝话术示例："抱歉，我是客服运营助手，无法修改公众号配置。如需菜单或内容管理，请联系管理员或内容编辑。"`,
  ].join("\n");
}

function buildCustomerGuard(label: string, account: string): string {
  return [
    `你是「${account}」的 AI 客服助手。`,
    `你当前与一位普通用户（${label}）对话。`,
    ``,
    `你可以帮他：`,
    `- 回答关于公众号的常见问题`,
    `- 提供信息查询和咨询`,
    `- 引导用户使用公众号的功能`,
    ``,
    `你不能执行（如用户请求，请礼貌拒绝）：`,
    `- 任何公众号后台管理操作`,
    `- 修改菜单、发布文章、群发消息等`,
    `- 查看其他用户的信息`,
    `- 管理系统配置`,
    ``,
    `拒绝话术示例："抱歉，此功能仅限管理员使用。如需帮助，请联系管理员。"`,
    `如果用户连续请求管理操作，可以补充："我是 AI 客服助手，主要帮你解答常见问题。后台管理操作需要管理员权限，我无法执行哦。"`,
  ].join("\n");
}

function formatAllowedTools(
  allowed: Array<{ toolName: string; actions: string[] }>,
): string[] {
  if (allowed.length === 0) return ["- （无管理工具权限）"];
  const lines: string[] = [];
  for (const { toolName, actions } of allowed) {
    const actionStr = actions.includes("*")
      ? "全部操作"
      : actions.join(", ");
    lines.push(`- ${toolName}：${actionStr}`);
  }
  return lines;
}

// ============================================================================
// Agent instructions 入口
// ============================================================================

/**
 * **resolveAgentInstructions** —— 为动态 agent 生成 instructions。
 *
 *  - `permissionMode = "role-based"`（v2.2.0+）→ 角色护栏 prompt
 *  - 其他模式（open / admin-only）→ v2.3.0+ 注入默认 persona preset（IT 学习客服）
 *  - 用户把 `defaultInstructionsPreset` 设成 `"none"` / `"off"` 时不注入
 *
 * @returns instructions 文本，如果不需要注入则返回 undefined
 */
export function resolveAgentInstructions(params: {
  openid: string;
  accountId: string;
  cfg: OpenClawConfig;
  accountName?: string;
}): string | undefined {
  const mode = getPermissionMode(params.cfg);
  if (mode === "role-based") {
    const role = resolveUserRole(params.cfg, params.openid);
    return buildRoleGuardPrompt({
      roleName: role,
      cfg: params.cfg,
      accountName: params.accountName,
    });
  }

  // open / admin-only 模式：注入默认 persona（v2.3.0+）
  const dynCfg = getDynamicAgentConfig(params.cfg);
  return resolvePersonaInstructions(dynCfg.defaultInstructionsPreset);
}

// ============================================================================
// 运行时护栏注入（注入到 envelope body）
// ============================================================================

/**
 * **injectGuardToEnvelope** —— 将角色护栏拼接到消息信封正文前。
 *
 * 作为 system 指令头部拼在用户原文前，让 agent 在每轮对话中都能看到自己的角色限制。
 * 仅在 permissionMode = "role-based" 时注入。
 *
 * @param body 原始消息正文
 * @param openid 发送者 openid
 * @param cfg 配置
 * @param accountName 公众号名称
 * @returns 拼接了护栏的消息正文
 */
export function injectGuardToEnvelope(params: {
  body: string;
  openid: string;
  cfg: OpenClawConfig;
  accountName?: string;
}): string {
  const mode = getPermissionMode(params.cfg);
  if (mode !== "role-based") return params.body;

  const role = resolveUserRole(params.cfg, params.openid);
  // customer 角色必须注入护栏（因为 customer 本身不能执行任何 tool）
  // admin/superadmin 不需要护栏
  // editor/operator 也需要提醒自己的权限边界
  if (role === "superadmin" || role === "admin") return params.body;

  const guardPrompt = buildRoleGuardPrompt({
    roleName: role,
    cfg: params.cfg,
    accountName: params.accountName,
  });

  return `${guardPrompt}\n\n---\n\n用户消息：${params.body}`;
}
