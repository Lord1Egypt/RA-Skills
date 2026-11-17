# Dynamic Agent Patch — TypeScript 参考

本文档包含完整的 TypeScript patch 代码，用于为钉钉连接器添加 `dynamicAgentCreation` 支持。

## 文件 1: `src/dynamic-agent.ts`（新文件）

```typescript
/**
 * DingTalk Dynamic Agent Creation
 *
 * 移植自 OpenClaw Feishu 的 dynamic-agent.ts
 * 当用户首次私聊机器人时，自动创建独立的 Agent + binding
 */
import { createHash } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

type DynamicAgentCreationConfig = {
  enabled?: boolean;
  workspaceTemplate?: string;
  agentDirTemplate?: string;
  maxAgents?: number;
};

interface OpenClawConfig {
  agents?: {
    default?: string;
    list?: Array<{ id: string; workspace?: string; agentDir?: string; [k: string]: any }>;
  };
  bindings?: Array<{
    agentId: string;
    match: {
      channel?: string;
      accountId?: string;
      peer?: { kind?: string; id?: string };
    };
  }>;
  channels?: Record<string, any>;
  [k: string]: any;
}

function resolveUserPath(p: string): string {
  if (p.startsWith("~/")) {
    return path.join(os.homedir(), p.slice(2));
  }
  return p;
}

function resolveDynamicAgentId(accountId: string, senderId: string): string {
  if (accountId === "default") {
    return `dingtalk-${senderId}`;
  }
  const identityDigest = createHash("sha256")
    .update(accountId)
    .update("\0")
    .update(senderId)
    .digest("hex")
    .slice(0, 32);
  return `dingtalk-${accountId.slice(0, 12)}-${identityDigest}`;
}

function resolveDynamicAgentConfig(
  cfg: OpenClawConfig,
  accountId: string,
): DynamicAgentCreationConfig | undefined {
  const channelCfg = cfg.channels?.["dingtalk-connector"];
  if (!channelCfg) return undefined;
  if (accountId !== "default" && channelCfg.accounts?.[accountId]) {
    return channelCfg.accounts[accountId].dynamicAgentCreation;
  }
  return channelCfg.dynamicAgentCreation;
}

function hasDefaultDirectRoute(
  cfg: OpenClawConfig,
  accountId: string,
  senderId: string,
): boolean {
  const bindings = cfg.bindings ?? [];
  for (const binding of bindings) {
    const match = binding.match;
    if (match.channel && match.channel !== "dingtalk-connector") continue;
    if (match.accountId && match.accountId !== accountId) continue;
    if (match.peer) {
      if (match.peer.kind && match.peer.kind !== "direct") continue;
      if (match.peer.id && match.peer.id !== "*" && match.peer.id !== senderId) continue;
    }
    return false;
  }
  return true;
}

function isAtDynamicAgentLimit(
  cfg: OpenClawConfig,
  dynamicCfg: DynamicAgentCreationConfig,
): boolean {
  if (dynamicCfg.maxAgents === undefined) return false;
  const count = (cfg.agents?.list ?? []).filter((a) => a.id.startsWith("dingtalk-")).length;
  return count >= dynamicCfg.maxAgents;
}

export async function maybeCreateDynamicAgent(params: {
  cfg: OpenClawConfig;
  configFilePath: string;
  accountId: string;
  senderId: string;
  isDirect: boolean;
  log?: (...args: any[]) => void;
}): Promise<{ created: boolean; agentId?: string; updatedCfg?: OpenClawConfig }> {
  const { cfg, configFilePath, senderId, isDirect, log } = params;
  const accountId = params.accountId || "default";

  if (!isDirect) return { created: false };
  if (!hasDefaultDirectRoute(cfg, accountId, senderId)) return { created: false };

  const dynamicCfg = resolveDynamicAgentConfig(cfg, accountId);
  if (!dynamicCfg?.enabled) return { created: false };

  const agentId = resolveDynamicAgentId(accountId, senderId);
  const exists = (cfg.agents?.list ?? []).some((a) => a.id === agentId);

  if (!exists && isAtDynamicAgentLimit(cfg, dynamicCfg)) {
    log?.(`dingtalk: maxAgents limit (${dynamicCfg.maxAgents}) reached`);
    return { created: false };
  }

  // 读取并解析配置文件
  let rawConfig: string;
  try {
    rawConfig = await fs.promises.readFile(configFilePath, "utf-8");
  } catch (e: any) {
    log?.(`dingtalk: 无法读取配置文件: ${e.message}`);
    return { created: false };
  }

  // 清理 JSON5 语法（注释和尾逗号）
  const cleaned = rawConfig
    .replace(/\/\/.*$/gm, "")
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/,\s*([}\]])/g, "$1");

  let draft: OpenClawConfig;
  try {
    draft = JSON.parse(cleaned);
  } catch (e: any) {
    log?.(`dingtalk: 配置文件 JSON 解析失败: ${e.message}`);
    return { created: false };
  }

  // 双重检查
  if (!hasDefaultDirectRoute(draft, accountId, senderId)) return { created: false };
  const draftDynamicCfg = resolveDynamicAgentConfig(draft, accountId);
  if (!draftDynamicCfg?.enabled) return { created: false };
  const draftExists = (draft.agents?.list ?? []).some((a) => a.id === agentId);
  if (!draftExists && isAtDynamicAgentLimit(draft, draftDynamicCfg)) return { created: false };

  // 创建目录
  if (!draftExists) {
    const wsTemplate = draftDynamicCfg.workspaceTemplate ?? "~/.openclaw/workspace-dingtalk-{agentId}";
    const adTemplate = draftDynamicCfg.agentDirTemplate ?? "~/.openclaw/agents/{agentId}/agent";
    const workspace = resolveUserPath(wsTemplate.replace("{userId}", senderId).replace("{agentId}", agentId));
    const agentDir = resolveUserPath(adTemplate.replace("{userId}", senderId).replace("{agentId}", agentId));
    log?.(`dingtalk: creating dynamic agent "${agentId}" for user ${senderId}`);
    await fs.promises.mkdir(workspace, { recursive: true });
    await fs.promises.mkdir(agentDir, { recursive: true });
    if (!draft.agents) draft.agents = { default: "main", list: [] };
    if (!draft.agents.list) draft.agents.list = [];
    draft.agents.list.push({ id: agentId, workspace, agentDir });
  }

  // 添加 binding
  if (!draft.bindings) draft.bindings = [];
  draft.bindings.push({
    agentId,
    match: { channel: "dingtalk-connector", accountId, peer: { kind: "direct", id: senderId } },
  });

  // 写回
  await fs.promises.writeFile(configFilePath, JSON.stringify(draft, null, 2) + "\n", "utf-8");
  log?.(`dingtalk: config updated, agent "${agentId}" created`);
  return { created: true, agentId, updatedCfg: draft };
}
```

