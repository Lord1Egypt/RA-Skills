# Send Email

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Send Email` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.sendemail`
- node group: `core-nodes`

## 核心要点

- Documentation for the Send Email node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Send**: Send an email.
- **Send and Wait for Response**: Send an email and wait for a response from the receiver. This operation pauses the workflow execution until the user submits a response.
- **Text**: Send the email in plain-text format.
- **HTML**: Send the email in HTML format.
- **Both**: Send the email in both formats. If you choose this option, the email recipient's client will set which format to display.

## 常用选项线索

- Use the Read/Write Files from Disk node or the HTTP Request node to upload the file to your workflow.
- Add multiple attachments by entering a comma-separated list of binary properties.
- Reference embedded images or other content within the body of an email message, for example ``.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

