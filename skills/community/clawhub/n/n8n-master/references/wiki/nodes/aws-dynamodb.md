# AWS DynamoDB node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `AWS DynamoDB node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.awsdynamodb`
- node group: `app-nodes`

## 核心要点

- Learn how to use the AWS DynamoDB node in n8n. Follow technical documentation to integrate AWS DynamoDB node into your workflows.

## 关键操作 / 参数线索

- Item
- Create a new record, or update the current one if it already exists (upsert/put)
- Delete an item
- Get an item
- Get all items

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

