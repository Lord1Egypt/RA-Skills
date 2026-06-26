/**
 * 上下游企业支持模块
 * 
 * 根据企业微信文档：https://developer.work.weixin.qq.com/document/path/97213
 * 
 * 关键逻辑：
 * 1. 上下游企业消息中的 ToUserName 是下游企业的 CorpID
 * 2. 需要使用下游企业的 access_token 来发送消息
 * 3. 获取下游企业 access_token 的接口：
 *    POST https://qyapi.weixin.qq.com/cgi-bin/corpgroup/corp/gettoken?access_token=ACCESS_TOKEN
 *    {
 *      "corpid": "下游企业corpid",
 *      "business_type": 1,  // 1 表示上下游企业
 *      "agentid": 下游企业应用ID
 *    }
 * 4. 需要使用上游企业的 access_token 作为调用凭证
 */

import type { ResolvedAgentAccount } from "../types/index.js";

export type UpstreamCorpConfig = {
  corpId: string;
  agentId: number;
};

/**
 * 从消息中检测是否是上下游用户
 * 通过比较消息中的 ToUserName（CorpID）与配置的 CorpID
 */
export function detectUpstreamUser(params: {
  messageToUserName: string;
  primaryCorpId: string;
}): boolean {
  const { messageToUserName, primaryCorpId } = params;
  if (!messageToUserName?.trim() || !primaryCorpId?.trim()) {
    return false;
  }
  const normalizedMessageCorpId = messageToUserName.trim().toLowerCase();
  const normalizedPrimaryCorpId = primaryCorpId.trim().toLowerCase();

  // 如果消息中的 CorpID 与主 CorpID 不同，则是上下游用户
  return normalizedMessageCorpId !== normalizedPrimaryCorpId;
}

/**
 * 为上下游用户创建临时的 Agent 配置
 * 使用下游企业的 CorpID 和 AgentID，但保持主企业的 corpSecret
 * 
 * 注意：这个配置用于发送消息，但获取 access_token 时需要使用专门的
 * corpgroup/corp/gettoken 接口
 */
export function createUpstreamAgentConfig(params: {
  baseAgent: ResolvedAgentAccount;
  upstreamCorpId: string;
  upstreamAgentId: number;
}): ResolvedAgentAccount {
  const { baseAgent, upstreamCorpId, upstreamAgentId } = params;
  
  return {
    ...baseAgent,
    corpId: upstreamCorpId,
    agentId: upstreamAgentId,
    // corpSecret 保持主企业的，用于获取下游企业的 access_token
    // token 和 encodingAESKey 保持主企业的，用于回调验证
  };
}

/**
 * 从配置中解析上下游企业映射
 * 支持在 agent 配置中添加 upstreamCorps 字段
 */
export function resolveUpstreamCorpConfig(params: {
  upstreamCorpId: string;
  upstreamCorps?: Record<string, UpstreamCorpConfig> | UpstreamCorpConfig[];
}): UpstreamCorpConfig | undefined {
  const { upstreamCorpId, upstreamCorps } = params;

  if (!upstreamCorps) {
    return undefined;
  }

  // Normalize to array format (support both Record<string, ...> and array)
  const entries: Array<[string, UpstreamCorpConfig]> = Array.isArray(upstreamCorps)
    ? upstreamCorps.map((item, i) => [String(i), item])
    : Object.entries(upstreamCorps);

  // Find matching upstream config
  const normalizedTargetCorpId = upstreamCorpId.trim().toLowerCase();

  for (const [key, config] of entries) {
    const normalizedConfigCorpId = config.corpId.trim().toLowerCase();

    if (normalizedConfigCorpId === normalizedTargetCorpId) {
      return config;
    }
  }

  return undefined;
}

/**
 * 构建上下游用户的回复目标
 * 格式: wecom-agent-upstream:{accountId}:{corpId}:{userId}
 */
export function buildUpstreamAgentSessionTarget(
  userId: string,
  accountId: string,
  upstreamCorpId: string,
): string {
  return `wecom-agent-upstream:${accountId}:${upstreamCorpId}:${userId}`;
}

/**
 * 解析上下游用户的回复目标
 */
export function parseUpstreamAgentSessionTarget(
  target: string,
): { accountId: string; upstreamCorpId: string; userId: string } | undefined {
  const prefix = "wecom-agent-upstream:";
  if (target.startsWith(prefix)) {
    const parts = target.slice(prefix.length).split(":");
    if (parts.length !== 3) {
      return undefined;
    }

    return {
      accountId: parts[0]!,
      upstreamCorpId: parts[1]!,
      userId: parts[2]!,
    };
  }

  // 兼容当前工作区里尚未持久化的新格式，避免旧会话目标失效。
  const queryIndex = target.indexOf("?upstream_corp=");
  if (queryIndex < 0 || !target.startsWith("wecom-agent:")) {
    return undefined;
  }
  const pathPart = target.slice(0, queryIndex);
  const upstreamCorpId = target.slice(queryIndex + "?upstream_corp=".length).trim();
  const match = pathPart.match(/^wecom-agent:([^:]+):user:(.+)$/i);
  if (!match || !upstreamCorpId) {
    return undefined;
  }

  return {
    accountId: match[1]!.trim(),
    upstreamCorpId,
    userId: match[2]!.trim(),
  };
}
