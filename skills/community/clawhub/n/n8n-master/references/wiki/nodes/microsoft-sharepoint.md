# Microsoft SharePoint node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Microsoft SharePoint node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.microsoftsharepoint`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Microsoft SharePoint node in n8n. Follow technical documentation to integrate Microsoft SharePoint node into your workflows.

## 关键操作 / 参数线索

- **File**:
- Download: Download a file.
- Update: Update a file.
- Upload: Upload an existing file.
- **Item**:
- Create: Create an item in an existing list.
- Create or Update: Create a new item, or update the current one if it already exists (upsert).
- Delete: Delete an item from a list.
- Get: Retrieve an item from a list.
- Get Many: Get specific items in a list or list many items.
- Update: Update an item in an existing list.
- **List**:
- Get: Retrieve details of a single list.
- Get Many: Retrieve a list of lists.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

