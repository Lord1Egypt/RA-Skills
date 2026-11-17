# PGVector Vector Store node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `PGVector Vector Store node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.vectorstorepgvector`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the PGVector Vector Store node in n8n. Follow technical documentation to integrate PGVector Vector Store node into your workflows.

## 关键操作 / 参数线索

- **Table name**: Enter the name of the table you want to query.
- **Prompt**: Enter your search query.
- **Limit**: Enter a number to set how many results to retrieve from the vector store. For example, set this to `10` to get the ten best results.
- **Name**: The name of the vector store.
- **Description**: Explain to the LLM what this tool does. A good, specific description allows LLMs to produce expected results more often.
- **Table Name**: Enter the PGVector table to use.
- **Limit**: Enter how many results to retrieve from the vector store. For example, set this to `10` to get the ten best results.

## 常用选项线索

- **Use Collection**: Select whether to use a collection (turned on) or not (turned off).
- **Collection Name**: Enter the name of the collection you want to use.
- **Collection Table Name**: Enter the name of the table to store collection information in.
- **ID Column Name**
- **Vector Column Name**
- **Content Column Name**
- **Metadata Column Name**

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

