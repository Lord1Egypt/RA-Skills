# MiniMax Chat Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `MiniMax Chat Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmchatminimax`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the MiniMax Chat Model node in n8n. Follow technical documentation to integrate MiniMax Chat Model node into your workflows.

## 关键操作 / 参数线索

- **Model**: Select the model that generates the completion. Refer to MiniMax's model documentation for the available models.

## 常用选项线索

- **Hide Thinking**: When turned on (default), the node strips `` tags from the model's response. Turn this off to include the model's reasoning in the output.
- **Maximum Number of Tokens**: Enter the maximum number of tokens used, which sets the completion length.
- **Sampling Temperature**: Use this option to control the randomness of the sampling process. A higher temperature creates more diverse sampling, but increases the risk of hallucinations.
- **Timeout**: Enter the maximum request time in milliseconds.
- **Max Retries**: Enter the maximum number of times to retry a request.
- **Top P**: Use this option to set the probability the completion should use. Use a lower value to ignore less probable options.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

