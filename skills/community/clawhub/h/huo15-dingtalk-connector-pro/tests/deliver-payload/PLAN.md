# 投放体与消息体构建模块测试方案

## 1. 模块划分与职责

- **buildDeliverBody(cardInstanceId: string, target: AICardTarget, robotCode: string): any**
  - 职责：构建钉钉 AI Card 投放请求体。target 为 `{ type: 'user', userId }` 或 `{ type: 'group', openConversationId }`，分别生成单聊/群聊的 openSpaceId 与 deliver 模型。
- **buildMsgPayload(msgType: DingTalkMsgType, content: string, title?: string): { msgKey, msgParam } | { error }**
  - 职责：根据消息类型构建普通消息 API 的 msgKey 与 msgParam；link/actionCard 需 content 为合法 JSON，否则返回 { error }。

## 2. buildDeliverBody 用例矩阵

| 序号 | cardInstanceId | target | robotCode | 期望 openSpaceId 含 | 期望 body 含 | 说明 |
|------|----------------|--------|-----------|----------------------|--------------|------|
| 1 | `'card_1'` | `{ type: 'user', userId: 'u1' }` | `'robot_1'` | `dtv1.card//IM_ROBOT.u1` | imRobotOpenDeliverModel, robotCode: 'robot_1' | 单聊 |
| 2 | `'card_2'` | `{ type: 'group', openConversationId: 'cid_1' }` | `'robot_2'` | `dtv1.card//IM_GROUP.cid_1` | imGroupOpenDeliverModel, robotCode: 'robot_2' | 群聊 |
| 3 | `'x'` | `{ type: 'user', userId: 'abc' }` | `'r'` | outTrackId: 'x', userIdType: 1 | - | 基础字段 |

## 3. buildMsgPayload 用例矩阵

### 3.1 msgType === 'text' / default

| 序号 | msgType | content | title | 期望 msgKey | 期望 msgParam | 说明 |
|------|---------|---------|-------|-------------|---------------|------|
| 4 | `'text'` | `'hello'` | - | `'sampleText'` | `{ content: 'hello' }` | 文本 |
| 5 | `undefined` 或任意未匹配 | `'x'` | - | `'sampleText'` | `{ content: 'x' }` | default |

### 3.2 msgType === 'markdown'

| 序号 | msgType | content | title | 期望 msgKey | 期望 msgParam 含 | 说明 |
|------|---------|---------|-------|-------------|------------------|------|
| 6 | `'markdown'` | `'# Hi\nbody'` | - | `'sampleMarkdown'` | title（首行去 # 等后截 20 字）, text: '# Hi\nbody' | 默认 title 从 content 取 |
| 7 | `'markdown'` | `'body'` | `'My Title'` | `'sampleMarkdown'` | title: 'My Title', text: 'body' | 显式 title |
| 8 | `'markdown'` | `''` | - | `'sampleMarkdown'` | title: 'Message'（fallback）, text: '' | 空 content |

### 3.3 msgType === 'link'

| 序号 | content | 期望 | 说明 |
|------|---------|------|------|
| 9 | `'{"title":"t","messageUrl":"u","picUrl":"p"}'` | msgKey: 'sampleLink', msgParam 为解析后对象 | 合法 JSON |
| 10 | `'not json'` | error: 'Invalid link message format, expected JSON' | 非法 JSON |
| 11 | `''` | error | 空字符串 JSON.parse 抛错 |

### 3.4 msgType === 'actionCard'

| 序号 | content | 期望 | 说明 |
|------|---------|------|------|
| 12 | `'{"title":"t","text":"b"}'` | msgKey: 'sampleActionCard', msgParam 为解析后对象 | 合法 JSON |
| 13 | `'invalid'` | error: 'Invalid actionCard message format, expected JSON' | 非法 JSON |

### 3.5 msgType === 'image'

| 序号 | content | 期望 | 说明 |
|------|---------|------|------|
| 14 | `'http://photo.url'` | msgKey: 'sampleImageMsg', msgParam: { photoURL: 'http://photo.url' } | 图片 URL |

## 4. 预期正确输出与潜在错误

- **正确输出**：buildDeliverBody 返回对象含 outTrackId、userIdType、openSpaceId 及对应 deliver 模型；buildMsgPayload 返回 { msgKey, msgParam } 或 { error }，无 undefined 必填字段。
- **潜在错误原因**：openSpaceId 拼写错误（IM_ROBOT/IM_GROUP）；target.type 漏分支；markdown 的 title 从 content 提取时正则或 slice 错误；link/actionCard 未 try-catch 导致抛错未转为 error。
