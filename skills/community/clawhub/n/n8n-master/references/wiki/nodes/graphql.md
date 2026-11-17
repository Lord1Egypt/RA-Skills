# GraphQL

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `GraphQL` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.graphql`
- node group: `core-nodes`

## 核心要点

- Documentation for the GraphQL node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **GET**
- **POST**: If you select this method, you'll also need to select the **Request Format** the node should use for the query payload. Choose from:
- **GraphQL (Raw)**
- **JSON**
- **String**: If you select this format, enter a **Response Data Property Name** to define the property the string is written to.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

