# Simple Vector Store node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Simple Vector Store node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.vectorstoreinmemory`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the Simple Vector Store node in n8n. Follow technical documentation to integrate Simple Vector Store node into your workflows.

## 关键操作 / 参数线索

- **Memory Key**: Select or create the key containing the vector memory you want to query.
- **Prompt**: Enter the search query.
- **Limit**: Enter how many results to retrieve from the vector store. For example, set this to `10` to get the ten best results.
- **Memory Key**: Select or create the key you want to store the vector memory as.
- **Clear Store**: Use this parameter to control whether to wipe the vector store for the given memory key for this workflow before inserting data (turned on).
- **Name**: The name of the vector store.
- **Description**: Explain to the LLM what this tool does. A good, specific description allows LLMs to produce expected results more often.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

