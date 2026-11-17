# n8n

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `n8n` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.n8n`
- node group: `core-nodes`

## 核心要点

- Documentation for the n8n node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- Audit
- **Generate** a security audit
- Credential
- **Create** a credential
- **Delete** a credential
- **Get Schema**: Use this operation to get credential data schema for type
- Execution
- **Get** an execution
- **Get Many** executions
- **Delete** an execution
- Workflow
- **Publish** a workflow
- **Create** a workflow
- **Deactivate** a workflow
- **Delete** a workflow
- **Get** a workflow
- **Get Many** workflows
- **Update** a workflow

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

