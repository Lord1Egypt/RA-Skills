# Embeddings OpenAI node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Embeddings OpenAI node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.embeddingsopenai`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the Embeddings OpenAI node in n8n. Follow technical documentation to integrate Embeddings OpenAI node into your workflows.

## 关键操作 / 参数线索

- Node options
- Templates and examples
- Related resources

## 常用选项线索

- **Model**: Select the model to use for generating embeddings.
- **Base URL**: Enter the URL to send the request to. Use this if you are using a self-hosted OpenAI-like model.
- **Batch Size**: Enter the maximum number of documents to send in each request.
- **Strip New Lines**: Select whether to remove new line characters from input text (turned on) or not (turned off). n8n enables this by default.
- **Timeout**: Enter the maximum amount of time a request can take in seconds. Set to `-1` for no timeout.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

