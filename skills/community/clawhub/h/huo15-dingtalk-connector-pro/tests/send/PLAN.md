# send 模块测试方案

## 1. 目的与覆盖范围

`tests/send` 覆盖消息发送服务，负责通过钉钉 Webhook 发送不同类型的消息（Markdown、文本、链接）。

主要覆盖（以测试文件实际引用为准）：

- Markdown 消息：**sendMarkdownMessage**
- 文本消息：**sendTextMessage**
- 链接消息：**sendLinkMessage**

## 2. 用例表（覆盖现有测试）

### 2.1 sendMarkdownMessage

| 序号 | 输入 | 期望 |
|------|------|------|
| 1 | webhook + title + markdown | 发送 msgtype=markdown，包含 title 和 text |
| 2 | 带 atUserId | 消息体包含 at 字段（userIds、isAtAll） |

### 2.2 sendTextMessage

| 序号 | 输入 | 期望 |
|------|------|------|
| 3 | webhook + 文本内容 | 发送 msgtype=text，包含 content |
| 4 | 带 atUserId | 文本内容包含 "@u2" |

### 2.3 sendLinkMessage

| 序号 | 输入 | 期望 |
|------|------|------|
| 5 | webhook + 链接对象（title、text、picUrl、messageUrl） | 发送 msgtype=link，包含完整的 link 对象 |

## 3. 预期正确输出与潜在错误

- **正确**：消息类型（msgtype）正确设置；消息体结构符合钉钉 API 规范；@ 功能正确应用到消息中。
- **潜在错误原因**：消息体字段缺失或格式错误；@ 功能未正确应用到文本内容；不同消息类型的字段混淆。
