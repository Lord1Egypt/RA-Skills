# Wait

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Wait` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.wait`
- node group: `core-nodes`

## 核心要点

- Documentation for the Wait node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **After Time Interval**: The node waits for a certain amount of time.
- **At Specified Time**: The node waits until a specific time.
- **On Webhook Call**: The node waits until it receives an HTTP call.
- **On Form Submitted**: The node waits until it receives a form submission.
- **Wait Amount**: Enter the amount of time to wait.
- **Wait Unit**: Select the unit of measure for the **Wait Amount**. Choose from:
- **Seconds**
- **Minutes**
- **Hours**
- **Days**
- **Basic Auth**: Use basic authentication. Select or enter a new **Credential for Basic Auth** to use.
- **Header Auth**: Use header authentication. Select or enter a new **Credential for Header Auth** to use.
- **JWT Auth**: Use JWT authentication. Select or enter a new **Credential for JWT Auth** to use.
- **None**: Don't use authentication.
- **Immediately**: Respond as soon as the node executes.
- **When Last Node Finishes**: Return the response code and the data output from the last node executed in the workflow. If you select this option, also set:
- **Response Data**: Select what data should be returned and what format to use. Options include:
- **All Entries**: Returns all the entries of the last node in an array.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

