# MCP Client node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `MCP Client node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.mcpClient`
- node group: `core-nodes`

## 核心要点

- Learn how to use the MCP Client node in n8n. Follow technical documentation to integrate MCP Client node into your workflows.

## 关键操作 / 参数线索

- **Server Transport**: The transport protocol used by the MCP Server endpoint you want to connect to.
- **MCP Endpoint URL**: The URL of the external MCP Server. For example, `https://mcp.notion.com/mcp`.
- **Authentication**: The authentication method for authentication to your MCP server. The MCP Client node supports bearer, generic header, and OAuth2 authentication. Select **None** to attempt to connect without authentication.
- **Tool**: Select the tool to use in the node. The list of tools is automatically fetched from the external MCP server.
- **Input Mode**:
- **Manual**: Specify each tool parameter manually.
- **JSON**: Specify tool parameters as a JSON object. Use this mode for tools with nested parameters.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

