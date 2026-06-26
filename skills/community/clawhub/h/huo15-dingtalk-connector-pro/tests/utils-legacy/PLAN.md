# utils-legacy 模块测试方案

## 1. 目的与覆盖范围

`tests/utils-legacy` 覆盖历史遗留的工具函数集合，包括鉴权、消息去重、配置读取、媒体处理、情绪回复和会话上下文构建等功能。

主要覆盖（以测试文件实际引用为准）：

- 鉴权：**getAccessToken / getOapiAccessToken / getUnionId**
- 消息去重：**isMessageProcessed / markMessageProcessed / cleanupProcessedMessages**
- 配置读取：**getDingtalkConfig / isDingtalkConfigured**
- 媒体：**buildMediaSystemPrompt**
- 情绪回复：**addEmotionReply / recallEmotionReply**
- 会话上下文：**buildSessionContext**

## 2. 用例表（覆盖现有测试）

### 2.1 getAccessToken

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | 两次调用相同配置 | 返回相同 token，只发起一次请求（缓存） |

### 2.2 getOapiAccessToken

| 序号 | 场景 | 期望 |
|------|------|------|
| 2 | 正常请求 | 返回 access_token |
| 3 | 网络失败 | 返回 null |

### 2.3 getUnionId

| 序号 | 场景 | 期望 |
|------|------|------|
| 4 | 两次调用相同员工 | 返回相同 unionId（缓存） |
| 5 | 首次调用 | 返回 unionId |

### 2.4 消息去重 helpers

| 序号 | 输入 | 期望 |
|------|------|------|
| 6 | isMessageProcessed("") | false |
| 7 | isMessageProcessed("m1") | false |
| 8 | markMessageProcessed("m1") 后 isMessageProcessed("m1") | true |
| 9 | cleanupProcessedMessages 后 isMessageProcessed("m1") | true（cleanup 不清除已标记） |

### 2.5 getDingtalkConfig / isDingtalkConfigured

| 序号 | 输入 | 期望 |
|------|------|------|
| 10 | getDingtalkConfig({}) | `{}` |
| 11 | isDingtalkConfigured({}) | false |
| 12 | isDingtalkConfigured + 有 clientId 和 clientSecret | true |

### 2.6 buildMediaSystemPrompt

| 序号 | 输入 | 期望 |
|------|------|------|
| 13 | 无参数 | 返回包含 "DINGTALK_VIDEO"、"DINGTALK_AUDIO"、"DINGTALK_FILE" 的 markdown |

### 2.7 addEmotionReply / recallEmotionReply

| 序号 | 场景 | 期望 |
|------|------|------|
| 14 | 无 msgId | 跳过，不发起请求 |
| 15 | 有 msgId + 成功 | 发起请求 |
| 16 | 有 msgId + 失败 | 记录 warn 日志 |

### 2.8 buildSessionContext

| 序号 | 输入 | 期望 |
|------|------|------|
| 17 | conversationType="1"（直聊） | chatType 为 "direct" |
| 18 | conversationType="2" + groupSessionScope="group_sender" | peerId 为 "c1:u1" |
| 19 | conversationType="2" + separateSessionByConversation=false | peerId 为 "u1" |

## 3. 预期正确输出与潜在错误

- **正确**：Token 缓存机制正常工作；消息去重正确标记和查询；配置读取和校验逻辑正确；媒体系统提示包含所有必要的标记；情绪回复正确处理成功和失败场景；会话上下文根据不同场景正确构建 peerId。
- **潜在错误原因**：缓存机制失效导致重复请求；消息去重状态未正确持久化；配置校验逻辑遗漏；会话上下文构建逻辑错误导致 peerId 不正确。
