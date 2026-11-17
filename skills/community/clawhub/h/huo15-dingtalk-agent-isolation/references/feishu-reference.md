# 飞书 Dynamic Agent 实现参考

本文档记录 OpenClaw 飞书连接器的 `dynamic-agent.ts` 实现细节，作为钉钉 Agent 级隔离的参考蓝图。

## 源码位置

```
~/.openclaw/dev/openclaw/extensions/feishu/src/dynamic-agent.ts
~/.openclaw/dev/openclaw/extensions/feishu/src/types.ts
```

## 核心类型

```typescript
// types.ts
export type DynamicAgentCreationConfig = {
  enabled?: boolean;
  workspaceTemplate?: string;
  agentDirTemplate?: string;
  maxAgents?: number;
};
```

## 工作流程

```
用户发消息 → 检查是否匹配到 default 路由
    ↓ 是 default
检查 dynamicAgentCreation.enabled
    ↓ 已启用
检查是否已有该用户的 Agent
    ↓ 不存在
检查 maxAgents 上限
    ↓ 未达上限
获取 config mutation lock (mutateConfigFile)
    ↓ 获取锁
双重检查（并发安全）
    ↓ 通过
生成 Agent ID
    ↓
创建 workspace 和 agentDir 目录
    ↓
添加 agent 到 agents.list
    ↓
添加 binding 到 bindings 数组
    ↓
写回 openclaw.json
    ↓
返回 { created: true, agentId }
```

## Agent ID 生成规则

```typescript
// 默认账号: feishu-{senderOpenId}
// 命名账号: feishu-{accountId前12位}-{sha256(accountId+senderOpenId)前32位}
```

## 钉钉的适配差异

| 方面 | 飞书 | 钉钉 |
|------|------|------|
| Channel ID | `feishu` | `dingtalk-connector` |
| 用户 ID | `senderOpenId` | `senderStaffId` |
| 会话类型 | `p2p` | `direct` (值为 `"1"`) |
| Agent ID 前缀 | `feishu-` | `dingtalk-` |
| 配置写入 | `runtime.config.mutateConfigFile` | 直接读写 `openclaw.json`（简化版） |
| 已有 binding 检查 | `resolveAgentRoute` (SDK) | 手动遍历 `cfg.bindings` |

## 钉钉连接器已有的 binding 匹配

钉钉连接器 `message-handler.ts` 已内置 binding 匹配逻辑（v0.8.24+），无需额外修改：

```typescript
// src/core/message-handler.ts (约 L1143-1158)
if (cfg.bindings && cfg.bindings.length > 0) {
  for (const binding of cfg.bindings) {
    const match = binding.match;
    if (match.channel && match.channel !== "dingtalk-connector") continue;
    if (match.accountId && match.accountId !== accountId) continue;
    if (match.peer) {
      if (match.peer.kind && match.peer.kind !== sessionContext.chatType) continue;
      if (match.peer.id && match.peer.id !== '*' && match.peer.id !== sessionContext.peerId) continue;
    }
    matchedAgentId = binding.agentId;
    break;
  }
}
```

这意味着 **Mode A（手动绑定）开箱即用**，只需要在 `openclaw.json` 中配置正确的 `agents` 和 `bindings`。
