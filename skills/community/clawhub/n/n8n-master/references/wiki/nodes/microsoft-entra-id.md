# Microsoft Entra ID node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Microsoft Entra ID node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.microsoftentra`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Microsoft Entra ID node in n8n. Follow technical documentation to integrate Microsoft Entra ID node into your workflows.

## 关键操作 / 参数线索

- **Group**
- **Create**: Create a new group
- **Delete**: Delete an existing group
- **Get**: Retrieve data for a specific group
- **Get Many**: Retrieve a list of groups
- **Update**: Update a group
- **User**
- **Create**: Create a new user
- **Delete**: Delete an existing user
- **Get**: Retrieve data for a specific user
- **Get Many**: Retrieve a list of users
- **Update**: Update a user
- **Add to Group**: Add user to a group
- **Remove from Group**: Remove user from a group

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

