# Telegram node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Telegram node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.telegram`
- node group: `app-nodes`

## 核心要点

- Documentation for the Telegram node in n8n, a workflow automation platform. Includes details of operations and configuration, and links to examples and credentials information.

## 关键操作 / 参数线索

- **Chat** operations
- **Get** up-to-date information about a chat.
- **Get Administrators**: Get a list of all administrators in a chat.
- **Get Member**: Get the details of a chat member.
- **Leave** a chat.
- **Set Description** of a chat.
- **Set Title** of a chat.
- **Callback** operations
- **Answer Query**: Send answers to callback queries sent from inline keyboards.
- **Answer Inline Query**: Send answers to callback queries sent from inline queries.
- **File** operations
- **Get File** from Telegram.
- **Message** operations
- **Delete Chat Message**.
- **Edit Message Text**: Edit the text of an existing message.
- **Pin Chat Message** for the chat.
- **Send Animation** to the chat.
- For use with GIFs or H.264/MPEG-4 AVC videos without sound up to 50 MB in size.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

