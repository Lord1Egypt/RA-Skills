# Slack node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Slack node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.slack`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Slack node in n8n. Follow technical documentation to integrate Slack node into your workflows.

## 关键操作 / 参数线索

- **Channel**
- **Archive** a channel.
- **Close** a direct message or multi-person direct message.
- **Create** a public or private channel-based conversation.
- **Get** information about a channel.
- **Get Many**: Get a list of channels in Slack.
- **History**: Get a channel's history of messages and events.
- **Invite** a user to a channel.
- **Join** an existing channel.
- **Kick**: Remove a user from a channel.
- **Leave** a channel.
- **Member**: List the members of a channel.
- **Open** or resume a direct message or multi-person direct message.
- **Rename** a channel.
- **Replies**: Get a thread of messages posted to a channel.
- **Sets purpose** of a channel.
- **Sets topic** of a channel.
- **Unarchive** a channel.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

