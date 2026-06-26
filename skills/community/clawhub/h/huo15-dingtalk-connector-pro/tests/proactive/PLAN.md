# Proactive（主动消息）模块测试方案

## 1. 模块划分与职责

本套件覆盖“主动消息 API”相关函数，包括消息体构造、发送到用户/群、以及 AI Card 的默认策略与回退：

- **buildMsgPayload(msgType, content, title?)**：构建 `{ msgKey, msgParam }`；markdown 若未显式传 title，则从 `# ` 头部提取；link/actionCard 支持从 JSON 字符串解析；未知类型回退到 text。
- **sendNormalToUser(config, userId \| userIds, content, opts)**：使用主动消息接口发送普通消息给单/多用户。
- **sendNormalToGroup(config, openConversationId, content, opts)**：发送普通消息到群。
- **sendToUser(config, userIds, content, opts)**：高层入口，默认单用户走 AI Card，多用户走普通消息；支持 `useAICard=false`；AI Card 失败可 `fallbackToNormal`（默认 true）。
- **sendToGroup(config, openConversationId, content, opts)**：高层入口，默认走 AI Card；失败回退普通消息（默认）。
- **sendProactive(config, target, content, opts)**：MCP/上层调用的统一入口；自动识别 markdown；目标支持 userId/userIds/openConversationId；目标缺失返回错误。

## 2. 用例表（覆盖现有测试）

### 2.1 buildMsgPayload

| 序号 | msgType | content | title | 期望 | 说明 |
|------|---------|---------|-------|------|------|
| 1 | text | 'Hello' | - | msgKey=sampleText | content 直传 |
| 2 | markdown | '# Title\nBody' | 'Title' | msgKey=sampleMarkdown + title/text |  |
| 3 | markdown | '# My Title\nBody' | (空) | title='My Title' | 自动提取 |
| 4 | link | JSON 字符串 | - | msgKey=sampleLink | 解析成功 |
| 5 | link | 非法 JSON | - | 返回 error | 解析失败 |
| 6 | actionCard | JSON 字符串 | - | msgKey=sampleActionCard |  |
| 7 | actionCard | 非法 JSON | - | 返回 error |  |
| 8 | image | url | - | msgKey=sampleImageMsg |  |
| 9 | unknown | 'content' | - | 回退 sampleText | 容错 |

### 2.2 sendNormalToUser

| 序号 | 场景 | 输入 | mock 返回 | 期望 |
|------|------|------|----------|------|
| 10 | 单用户 text | userId='user123' | processQueryKey=key123 | ok=true + usedAICard=false |
| 11 | 多用户 | ['user1','user2'] | processQueryKey=key123 | ok=true |
| 12 | link/actionCard 格式错误 | msgType='link' 且 content 非 JSON | - | ok=false + error |
| 13 | API 错误（有 response.data.message） | axios.post reject | - | ok=false + error |
| 14 | 响应缺 processQueryKey | data={} | - | ok=false |

**契约补充（请求体）**：

- `msgParam` 必须是 **JSON 字符串**（可 `JSON.parse`），且 text 场景至少包含 `{ content: string }`。
- 单用户发送应调用 `POST /v1.0/robot/oToMessages/batchSend`，并携带 `robotCode/userIds/msgKey/msgParam` 等关键字段。

### 2.3 sendNormalToGroup

| 序号 | 场景 | 输入 | mock 返回 | 期望 |
|------|------|------|----------|------|
| 15 | 群消息成功 | conv123 | processQueryKey=key123 | ok=true |
| 16 | 群 markdown | msgType=markdown | processQueryKey=key123 | ok=true |
| 17 | API 错误 | axios.post reject | - | ok=false |

**契约补充（请求体）**：

- 群发送应调用 `POST /v1.0/robot/groupMessages/send`，并携带 `openConversationId/robotCode/msgKey/msgParam`。
- `msgParam` 必须是 **JSON 字符串**（可 `JSON.parse`）：
  - text：至少包含 `{ content: string }`
  - markdown：至少包含 `{ title: string, text: string }`，其中 title 可从 `# 标题` 自动提取（具体规则见实现与用例）

### 2.4 sendToUser / sendToGroup（AI Card 策略与回退）

| 序号 | 场景 | 输入 | mock | 期望 | 说明 |
|------|------|------|------|------|------|
| 18 | 缺 clientId/secret | config={} | - | ok=false | 参数校验 |
| 19 | userIds 为空数组 | [] | - | ok=false | 参数校验 |
| 20 | 单用户默认 AI Card | 'user123' | card 成功 | ok=true | 默认策略 |
| 21 | 多用户默认普通消息 | ['u1','u2'] | normal 成功 | ok=true + usedAICard=false |  |
| 22 | AI Card 失败回退普通消息 | 单用户 | card 失败 + normal 成功 | ok=true | fallbackToNormal=true |
| 23 | 禁止回退 | fallbackToNormal=false | card 失败 | ok=false |  |
| 24 | useAICard=false | 单用户 | normal 成功 | ok=true + usedAICard=false |  |
| 25 | 群默认 AI Card | conv123 | card 成功 | ok=true |  |
| 26 | 群卡片失败回退 | conv123 | card 失败 + normal 成功 | ok=true |  |

### 2.5 sendProactive

| 序号 | 场景 | target | content | 期望 |
|------|------|--------|---------|------|
| 27 | 自动识别 markdown | userId | '# Title\nContent' | ok=true |
| 28 | userId | {userId} | 'Hello' | ok=true |
| 29 | userIds | {userIds:[...]} | 'Hello' | ok=true |
| 30 | openConversationId | {openConversationId} | 'Hello' | ok=true |
| 31 | 无 target | {} | 'Hello' | ok=false + error 包含 Must specify |

## 3. 预期正确输出与潜在错误

- **正确**：消息体构造对 link/actionCard 的 JSON 解析有错误返回；`sendToUser/sendToGroup` 的 AI Card 策略与回退行为符合测试；所有错误路径都返回结构化 `{ ok:false, error }`。
- **潜在错误原因**：markdown title 提取规则错误；processQueryKey 判空遗漏；回退逻辑在 `fallbackToNormal=false` 时仍执行；把单用户/多用户策略写反；target 选择优先级不一致导致发送到错误对象。

