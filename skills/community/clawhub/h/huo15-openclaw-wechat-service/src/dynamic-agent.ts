/**
 * **动态 Agent 路由模块（微信服务号 / 公众号）**
 *
 * 为每个 openid 自动派生一个独立 agent，实现"一粉一会话"的隔离。
 * 与 `@huo15/wecom` 的 dynamic-agent 同构（schema 完全对齐），便于运维同学统一心智模型。
 *
 * 公众号场景说明：
 *  - 公众号是 1:N 推送 + 1:1 客服消息，没有"群聊"概念。
 *  - `groupEnabled` 字段保留是为了 schema 与 wecom 对齐，公众号场景请保持默认 false。
 *  - `dmCreateAgent`：每个 openid 一个 agent —— 公众号默认场景。
 *  - `adminUsers`：管理员 openid 名单，绕过动态路由，始终走 main agent。
 *
 * Agent ID 命名：`wechat-service-{accountId}-{type}-{sanitizedOpenid}`
 *   例：`wechat-service-default-dm-oabc123` （openid 走 sanitize：小写 + 非 [a-z0-9_-] 替换为 _）
 *
 * 参考：`@huo15/wecom` `src/dynamic-agent.ts`
 */

import type { OpenClawConfig } from "openclaw/plugin-sdk";
import { CONFIG_SECTION_KEY, LEGACY_CONFIG_SECTION_KEY } from "./config/index.js";

export interface DynamicAgentConfig {
  enabled: boolean;
  dmCreateAgent: boolean;
  /** 公众号无群聊场景，保留字段是为了 schema 与 @huo15/wecom 对齐，默认 false */
  groupEnabled: boolean;
  adminUsers: string[];
  /**
   * 默认 persona preset（v2.3.0+）：未配置时用 "it-support"（IT 学习客服）。
   * 设 "none" / "off" 关闭 persona 注入。
   */
  defaultInstructionsPreset: string;
}

/**
 * **getDynamicAgentConfig (读取动态 Agent 配置)**
 *
 * 从全局配置 `channels["wechat-service"].dynamicAgents` 读取，提供默认值。
 * v1.0.1+ key 是 kebab-case（与 channel id 对齐），v0.1 ~ v1.0.0 的 `wechatService` 旧 key 也兜底读一次。
 */
export function getDynamicAgentConfig(config: OpenClawConfig): DynamicAgentConfig {
  const channels = (config as { channels?: Record<string, unknown> })?.channels;
  const section =
    (channels?.[CONFIG_SECTION_KEY] as { dynamicAgents?: Partial<DynamicAgentConfig> } | undefined) ??
    (channels?.[LEGACY_CONFIG_SECTION_KEY] as { dynamicAgents?: Partial<DynamicAgentConfig> } | undefined);
  const dynamicAgents = section?.dynamicAgents;
  return {
    // v2.3.0 起：默认开启动态 agent —— 每位粉丝一个独立会话/记忆，开箱即可用
    enabled: dynamicAgents?.enabled ?? true,
    // 公众号场景：每个 openid 一个 agent 是默认推荐
    dmCreateAgent: dynamicAgents?.dmCreateAgent ?? true,
    // 公众号无群聊：默认 false（与 wecom 同名字段语义保持一致即可）
    groupEnabled: dynamicAgents?.groupEnabled ?? false,
    adminUsers: dynamicAgents?.adminUsers ?? [],
    // v2.3.0 起：默认走 IT 学习客服 persona
    defaultInstructionsPreset:
      typeof dynamicAgents?.defaultInstructionsPreset === "string"
        ? dynamicAgents.defaultInstructionsPreset
        : "it-support",
  };
}

function sanitizeDynamicIdPart(value: string): string {
  return String(value)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_-]/g, "_");
}

/**
 * **generateAgentId (生成动态 Agent ID)**
 *
 * 根据账号 + 聊天类型 + 对端 ID 生成确定性的 Agent ID，避免多账号串会话。
 * 格式: `wechat-service-{accountId}-{type}-{sanitizedPeerId}`
 */
export function generateAgentId(
  chatType: "dm" | "group",
  peerId: string,
  accountId?: string,
): string {
  const sanitizedPeer = sanitizeDynamicIdPart(peerId) || "unknown";
  const sanitizedAccountId = sanitizeDynamicIdPart(accountId ?? "default") || "default";
  return `wechat-service-${sanitizedAccountId}-${chatType}-${sanitizedPeer}`;
}

/**
 * **buildAgentSessionTarget (构造动态 Agent 的会话目标字符串)**
 *
 * 与 wecom 的 `wecom-agent:<accountId>:user:<userid>` 同构，给上层 outbound 解析用。
 */
export function buildAgentSessionTarget(openid: string, accountId?: string): string {
  const normalizedOpenid = String(openid).trim();
  const sanitizedAccountId = sanitizeDynamicIdPart(accountId ?? "default") || "default";
  return `wechat-service:${sanitizedAccountId}:user:${normalizedOpenid}`;
}

