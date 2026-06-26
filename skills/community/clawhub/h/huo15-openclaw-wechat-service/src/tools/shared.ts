/**
 * Agent tool 共享工具：
 *  - 解析 accountId 到 ResolvedWechatServiceAccount
 *  - 构造 JSON tool result
 *  - 统一错误包装
 */

import type { OpenClawConfig } from "openclaw/plugin-sdk";

import { accessTokenHandleFor, type AccessTokenHandle } from "../access-token.js";
import {
  resolveWechatServiceAccount,
  listWechatServiceAccountIds,
  resolveDefaultWechatServiceAccountId,
} from "../config/accounts.js";
import { checkAuthorization } from "../shared/authorization.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type ToolContext = {
  accountId?: string;
  agentAccountId?: string;
  agentId?: string;
  /** Trusted sender openid from inbound runtime context */
  requesterSenderId?: string;
  /** Whether the trusted sender is registered as OpenClaw owner */
  senderIsOwner?: boolean;
  messageChannel?: string;
  config?: OpenClawConfig;
  runtimeConfig?: OpenClawConfig;
};

export type ResolvedHandle = {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
};

function readConfig(ctx: ToolContext, apiConfig?: OpenClawConfig): OpenClawConfig {
  const cfg = ctx.runtimeConfig ?? ctx.config ?? apiConfig;
  if (!cfg) {
    throw new Error("[wechat-service] tool invoked without an OpenClawConfig context");
  }
  return cfg;
}

function pickRequestedAccountId(
  ctx: ToolContext,
  explicit: string | undefined,
  cfg: OpenClawConfig,
): string {
  const trimmed = (explicit ?? "").trim();
  if (trimmed) return trimmed;
  const fromCtx = (ctx.agentAccountId || ctx.accountId || "").trim();
  if (fromCtx) return fromCtx;
  return resolveDefaultWechatServiceAccountId(cfg);
}

/**
 * 把 tool params.accountId / toolContext.agentAccountId 解析成 ResolvedWechatServiceAccount。
 * 未配置时抛错提示可用的 accountId。
 */
export function resolveToolAccount(params: {
  ctx: ToolContext;
  apiConfig?: OpenClawConfig;
  explicitAccountId?: string;
}): ResolvedHandle {
  const cfg = readConfig(params.ctx, params.apiConfig);
  const accountId = pickRequestedAccountId(params.ctx, params.explicitAccountId, cfg);
  const account = resolveWechatServiceAccount({ cfg, accountId });
  if (!account.configured) {
    const available = listWechatServiceAccountIds(cfg);
    throw new Error(
      `[wechat-service] accountId "${accountId}" not configured. Available: ${available.join(", ") || "(none)"}. Run /setup wechat-service first.`,
    );
  }
  return { account, tokenHandle: accessTokenHandleFor(account) };
}

export type ToolResult = {
  content: Array<{ type: "text"; text: string }>;
  details: unknown;
  isError?: boolean;
};

export function buildToolResult(payload: Record<string, unknown>): ToolResult {
  return {
    content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    details: payload,
  };
}

export function buildErrorResult(payload: {
  action?: string;
  error: string;
  [key: string]: unknown;
}): ToolResult {
  const body: Record<string, unknown> = { ok: false, ...payload };
  return {
    content: [{ type: "text", text: JSON.stringify(body, null, 2) }],
    details: body,
    isError: true,
  };
}

export function asErrorMessage(err: unknown): string {
  return err instanceof Error ? err.message : String(err);
}

/**
 * **assertAuthorized** —— v2.1.0+ 权限闸门。
 *
 * 在每个 tool 的 `execute()` 拿到 account 之后立刻调一次：
 *
 *   const denied = assertAuthorized({ ctx, apiConfig: api.config, toolName, action, accountId });
 *   if (denied) return denied;
 *
 * 默认 permissionMode=open（所有 agent 全权限）；用户若设
 * `dynamicAgents.permissionMode = "admin-only"`，写操作仅放行 main agent /
 * dynamicAgents.adminUsers / OpenClaw owner，其他动态 agent 调写操作直接返回
 * 结构化错误 ToolResult。
 *
 * 详见 `src/shared/authorization.ts`。
 */
export function assertAuthorized(params: {
  ctx: ToolContext;
  apiConfig?: OpenClawConfig;
  toolName: string;
  action: string;
  accountId: string;
}): ToolResult | null {
  const cfg = params.ctx.runtimeConfig ?? params.ctx.config ?? params.apiConfig;
  if (!cfg) return null; // 缺 cfg → 防御性放行（不阻断业务）
  const decision = checkAuthorization({
    cfg,
    toolContext: {
      agentId: params.ctx.agentId,
      requesterSenderId: params.ctx.requesterSenderId,
      senderIsOwner: params.ctx.senderIsOwner,
    },
    accountId: params.accountId,
    toolName: params.toolName,
    action: params.action,
  });
  if (decision.allowed) return null;
  return buildErrorResult({
    action: params.action,
    error: decision.reason,
    permissionMode: "admin-only",
    agentId: params.ctx.agentId ?? null,
    requesterSenderId: params.ctx.requesterSenderId ?? null,
  });
}

/**
 * 公共的 accountId JSON schema 片段：所有 tool 参数里都可以复用。
 */
export const ACCOUNT_ID_SCHEMA_PROPERTY = {
  type: "string",
  description:
    "目标公众号 accountId（channels[\"wechat-service\"].accounts.* 的 key）。不传则使用默认账号或当前 agent 绑定的账号。",
} as const;
