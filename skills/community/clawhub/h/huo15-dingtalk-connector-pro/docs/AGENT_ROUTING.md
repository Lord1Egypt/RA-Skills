# Agent 路由与 SessionKey 规范

本文档是 DingTalk OpenClaw Connector 中 **Agent 路由（bindings）** 和 **SessionKey 构建** 的完整开发规范，供新功能开发和代码审查参考。

涉及文件：
- `src/utils/session.ts` — `buildSessionContext()` 函数，构建会话上下文
- `src/core/message-handler.ts` — bindings 路由匹配、sessionKey 构建、消息队列管理

---

## 一、SessionContext 字段总览

`buildSessionContext()` 返回的 `SessionContext` 包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `channel` | `'dingtalk-connector'` | 固定值，标识频道来源 |
| `accountId` | `string` | 当前钉钉账号 ID |
| `chatType` | `'direct' \| 'group'` | 会话类型，单聊或群聊 |
| `peerId` | `string` | **路由匹配专用**，真实 peer 标识（群聊为 `conversationId`，单聊为 `senderId`），**不受任何会话隔离配置影响** |
| `sessionPeerId` | `string` | **session/memory 隔离键**，用于构建 `sessionKey` 和消息队列 key，**受会话隔离配置影响，可能与 `peerId` 不同** |
| `conversationId` | `string?` | 群聊会话 ID，单聊时为 `undefined` |
| `senderName` | `string?` | 发送者昵称 |
| `groupSubject` | `string?` | 群名称，单聊时为 `undefined` |

其中 `channel`、`accountId`、`chatType`、`conversationId`、`senderName`、`groupSubject` 都是直接从消息原始字段透传的，没有歧义。

**需要特别注意的是 `peerId` 和 `sessionPeerId` 这两个字段**，它们都是 peer 标识，但职责完全不同，**不能混用**：

- **路由匹配（去哪个 Agent）** → 使用 `peerId`
- **session 隔离（共享多大范围的上下文）** → 使用 `sessionPeerId`

---

## 二、buildSessionContext() 完整逻辑

`buildSessionContext()` 在 `src/utils/session.ts` 中定义，每条消息到达时调用一次，根据消息原始字段和账号配置，决定 `peerId` 和 `sessionPeerId` 的值。

### 2.1 输入参数

| 参数 | 来源 | 说明 |
|------|------|------|
| `accountId` | 账号配置 key | 当前钉钉账号标识 |
| `senderId` | 消息原始字段 `data.senderStaffId` | 发送者 userId |
| `senderName` | 消息原始字段 `data.senderNick` | 发送者昵称 |
| `conversationType` | 消息原始字段 `data.conversationType` | `"1"` = 单聊，其他 = 群聊 |
| `conversationId` | 消息原始字段 `data.conversationId` | 群聊的会话 ID |
| `groupSubject` | 消息原始字段 `data.conversationTitle` | 群名称 |
| `separateSessionByConversation` | `config.separateSessionByConversation` | 是否按会话区分 session |
| `groupSessionScope` | `config.groupSessionScope` | 群聊 session 粒度 |
| `sharedMemoryAcrossConversations` | `config.sharedMemoryAcrossConversations` | 是否跨会话共享记忆 |

### 2.2 peerId 的计算规则（固定，不受配置影响）

```
peerId = isDirect ? senderId : (conversationId || senderId)
```

- 单聊：`peerId = senderId`
- 群聊：`peerId = conversationId`（无 conversationId 时降级为 senderId）

### 2.3 sessionPeerId 的决策树

配置优先级从高到低，**命中第一条即返回**：

```
sharedMemoryAcrossConversations === true
  → sessionPeerId = accountId
  （所有单聊+群聊共享同一记忆，以 accountId 为 session 键）

separateSessionByConversation === false
  → sessionPeerId = senderId
  （按用户维度隔离，不区分群/单聊，同一用户在不同群共享 session）

isDirect（单聊）
  → sessionPeerId = senderId
  （每个用户独立 session）

groupSessionScope === 'group_sender'（群聊）
  → sessionPeerId = `${conversationId}:${senderId}`
  （群内每个用户独立 session）

默认（群聊）
  → sessionPeerId = conversationId || senderId
  （整个群共享一个 session）
```

### 2.4 各配置组合下的完整取值表

| 配置 | 场景 | `peerId` | `sessionPeerId` |
|------|------|----------|-----------------|
| `sharedMemoryAcrossConversations: true` | 单聊 | `senderId` | `accountId` |
| `sharedMemoryAcrossConversations: true` | 群聊 | `conversationId` | `accountId` |
| `separateSessionByConversation: false` | 单聊 | `senderId` | `senderId` |
| `separateSessionByConversation: false` | 群聊 | `conversationId` | `senderId` |
| `groupSessionScope: "group_sender"` | 群聊 | `conversationId` | `${conversationId}:${senderId}` |
| 默认 | 单聊 | `senderId` | `senderId` |
| 默认 | 群聊 | `conversationId` | `conversationId` |