## 文件 2: `src/config/schema.ts`（修改）

在 `DingtalkSharedConfigShape` 对象的 `groupReplyMode` 后添加：

```typescript
  // Dynamic Agent Creation (Agent 级隔离)
  dynamicAgentCreation: z
    .object({
      enabled: z.boolean().optional(),
      workspaceTemplate: z.string().optional(),
      agentDirTemplate: z.string().optional(),
      maxAgents: z.number().int().positive().optional(),
    })
    .strict()
    .optional(),
```

## 文件 3: `src/core/message-handler.ts`（修改）

在 `matchedAgentId` 确定后（约 L1156 `if (!matchedAgentId) {` 之前）插入：

```typescript
  // ===== Dynamic Agent Creation (Agent 级隔离) =====
  if (matchedAgentId === (cfg.defaultAgent || 'main') && isDirect) {
    try {
      const { maybeCreateDynamicAgent } = await import('../dynamic-agent.ts');
      const configFilePath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
      const dynamicResult = await maybeCreateDynamicAgent({
        cfg, configFilePath, accountId, senderId, isDirect, log,
      });
      if (dynamicResult.created && dynamicResult.agentId) {
        log?.info?.(`[DynamicAgent] 创建新 Agent: ${dynamicResult.agentId}`);
        matchedAgentId = dynamicResult.agentId;
        if (dynamicResult.updatedCfg) {
          Object.assign(cfg, dynamicResult.updatedCfg);
        }
      }
    } catch (dynErr: any) {
      log?.warn?.(`[DynamicAgent] 动态创建失败: ${dynErr?.message || dynErr}`);
    }
  }
```

## 与飞书实现的差异

1. **配置写入方式**: 飞书使用 SDK 的 `runtime.config.mutateConfigFile`（带锁），钉钉简化为直接读写文件
2. **binding 检查**: 飞书使用 SDK 的 `resolveAgentRoute`，钉钉手动遍历 `cfg.bindings`
3. **Channel ID**: `feishu` → `dingtalk-connector`
4. **会话类型**: `p2p` → `direct`（值为 `"1"`）
5. **用户 ID**: `senderOpenId` → `senderStaffId`
6. **Agent ID 前缀**: `feishu-` → `dingtalk-`
