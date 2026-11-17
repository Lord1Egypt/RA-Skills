# Chat Trigger node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Chat Trigger node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.chattrigger`
- node group: `core-nodes`

## 核心要点

- Learn how to use the Chat Trigger node in n8n. Follow technical documentation to integrate Chat Trigger node into your workflows.

## 关键操作 / 参数线索

- **Hosted Chat**: Use n8n's hosted chat interface. Recommended for most users because you can configure the interface using the node options and don't have to do any other setup.
- **Embedded Chat**: This option requires you to create your own chat interface. You can use n8n's chat widget or build your own. Your chat interface must call the webhook URL shown in **Chat URL** in the node.
- **None**: The chat doesn't use authentication. Anyone can use the chat.
- **Basic Auth**: The chat uses basic authentication.
- Select or create a **Credential for Basic Auth** with a username and password. All users must use the same username and password.
- **n8n User Auth**: Only users logged in to an n8n account can use the chat.

## 常用选项线索

- **When Last Node Finishes**: The Chat Trigger node returns the response code and the data output from the last node executed in the workflow.
- **Using Response Nodes**: The Chat Trigger node responds as defined in a Chat node or Respond to Webhook node. In this response mode, the Chat Trigger will solely show messages as defined in these nodes and not output the data from the last node executed in the workflow.
- **Streaming response**: Enables real-time data streaming back to the user as the workflow processes. Requires nodes with streaming support in the workflow (for example, the AI agent node).
- **Streaming response**: Enables real-time data streaming back to the user as the workflow processes. Requires nodes with streaming support enabled.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

