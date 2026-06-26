# Session 模块测试方案

## 1. 模块划分与职责

- **normalizeSlashCommand(text: string): string**  
  将新会话触发指令统一归一到 `/new`，其余原样返回。
- **buildSessionContext(params): SessionContext**  
  根据 accountId、senderId、conversationType、conversationId、groupSubject、separateSessionByConversation、groupSessionScope 构造 OpenClaw 标准会话上下文。
- **isMessageProcessed(messageId: string): boolean**  
  判断消息是否已处理（去重）。
- **markMessageProcessed(messageId: string): void**  
  标记消息已处理；空 messageId 不写入；size>=100 时触发清理。
- **cleanupProcessedMessages(): void**  
  删除超过 MESSAGE_DEDUP_TTL 的条目。

## 2. 已覆盖用例（与 `session.test.ts` 对齐）

> 说明：本章节仅列出**已在测试中覆盖**的用例，确保文档与现状 100% 一致；后续新增用例建议继续用 `it.each` 扩展。

### 2.1 normalizeSlashCommand

| 序号 | 输入 text | 期望输出 | 说明 |
|------|-----------|----------|------|
| 1 | `''` | `''` | 空字符串 |
| 2 | `'   '` | `'   '` | 仅空格非命令，返回原文（实现返回 text 非 trimmed） |
| 3 | `'/new'` | `'/new'` | 标准命令 |
| 4 | `' /new '` | `'/new'` | 首尾空格 |
| 5 | `'/NEW'` | `'/new'` | 大写 |
| 6 | `'/New'` | `'/new'` | 混合大小写 |
| 7 | `'/reset'` | `'/new'` | 重置 |
| 8 | `'/clear'` | `'/new'` | 清空 |
| 9 | `'新会话'` | `'/new'` | 中文 |
| 10 | `'重新开始'` | `'/new'` | 中文 |
| 11 | `'清空对话'` | `'/new'` | 中文 |
| 12 | `'  新会话  '` | `'/new'` | 中文+空格 |
| 13 | `'hello'` | `'hello'` | 非命令 |
| 14 | `' /not-a-command '` | `' /not-a-command '` | 非命令保留空格 |
| 15 | `'/new session'` | `'/new session'` | 多词不匹配全等 |
| 16 | `'new'` | `'new'` | 无斜杠不匹配 |
| 17 | `'新会话xxx'` | `'新会话xxx'` | 带后缀不匹配 |

### 2.2 buildSessionContext

> 说明：当前测试覆盖了 `conversationType=1/2`、`groupSessionScope=group_sender`、以及 `conversationId` 缺失/空字符串回退等关键路径。

| 序号 | separateSessionByConversation | conversationType | conversationId | groupSessionScope | 期望 chatType | 期望 peerId | 说明 |
|------|-------------------------------|------------------|----------------|-------------------|---------------|-------------|------|
| 18 | false | '1' | - | - | direct | senderId | 按用户维度单聊 |
| 19 | false | '2' | cid1 | - | group | senderId | 按用户维度群聊 |
| 20 | true | '1' | - | - | direct | senderId | 单聊 |
| 21 | true | '2' | cid1 | 未设置 | group | cid1 | 群共享 |
| 22 | true | '2' | cid1 | 'group' | group | cid1 | 群共享显式 |
| 23 | true | '2' | cid1 | 'group_sender' | group | cid1:senderId | 群内按人 |
| 24 | true | '2' | undefined | - | group | senderId | conversationId 缺失时 peerId 回退 senderId |
| 25 | true | '2' | '' | - | group | senderId | 空字符串 conversationId 回退 |

**可选字段**：senderName、groupSubject 有则带出，无则 undefined；单聊无 conversationId/groupSubject；separateSessionByConversation 为 true 时群聊带 conversationId、groupSubject。

### 2.3 消息去重

| 序号 | 操作 | 期望 | 说明 |
|------|------|------|------|
| 27 | isMessageProcessed('') | false | 空字符串视为未处理 |
| 28 | isMessageProcessed('msg-1') 首次 | false | 未标记过 |
| 29 | markMessageProcessed('msg-1'); isMessageProcessed('msg-1') | true | 标记后为已处理 |
| 30 | markMessageProcessed('') | 无写入 | 空 messageId 不写入 Map |
| 31 | markMessageProcessed(''); isMessageProcessed('') | false | 空未标记，仍为未处理 |
| 32 | cleanupProcessedMessages() 调用 | 不抛错 | 空 Map 或未过期条目不变 |

## 3. 待补充用例（文档列出但当前未覆盖）

> 说明：以下用例用于后续补齐覆盖，**不代表当前已测**。

### 3.1 buildSessionContext

| 序号 | separateSessionByConversation | conversationType | conversationId | groupSessionScope | 期望 chatType | 期望 peerId | 说明 |
|------|-------------------------------|------------------|----------------|-------------------|---------------|-------------|------|
| P1 | - | '3'（或其它异常值） | - | - | group（按实现） | - | 若实现允许“非 1 均视为群聊”，建议补充覆盖 |

### 3.2 消息去重清理策略

| 序号 | 场景 | 操作 | 期望 | 说明 |
|------|------|------|------|------|
| P2 | size>=100 触发清理 | 连续 mark 100+ 条 | Map 被清理/容量回落 | 以实现为准 |
| P3 | TTL 到期清理 | 构造过期条目 + cleanup | 过期条目被删除 | 需要可控时间或注入 now |

## 5. 预期正确输出与潜在错误

- **正确**：normalizeSlashCommand 仅对 NEW_SESSION_COMMANDS 全等（trim+lowerCase）归一为 `/new`；buildSessionContext 各分支 peerId/chatType 符合上表；空 messageId 不写入、isMessageProcessed('') 为 false。
- **错误原因**：trim/toLowerCase 漏写；conversationType 用数字 1/2；groupSessionScope 分支漏写；conversationId 为 undefined 时未回退 peerId；空 messageId 被写入导致误判；TTL 单位或比较反了。
