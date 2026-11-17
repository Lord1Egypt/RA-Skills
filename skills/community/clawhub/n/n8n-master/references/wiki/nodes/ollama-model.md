# Ollama Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Ollama Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmollama`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the Ollama Model node in n8n. Follow technical documentation to integrate Ollama Model node into your workflows.

## 关键操作 / 参数线索

- **Model**: Select the model that generates the completion. Choose from:
- **Llama2**
- **Llama2 13B**
- **Llama2 70B**
- **Llama2 Uncensored**

## 常用选项线索

- **Sampling Temperature**: Use this option to control the randomness of the sampling process. A higher temperature creates more diverse sampling, but increases the risk of hallucinations.
- **Top K**: Enter the number of token choices the model uses to generate the next token.
- **Top P**: Use this option to set the probability the completion should use. Use a lower value to ignore less probable options.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

