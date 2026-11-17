# Google Vertex Chat Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Google Vertex Chat Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmchatgooglevertex`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the Google Vertex Chat Model node in n8n. Follow technical documentation to integrate Google Vertex Chat Model node into your workflows.

## 关键操作 / 参数线索

- **Project ID**: Select the project ID from your Google Cloud account to use. n8n dynamically loads projects from the Google Cloud account, but you can also enter it manually.
- **Model Name**: Select the name of the model to use to generate the completion, for example `gemini-1.5-flash-001`, `gemini-1.5-pro-001`, etc. Refer to Google models for a list of available models.

## 常用选项线索

- **Maximum Number of Tokens**: Enter the maximum number of tokens used, which sets the completion length.
- **Sampling Temperature**: Use this option to control the randomness of the sampling process. A higher temperature creates more diverse sampling, but increases the risk of hallucinations.
- **Thinking Budget**: Controls reasoning tokens for thinking models. Set to `0` to disable automatic thinking. Set to `-1` for dynamic thinking. Leave empty for auto mode.
- **Top K**: Enter the number of token choices the model uses to generate the next token.
- **Top P**: Use this option to set the probability the completion should use. Use a lower value to ignore less probable options.
- **Safety Settings**: Gemini supports adjustable safety settings. Refer to Google's Gemini API safety settings for information on the available filters and levels.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

