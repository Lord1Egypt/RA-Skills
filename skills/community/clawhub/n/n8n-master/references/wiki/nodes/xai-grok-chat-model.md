# xAI Grok Chat Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `xAI Grok Chat Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmchatxaigrok`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the xAI Grok Chat Model node in n8n. Follow technical documentation to integrate xAI Grok Chat Model node into your workflows.

## 关键操作 / 参数线索

- **Model**: Select the model which will generate the completion. n8n dynamically loads available models from the xAI Grok API. Learn more in the xAI Grok model documentation.

## 常用选项线索

- **Frequency Penalty**: Use this option to control the chances of the model repeating itself. Higher values reduce the chance of the model repeating itself.
- **Maximum Number of Tokens**: Enter the maximum number of tokens used, which sets the completion length. Most models have a context length of 2048 tokens with the newest models supporting up to 32,768 tokens.
- **Response Format**: Choose **Text** or **JSON**. **JSON** ensures the model returns valid JSON.
- **Presence Penalty**: Use this option to control the chances of the model talking about new topics. Higher values increase the chance of the model talking about new topics.
- **Sampling Temperature**: Use this option to control the randomness of the sampling process. A higher temperature creates more diverse sampling, but increases the risk of hallucinations.
- **Timeout**: Enter the maximum request time in milliseconds.
- **Max Retries**: Enter the maximum number of times to retry a request.
- **Top P**: Use this option to set the probability the completion should use. Use a lower value to ignore less probable options.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

