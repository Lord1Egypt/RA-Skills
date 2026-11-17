# Embeddings Mistral Cloud node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Embeddings Mistral Cloud node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.embeddingsmistralcloud`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the Embeddings Mistral Cloud node in n8n. Follow technical documentation to integrate Embeddings Mistral Cloud node into your workflows.

## 关键操作 / 参数线索

- **Model**: Select the model to use to generate the embedding.

## 常用选项线索

- **Batch Size**: Enter the maximum number of documents to send in each request.
- **Strip New Lines**: Select whether to remove new line characters from input text (turned on) or not (turned off). n8n enables this by default.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

