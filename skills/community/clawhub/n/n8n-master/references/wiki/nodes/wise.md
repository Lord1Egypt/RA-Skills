# Wise node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Wise node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.wise`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Wise node in n8n. Follow technical documentation to integrate Wise node into your workflows.

## 关键操作 / 参数线索

- Account
- Retrieve balances for all account currencies of this user.
- Retrieve currencies in the borderless account of this user.
- Retrieve the statement for the borderless account of this user.
- Exchange Rate
- Get
- Profile
- Get All
- Recipient
- Quote
- Create
- Transfer
- Delete
- Execute

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

