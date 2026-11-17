# Chroma Vector Store node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Chroma Vector Store node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.vectorstorechroma`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the Chroma Vector Store node in n8n. Follow technical documentation to integrate Chroma Vector Store node into your workflows.

## 关键操作 / 参数线索

- **Chroma collection name**: Select your collection from the fetched collections list.
- **Prompt**: Enter the search query.
- **Limit**: Enter how many results to retrieve from the vector store. For example, set this to `5` to get the five best results.
- **Description**: Explain to the LLM what this tool does. A good, specific description allows LLMs to produce expected results more often.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

