# Bindings 解析模块（resolveAgentIdByBindings）测试方案

## 1. 模块划分与职责

- **resolveAgentIdByBindings(accountId, peerKind, peerId, log?): string**
  - 职责：根据 OpenClaw 配置的 bindings 与当前会话（accountId、peerKind、peerId）解析出应使用的 agentId。配置从 `~/.openclaw/openclaw.json` 读取；匹配优先级见下。

## 2. 匹配优先级（从高到低）

| 优先级 | 条件 | 说明 |
|--------|------|------|
| 1 | peer.kind + peer.id 精确匹配（id 非 '*'） | 单聊/群聊 + 具体 peerId |
| 2 | peer.kind + peer.id='*' | 通配该会话类型下所有 peer |
| 3 | 仅 peer.kind 匹配（无 peer.id） | 按单聊/群聊 |
| 4 | 无 peer，match.accountId === accountId | 按账号 |
| 5 | 无 peer 且无 accountId | 仅 channel |
| 6 | 无匹配 | 返回 defaultAgentId |

**defaultAgentId**：当 accountId === `'__default__'` 时为 `'main'`，否则为 accountId。

## 3. 用例矩阵（全覆盖）

### 3.1 无配置文件或配置不可读

| 序号 | fs.existsSync | fs.readFileSync / 异常 | 期望 | 说明 |
|------|----------------|------------------------|------|------|
| 1 | false | - | defaultAgentId | 文件不存在 |
| 2 | true | throw Error | defaultAgentId，log.warn | 读文件抛错 |
| 3 | true | 非 JSON 字符串 | defaultAgentId，log.warn | JSON.parse 抛错 |

### 3.2 无 bindings 或 bindings 为空

| 序号 | readFileSync 返回 | 期望 | 说明 |
|------|-------------------|------|------|
| 4 | `'{}'` | defaultAgentId | 无 bindings 键 |
| 5 | `'{"bindings":[]}'` | defaultAgentId | 空数组 |

### 3.3 channel 筛选

| 序号 | bindings 内容 | 期望 | 说明 |
|------|----------------|------|------|
| 6 | `[{ agentId: 'a', match: { channel: 'other' } }]` | defaultAgentId | 非 dingtalk-connector 被筛掉 |
| 7 | `[{ agentId: 'a', match: { channel: 'dingtalk-connector' } }]` | 能匹配到 'a'（见优先级5） | channel 匹配 |
| 8 | `[{ agentId: 'a', match: {} }]` | 能匹配到 'a' | 无 channel 视为匹配 |

### 3.4 defaultAgentId 逻辑

| 序号 | accountId | 无配置/无匹配时期望 | 说明 |
|------|-----------|---------------------|------|
| 9 | `'__default__'` | `'main'` | 单账号模式 |
| 10 | `'acc1'` | `'acc1'` | 多账号 |

### 3.5 优先级1：精确 peer.id

| 序号 | bindings | accountId | peerKind | peerId | 期望 | 说明 |
|------|----------|-----------|----------|--------|------|------|
| 11 | `[{ agentId: 'agent1', match: { peer: { kind: 'direct', id: 'user1' } } }]` | any | 'direct' | 'user1' | 'agent1' | 精确匹配 |
| 12 | 同上 | any | 'direct' | 'user2' | defaultAgentId | id 不同 |
| 13 | 同上 | any | 'group' | 'user1' | defaultAgentId | kind 不同 |
| 14 | `[{ agentId: 'a', match: { accountId: 'acc1', peer: { kind: 'direct', id: 'u1' } } }]` | 'acc1' | 'direct' | 'u1' | 'a' | accountId 一致 |
| 15 | 同上 | 'acc2' | 'direct' | 'u1' | defaultAgentId | accountId 不一致被 continue |

### 3.6 优先级2：peer.id='*'

| 序号 | bindings | peerKind | peerId | 期望 | 说明 |
|------|----------|----------|--------|------|------|
| 16 | `[{ agentId: 'wild', match: { peer: { kind: 'direct', id: '*' } } }]` | 'direct' | 'any_id' | 'wild' | 通配单聊 |
| 17 | 同上 | 'group' | 'any' | defaultAgentId | kind 不同 |

### 3.7 优先级3：仅 peer.kind

| 序号 | bindings | peerKind | 期望 | 说明 |
|------|----------|----------|------|------|
| 18 | `[{ agentId: 'kindOnly', match: { peer: { kind: 'group' } } }]` | 'group' | 'kindOnly' | 无 peer.id |
| 19 | 同上 | 'direct' | defaultAgentId | kind 不同 |

### 3.8 优先级4：accountId

| 序号 | bindings | accountId | 期望 | 说明 |
|------|----------|-----------|------|------|
| 20 | `[{ agentId: 'accAgent', match: { accountId: 'acc1' } }]` | 'acc1' | 'accAgent' | 无 peer |
| 21 | 同上 | 'acc2' | defaultAgentId | accountId 不同 |

### 3.9 优先级5：仅 channel

| 序号 | bindings | 期望 | 说明 |
|------|----------|------|------|
| 22 | `[{ agentId: 'channelOnly', match: { channel: 'dingtalk-connector' } }]` | 'channelOnly' | 无 peer 无 accountId 时取第一个 |

### 3.10 binding.agentId 为空

| 序号 | bindings | 期望 | 说明 |
|------|----------|------|------|
| 23 | `[{ agentId: '', match: { peer: { kind: 'direct', id: 'u1' } } }]` | defaultAgentId | 代码 return binding.agentId \|\| defaultAgentId |

## 4. 预期正确输出与潜在错误

- **正确输出**：返回字符串 agentId，无 undefined；优先级顺序正确时先匹配到的先返回。
- **潜在错误原因**：配置文件路径写死或与文档不一致；channel 筛选条件反了；accountId 比较时 continue 漏写；优先级顺序颠倒；defaultAgentId 未区分 __default__。