> **注意**：`sharedMemoryAcrossConversations: true` 优先级最高，会覆盖其他所有配置。

---

## 三、Agent 路由规则（Bindings）

### 3.1 路由流程

每条钉钉消息到达后，connector 按以下顺序确定目标 Agent：

```
消息到达
  ↓
buildSessionContext()        ← 构建会话上下文（含 peerId / sessionPeerId）
  ↓
遍历 cfg.bindings[]          ← 按顺序逐条匹配，使用 peerId 进行匹配
  ↓ 命中第一条
matchedAgentId               ← 使用该 agentId
  ↓ 全部未命中
cfg.defaultAgent || 'main'   ← 回退到默认 Agent
```

### 3.2 Binding 匹配字段

每条 binding 的 `match` 字段支持以下维度，**所有指定的维度必须同时满足**（AND 关系）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `match.channel` | `string?` | 频道名，固定为 `"dingtalk-connector"`，省略则匹配所有频道 |
| `match.accountId` | `string?` | 钉钉账号 ID（对应 `accounts` 配置中的 key），省略则匹配所有账号 |
| `match.peer.kind` | `"direct" \| "group"?` | 会话类型，省略则匹配单聊和群聊 |
| `match.peer.id` | `string?` | Peer 标识，群聊为 `conversationId`，单聊为 `senderId`，`"*"` 表示通配所有 |

### 3.3 匹配逻辑（源码）

```typescript
// src/core/message-handler.ts
for (const binding of cfg.bindings) {
  const match = binding.match;
  if (match.channel && match.channel !== 'dingtalk-connector') continue;
  if (match.accountId && match.accountId !== accountId) continue;
  if (match.peer) {
    if (match.peer.kind && match.peer.kind !== sessionContext.chatType) continue;
    // 使用 peerId（真实 peer 标识），不受会话隔离配置影响
    if (match.peer.id && match.peer.id !== '*' && match.peer.id !== sessionContext.peerId) continue;
  }
  matchedAgentId = binding.agentId;
  break;
}
if (!matchedAgentId) {
  matchedAgentId = cfg.defaultAgent || 'main';
}
```

### 3.4 优先级规则

- **顺序优先**：bindings 数组按顺序遍历，**第一条命中的规则生效**，后续规则不再检查
- **精确规则放前面**：将指定了 `peer.id` 的精确规则放在通配规则（`peer.id: "*"`）之前，避免通配规则提前拦截

### 3.5 典型配置示例

