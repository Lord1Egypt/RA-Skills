# Mattermost node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Mattermost node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.mattermost`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Mattermost node in n8n. Follow technical documentation to integrate Mattermost node into your workflows.

## 关键操作 / 参数线索

- Channel
- Add a user to a channel
- Create a new channel
- Soft delete a channel
- Get a page of members for a channel
- Restores a soft deleted channel
- Search for a channel
- Get statistics for a channel
- Message
- Soft delete a post, by marking the post as deleted in the database
- Post a message into a channel
- Post an ephemeral message into a channel
- Reaction
- Add a reaction to a post.
- Remove a reaction from a post
- Get all the reactions to one or more posts
- User
- Create a new user

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

