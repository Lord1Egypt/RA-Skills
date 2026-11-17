# Respond to Webhook

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Respond to Webhook` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.respondtowebhook`
- node group: `core-nodes`

## 核心要点

- Documentation for the Respond to Webhook node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **All Incoming Items**: Respond with all the JSON items from the input.
- **Binary File**: Respond with a binary file defined in **Response Data Source**.
- **First Incoming Item**: Respond with the first incoming item's JSON.
- **JSON**: Respond with a JSON object defined in **Response Body**.
- **JWT Token**: Respond with a JSON Web Token (JWT).
- **No Data**: No response payload.
- **Redirect**: Redirect to a URL set in **Redirect URL**.
- **Text**: Respond with text set in **Response Body**. This sends HTML by default (`Content-Type: text/html`).

## 常用选项线索

- **Response Code**: Set the response code to use.
- **Response Headers**: Define the response headers to send.
- **Put Response in Field**: Available when you respond with **All Incoming Items** or **First Incoming Item**. Set the field name for the field containing the response data.
- **Enable Streaming**: When enabled, sends the data back to the user using streaming. Requires a trigger configured with the **Response mode** **Streaming**.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

