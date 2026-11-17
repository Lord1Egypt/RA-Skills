# Azure AI Search Vector Store node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Azure AI Search Vector Store node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.vectorstoreazureaisearch`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the Azure AI Search Vector Store node in n8n. Follow technical documentation to integrate Azure AI Search Vector Store node into your workflows.

## 关键操作 / 参数线索

- **Endpoint**: Your Azure AI Search endpoint (format: `https://your-service.search.windows.net`)
- **Index Name**: The index to query
- **Limit**: Maximum documents to return (default: 4)
- **Endpoint**: Your Azure AI Search endpoint
- **Index Name**: The index to use (created automatically if it doesn't exist)
- **Batch Size**: Number of documents uploaded per batch to Azure AI Search. Adjust based on document size and your service tier limits. This controls upload batching only—embedding generation batching is configured in embedding nodes.
- **Index Name**: The index to update
- **Name**: Tool name shown to the LLM
- **Description**: Explain to the LLM what this tool does. Be specific to help the LLM choose when to use this tool.
- **Limit**: Maximum results to retrieve (e.g., `10` for ten best matches)

## 常用选项线索

- **Filter**: OData filter expression to filter results by document fields or metadata. See filter examples below.
- **Query Mode**: Search strategy to use:
- **Vector**: Similarity search using embeddings only
- **Keyword**: Full-text search using BM25 ranking
- **Hybrid** (default): Combines vector and keyword search with Reciprocal Rank Fusion (RRF)
- **Semantic Hybrid**: Hybrid search with semantic reranking for improved relevance
- **Semantic Configuration**: Name of the semantic configuration to use for semantic ranking. Defaults to `semantic-search-config` if not specified. Only required if you pre-created an index with a custom semantic configuration name.
- Comparison: `eq`, `ne`, `gt`, `ge`, `lt`, `le`
- Logical: `and`, `or`, `not`
- String functions: `startswith()`, `endswith()`, `contains()`

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

