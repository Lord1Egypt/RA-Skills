# MCP Server Trigger node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `MCP Server Trigger node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.mcptrigger`
- node group: `core-nodes`

## 核心要点

- Learn how to use the MCP Server Trigger node in n8n. Follow technical documentation to integrate the MCP Server Trigger node into your workflows.

## 关键操作 / 参数线索

- **Test**: n8n registers a test MCP URL when you select **Listen for Test Event** or **Execute workflow**, if the workflow isn't active. When you call the MCP URL, n8n displays the data in the workflow.
- **Production**: n8n registers a production MCP URL when you publish the workflow. When using the production URL, n8n doesn't display the data in the workflow. You can still view workflow data for a production execution: select the **Executions** tab in the workflow, then select the workflow execution you want to view.
- Bearer auth
- Header auth

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

