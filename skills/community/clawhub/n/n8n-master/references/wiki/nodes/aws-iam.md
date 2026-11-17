# AWS IAM node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `AWS IAM node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.awsiam`
- node group: `app-nodes`

## 核心要点

- Learn how to use the AWS IAM node in n8n. Follow technical documentation to integrate AWS IAM node into your workflows.

## 关键操作 / 参数线索

- **User**:
- **Add to Group**: Add an existing user to a group.
- **Create**: Create a new user.
- **Delete**: Delete a user.
- **Get**: Retrieve a user.
- **Get Many**: Retrieve a list of users.
- **Remove From Group**: Remove a user from a group.
- **Update**: Update an existing user.
- **Group**:
- **Create**: Create a new group.
- **Delete**: Create a new group.
- **Get**: Retrieve a group.
- **Get Many**: Retrieve a list of groups.
- **Update**: Update an existing group.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

