# Chat Memory Manager node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Chat Memory Manager node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.memorymanager`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the Chat Memory Manager node in n8n. Follow technical documentation to integrate Chat Memory Manager node into your workflows.

## 关键操作 / 参数线索

- **Operation Mode**: Choose between **Get Many Messages**, **Insert Messages**, and **Delete Messages** operations.
- **Insert Mode**: Available in **Insert Messages** mode. Choose from:
- **Insert Messages**: Insert messages alongside existing messages.
- **Override All Messages**: Replace current memory.
- **Delete Mode**: available in **Delete Messages** mode. Choose from:
- **Last N**: Delete the last N messages.
- **All Messages**: Delete messages from memory.
- **Chat Messages**: available in **Insert Messages** mode. Define the chat messages to insert into the memory, including:
- **Type Name or ID**: Set the message type. Select one of:
- **AI**: Use this for messages from the AI.
- **System**: Add a message containing instructions for the AI.
- **User**: Use this for messages from the user. This message type is sometimes called the 'human' message in other AI tools and guides.
- **Message**: Enter the message contents.
- **Hide Message in Chat**: Select whether n8n should display the message to the user in the chat UI (turned off) or not (turned on).
- **Messages Count**: Available in **Delete Messages** mode when you select **Last N**. Enter the number of latest messages to delete.
- **Simplify Output**: Available in **Get Many Messages** mode. Turn on to simplify the output to include only the sender (AI, user, or system) and the text.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

