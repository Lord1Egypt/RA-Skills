# MCP Tools 测试方案

## 1. 模块划分与职责

本套件验证对外暴露给 MCP 的“工具级接口”在输入校验、路由与错误返回方面的行为一致性（并不追求真实网络调用）：

- **sendToUser(config, userId, content, opts)**：向单用户发送（text/markdown），缺参数时返回结构化错误。
- **sendToGroup(config, openConversationId, content, opts)**：向群发送，缺参数时返回错误。
- **sendProactive(config, target, content, opts)**：统一主动消息入口，支持 userId/userIds/openConversationId。
- **sendFileProactive / sendVideoProactive / sendAudioProactive**：文件/视频/音频的主动发送封装。
- **uploadMediaToDingTalk**：上传媒体并返回 `media_id` 或 null。
- **extractMessageContent**：消息内容提取的基础能力（复用单元逻辑）。

## 2. 用例表（覆盖现有测试）

### 2.1 sendToUser（MCP）

| 序号 | 场景 | 输入 | 期望 |
|------|------|------|------|
| 1 | text | user123 + 'Hello' + useAICard=false | ok=true |
| 2 | markdown | user123 + '# Title...' + useAICard=false | ok=true |
| 3 | userId 缺失 | userId='' | ok=false + error 包含 empty |
| 4 | clientId 缺失 | config={} | ok=false + error 包含 Missing |

### 2.2 sendToGroup（MCP）

| 序号 | 场景 | 输入 | 期望 |
|------|------|------|------|
| 5 | 成功 | conv123 | ok=true |
| 6 | openConversationId 缺失 | '' | ok=false |

### 2.3 sendProactive（MCP）

| 序号 | 场景 | target | 期望 |
|------|------|--------|------|
| 7 | userId | {userId:'user123'} | ok=true |
| 8 | userIds | {userIds:['u1','u2']} | ok=true |
| 9 | openConversationId | {openConversationId:'conv123'} | ok=true |
| 10 | 缺 target | {} | ok=false + error 包含 Must specify |

### 2.4 send*Proactive（文件/视频/音频）

| 序号 | 场景 | 期望 |
|------|------|------|
| 11 | sendFileProactive user/group | log.info 被调用 |
| 12 | sendVideoProactive user/group | log.info 被调用 |
| 13 | sendAudioProactive user/group（含 duration） | log.info 被调用 |

### 2.5 uploadMediaToDingTalk（MCP）

| 序号 | 场景 | mock | 期望 |
|------|------|------|------|
| 14 | 成功 | errcode=0 + media_id | 返回 media_id |
| 15 | 失败 | errcode!=0 | 返回 null |

### 2.6 extractMessageContent / buildDeliverBody

| 序号 | 场景 | 期望 |
|------|------|------|
| 16 | text/markdown 提取 | result.text 正确 |
| 17 | （已移除）deliver body | buildDeliverBody 属于 AI Card 投放体构建，契约由 `tests/ai-card` 覆盖 |

## 3. 预期正确输出与潜在错误

- **正确**：对外工具在“缺参”场景返回稳定的结构化错误；同一类能力（发送/上传/解析）与单元实现一致；不依赖真实网络环境即可跑通。
- **潜在错误原因**：MCP 层未做输入校验导致下游抛错；将 `useAICard` 默认策略带入导致测试不稳定；错误信息不一致影响调用方处理。