**多群分配不同 Agent**：

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "dingtalk-connector",
        "accountId": "groupbot",
        "peer": { "kind": "group", "id": "cid3RKewszsVbXZYCYmbybVNw==" }
      }
    },
    {
      "agentId": "organizer",
      "match": {
        "channel": "dingtalk-connector",
        "accountId": "groupbot",
        "peer": { "kind": "group", "id": "cidqO7Ne7e+myoRu67AguW+HQ==" }
      }
    },
    {
      "agentId": "atlas",
      "match": {
        "channel": "dingtalk-connector",
        "accountId": "groupbot",
        "peer": { "kind": "group", "id": "cidekzhmRmaKaJ6vnQezRFZWA==" }
      }
    }
  ]
}
```

**单聊走一个 Agent，群聊走另一个**：

```json
{
  "bindings": [
    {
      "agentId": "personal-assistant",
      "match": { "channel": "dingtalk-connector", "peer": { "kind": "direct" } }
    },
    {
      "agentId": "group-bot",
      "match": { "channel": "dingtalk-connector", "peer": { "kind": "group" } }
    }
  ]
}
```

**精确路由 + 通配兜底**：

```json
{
  "bindings": [
    {
      "agentId": "vip-agent",
      "match": { "channel": "dingtalk-connector", "peer": { "kind": "group", "id": "cidVIP..." } }
    },
    {
      "agentId": "main",
      "match": { "channel": "dingtalk-connector", "peer": { "kind": "group", "id": "*" } }
    }
  ]
}
```

---

## 四、SessionKey 构建规范

### 4.1 SessionKey 格式

SessionKey 由 SDK 的 `core.channel.routing.buildAgentSessionKey()` 生成，格式为：

```
agent:{agentId}:{channel}:{peerKind}:{sessionPeerId}
```

示例：
- `agent:main:dingtalk-connector:direct:manager7195` — 默认单聊，按用户隔离
- `agent:main:dingtalk-connector:group:cid3RKewszsVbXZYCYmbybVNw==` — 默认群聊，按群隔离
- `agent:main:dingtalk-connector:direct:bot1` — `sharedMemoryAcrossConversations=true`，所有会话共享（sessionPeerId = accountId = "bot1"）
- `agent:main:dingtalk-connector:group:bot1` — 同上，群聊也共享

### 4.2 SessionKey 构建代码规范

```typescript
// src/core/message-handler.ts
const dmScope = cfg.session?.dmScope || 'per-channel-peer';
const sessionKey = core.channel.routing.buildAgentSessionKey({
  agentId: matchedAgentId,
  channel: 'dingtalk-connector',       // ✅ 固定值，不能写 'dingtalk'
  accountId: accountId,
  peer: {
    kind: sessionContext.chatType,       // 'direct' | 'group'
    id: sessionContext.sessionPeerId,    // ✅ 使用 sessionPeerId，不是 peerId
  },
  dmScope: dmScope,                      // ✅ 必须传递，影响 sessionKey 格式
});
```

**禁止**：
- 用 `sessionContext.peerId` 构建 sessionKey（`peerId` 是路由匹配专用）
- 手动拼接 sessionKey 字符串（必须通过 SDK 的 `buildAgentSessionKey` 方法）
- `channel` 写成 `'dingtalk'`（必须是 `'dingtalk-connector'`）

### 4.3 消息队列 Key 规范

消息队列（`sessionQueues`）用于确保同一会话+Agent 的消息串行处理，避免并发冲突。队列 key 格式：

```
{sessionPeerId}:{agentId}
```

**必须与 sessionKey 使用相同的 `sessionPeerId`**，确保隔离策略一致：

```typescript
// src/core/message-handler.ts
const baseSessionId = sessionContext.sessionPeerId;
const queueKey = `${baseSessionId}:${matchedAgentId}`;
```

这样不同 Agent 可以并发处理，同一 Agent 的同一会话串行处理。

### 4.4 InboundContext 中的 From / To 字段

构建 `ctxPayload` 时，`From` 和 `To` 字段规则如下：

| 字段 | 单聊 | 群聊 |
|------|------|------|
| `From` | `senderId` | `senderId` |
| `To` | `senderId` | `conversationId` |
| `OriginatingTo` | `senderId` | `conversationId` |

```typescript
const toField = isDirect ? senderId : data.conversationId;
// From 始终是 senderId，To 单聊用 senderId，群聊用 conversationId
```

---

## 五、配置参数速查

### 5.1 会话隔离相关配置

| 配置字段 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `sharedMemoryAcrossConversations` | `boolean` | `false` | 所有会话（单聊+群聊）共享同一记忆，优先级最高 |
| `separateSessionByConversation` | `boolean` | `true` | 是否按会话（群/单聊）区分 session；`false` 时按用户维度 |
| `groupSessionScope` | `"group" \| "group_sender"` | `"group"` | 群聊 session 粒度；`group_sender` 时群内每人独立 |
| `session.dmScope` | `string` | `"per-channel-peer"` | 传递给 SDK 的 dmScope 参数，影响 sessionKey 格式 |

### 5.2 路由相关配置

| 配置字段 | 类型 | 说明 |
|---------|------|------|
| `bindings` | `Binding[]` | Agent 路由规则列表，按顺序匹配 |
| `defaultAgent` | `string` | 未命中任何 binding 时的默认 Agent，默认为 `"main"` |

---

## 六、开发规范总结

1. **路由匹配用 `peerId`**：`match.peer.id` 与 `sessionContext.peerId` 比较，`peerId` 始终是真实的 `conversationId`（群）或 `senderId`（单聊），不受任何会话隔离配置影响。

2. **session 构建用 `sessionPeerId`**：`sessionKey` 和 `queueKey` 的构建均使用 `sessionContext.sessionPeerId`，受会话隔离配置影响，决定记忆/上下文的共享范围。

3. **两者职责严格分离**：路由（去哪个 Agent）和记忆隔离（共享多大范围的上下文）是两个独立维度，代码中不能用同一个字段同时承担两种职责。

4. **sessionKey 必须通过 SDK 构建**：使用 `core.channel.routing.buildAgentSessionKey()`，不要手动拼接字符串，`channel` 固定为 `'dingtalk-connector'`，`dmScope` 必须传递。

5. **bindings 顺序即优先级**：精确规则（指定 `peer.id`）必须放在通配规则（`peer.id: "*"`）之前。

6. **`sharedMemoryAcrossConversations` 优先级最高**：该配置开启后，`sessionPeerId` 被强制设为 `accountId`，覆盖其他所有会话隔离配置，但 `peerId` 不受影响，路由仍然正常工作。
