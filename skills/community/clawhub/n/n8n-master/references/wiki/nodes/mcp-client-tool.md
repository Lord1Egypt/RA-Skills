# MCP Client Tool node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `MCP Client Tool node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.toolmcp`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the MCP Client Tool node in n8n. Follow technical documentation to integrate MCP Client Tool node into your workflows.

## 关键操作 / 参数线索

- **SSE Endpoint**: The SSE endpoint for the MCP server you want to connect to.
- **Authentication**: The authentication method for authentication to your MCP server. The MCP tool supports bearer, generic header, and OAuth2 authentication. Select **None** to attempt to connect without authentication.
- **Tools to Include**: Choose which tools you want to expose to the AI Agent:
- **All**: Expose all the tools given by the MCP server.
- **Selected**: Activates a **Tools to Include** parameter where you can select the tools you want to expose to the AI Agent.
- **All Except**: Activates a **Tools to Exclude** parameter where you can select the tools you want to avoid sharing with the AI Agent. The AI Agent will have access to all MCP server's tools that aren't selected.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

