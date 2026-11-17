# Azure Storage node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Azure Storage node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.azurestorage`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Azure Storage node in n8n. Follow technical documentation to integrate Azure Storage node into your workflows.

## 关键操作 / 参数线索

- **Blob**
- **Create blob**: Create a new blob or replace an existing one.
- **Delete blob**: Delete an existing blob.
- **Get blob**: Retrieve data for a specific blob.
- **Get many blobs**: Retrieve a list of blobs.
- **Container**
- **Create container**: Create a new container.
- **Delete container**: Delete an existing container.
- **Get container**: Retrieve data for a specific container.
- **Get many containers**: Retrieve a list of containers.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

