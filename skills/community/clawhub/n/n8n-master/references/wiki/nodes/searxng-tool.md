# SearXNG Tool node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `SearXNG Tool node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.toolsearxng`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the SearXNG Tool node in n8n. Follow technical documentation to integrate SearXNG Tool node into your workflows.

## 关键操作 / 参数线索

- Node Options
- Running a SearXNG instance
- Templates and examples
- Related resources

## 常用选项线索

- **Number of Results**: The number of results to retrieve. The default is 10.
- **Page Number**: The page number of the search results to retrieve. The default is 1.
- **Language**: A two-letter language code to filter search results by language. For example: `en` for English, `fr` for French. The default is `en`.
- **Safe Search**: Enables or disables filtering explicit content in the search results. Can be None, Moderate, or Strict. The default is None.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