/**
 * **shouldUseDynamicAgent (检查是否使用动态 Agent)**
 *
 * 判断流程：
 *  1. `enabled === false` → 不使用，走静态路由
 *  2. senderId 在 `adminUsers` 里 → 不使用（绕过动态路由）
 *  3. group 场景 → 看 `groupEnabled`（公众号正常情况下永远不会进这条分支）
 *  4. dm 场景 → 看 `dmCreateAgent`
 */
export function shouldUseDynamicAgent(params: {
  chatType: "dm" | "group";
  senderId: string;
  config: OpenClawConfig;
}): boolean {
  const { chatType, senderId, config } = params;
  const dynamicConfig = getDynamicAgentConfig(config);

  if (!dynamicConfig.enabled) {
    return false;
  }

  // 管理员绕过动态路由
  const sender = String(senderId).trim().toLowerCase();
  const isAdmin = dynamicConfig.adminUsers.some(
    (admin) => admin.trim().toLowerCase() === sender,
  );
  if (isAdmin) {
    return false;
  }

  if (chatType === "group") {
    return dynamicConfig.groupEnabled;
  }
  return dynamicConfig.dmCreateAgent;
}

/**
 * 内存中已确保的 Agent ID（避免重复写入）
 */
const ensuredDynamicAgentIds = new Set<string>();

/**
 * 写入队列（避免并发冲突）
 */
let ensureDynamicAgentWriteQueue: Promise<void> = Promise.resolve();

/**
 * 将 Agent ID 插入 agents.list（如果不存在），可选写入 instructions。
 */
function upsertAgentEntry(
  cfg: Record<string, unknown>,
  agentId: string,
  instructions?: string,
): boolean {
  if (!cfg.agents || typeof cfg.agents !== "object") {
    cfg.agents = {};
  }

  const agentsObj = cfg.agents as Record<string, unknown>;
  const currentList: Array<{ id: string; instructions?: string }> = Array.isArray(agentsObj.list)
    ? (agentsObj.list as Array<{ id: string; instructions?: string }>)
    : [];
  const existingIds = new Set(
    currentList
      .map((entry) => entry?.id?.trim().toLowerCase())
      .filter((id): id is string => Boolean(id)),
  );

  let changed = false;
  const nextList = [...currentList];

  // 首次创建时保留 main 作为默认
  if (nextList.length === 0) {
    nextList.push({ id: "main" });
    existingIds.add("main");
    changed = true;
  }

  if (!existingIds.has(agentId.toLowerCase())) {
    const entry: { id: string; instructions?: string } = { id: agentId };
    if (instructions) entry.instructions = instructions;
    nextList.push(entry);
    changed = true;
  } else if (instructions) {
    // agent 已存在 → 更新 instructions（如果变化了）
    const idx = nextList.findIndex(
      (e) => e.id?.trim().toLowerCase() === agentId.toLowerCase(),
    );
    if (idx >= 0 && nextList[idx]!.instructions !== instructions) {
      nextList[idx] = { ...nextList[idx]!, instructions };
      changed = true;
    }
  }

  if (changed) {
    agentsObj.list = nextList;
  }

  return changed;
}

/**
 * **ensureDynamicAgentListed (确保动态 Agent 已添加到 agents.list)**
 *
 * 将动态生成的 Agent ID 添加到 OpenClaw 配置中的 agents.list。
 * 在 role-based 权限模式下，同时写入角色感知的 agent instructions。
 *
 * 特性：
 * - 幂等：使用内存 Set 避免重复写入
 * - 串行：使用 Promise 队列避免并发冲突
 * - 异步：调用方应 fire-and-forget，不阻塞消息处理流程
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function ensureDynamicAgentListed(
  agentId: string,
  runtime: any,
  instructions?: string,
): Promise<void> {
  const normalizedId = String(agentId).trim().toLowerCase();
  if (!normalizedId) return;
  if (ensuredDynamicAgentIds.has(normalizedId)) return;

  const configRuntime = runtime?.config;
  if (!configRuntime?.loadConfig || !configRuntime?.writeConfigFile) return;

  ensureDynamicAgentWriteQueue = ensureDynamicAgentWriteQueue
    .then(async () => {
      if (ensuredDynamicAgentIds.has(normalizedId)) return;

      const latestConfig = configRuntime.loadConfig!();
      if (!latestConfig || typeof latestConfig !== "object") return;

      const changed = upsertAgentEntry(
        latestConfig as Record<string, unknown>,
        normalizedId,
        instructions,
      );
      if (changed) {
        await configRuntime.writeConfigFile!(latestConfig as unknown);
      }

      ensuredDynamicAgentIds.add(normalizedId);
    })
    .catch((err) => {
      console.warn(`[wechat-service] 动态 Agent 添加失败: ${normalizedId}`, err);
    });

  await ensureDynamicAgentWriteQueue;
}

/**
 * **resetEnsuredCache (重置已确保缓存)**
 *
 * 主要用于测试场景，重置内存中的缓存状态。
 */
export function resetEnsuredCache(): void {
  ensuredDynamicAgentIds.clear();
}
