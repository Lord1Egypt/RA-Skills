# Webhook node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Webhook node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.webhook`
- node group: `core-nodes`

## 核心要点

- Learn how to use the Webhook node in n8n. Follow technical documentation to integrate Webhook node into your workflows.

## 关键操作 / 参数线索

- **Test**: n8n registers a test webhook when you select **Listen for Test Event** or **Execute workflow**, if the workflow isn't active. When you call the webhook URL, n8n displays the data in the workflow.
- **Production**: n8n registers a production webhook when you publish the workflow. When using the production URL, n8n doesn't display the data in the workflow. You can still view workflow data for a production execution: select the **Executions** tab in the workflow, then select the workflow execution you want to view.
- DELETE
- GET
- HEAD
- PATCH
- POST
- PUT
- `/:variable`
- `/path/:variable`
- `/:variable/path`
- `/:variable1/path/:variable2`
- `/:variable1/:variable2`
- Basic auth
- Header auth
- JWT auth
- None
- **Immediately**: The Webhook node returns the response code and the message **Workflow got started**.

## 常用选项线索

- **Allowed Origins (CORS)**: Set the permitted cross-origin domains. Enter a comma-separated list of URLs allowed for cross-origin non-preflight requests. Use `*` (default) to allow all origins.
- **Binary Property**: Enabling this setting allows the Webhook node to receive binary data, such as an image or audio file. Enter the name of the binary property to write the data of the received file to.
- **Ignore Bots**: Ignore requests from bots like link previewers and web crawlers.
- **IP(s) Whitelist**: Enable this to limit who (or what) can invoke a Webhook trigger URL. Enter a comma-separated list of allowed IP addresses. Access from IP addresses outside the whitelist throws a 403 error. If left blank, all IP addresses can invoke the webhook trigger URL.
- **No Response Body**: Enable this to prevent n8n sending a body with the response.
- **Raw Body**: Specify that the Webhook node will receive data in a raw format, such as JSON or XML.
- **Response Content-Type**: Choose the format for the webhook body.
- **Response Data**: Send custom data with the response.
- **Response Headers**: Send extra headers in the Webhook response. Refer to MDN Web Docs | Response header to learn more about response headers.
- **Property Name**: by default, n8n returns all available data. You can choose to return a specific JSON key, so that n8n returns the value.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

