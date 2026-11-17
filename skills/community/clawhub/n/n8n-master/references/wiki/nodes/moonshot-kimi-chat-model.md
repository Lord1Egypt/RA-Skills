# Moonshot Kimi Chat Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Moonshot Kimi Chat Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmchatmoonshot`
- node group: `cluster-sub-nodes`

## 核心要点

- Integrate the Moonshot Kimi Chat Model into n8n workflows to generate chat responses for AI chains. Common uses include generating conversational replies, integrating with LangChain-style workflows, and tuning response behavior via temperature/top-p and token limits.

## 关键操作 / 参数线索

- **Model** (type: options, field: `model`): The model that generates the completion. Default: `kimi-k2.5`. Learn more at Moonshot Kimi Chat API docs.
- **Frequency Penalty** (type: number, field: `frequencyPenalty`): Positive values penalize new tokens based on their existing frequency, so the model repeats less. Default: `0`.
- **Maximum number of tokens** (type: number, field: `maxTokens`): The maximum number of tokens to generate in the completion. A value of -1 uses the model default. The token limit depends on the selected model. Default: `-1`.
- **Response format** (type: options, field: `responseFormat`): Format of the model response. Default: `text`.
- **Presence penalty** (type: number, field: `presencePenalty`): Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Default: `0`.
- **Sampling temperature** (type: number, field: `temperature`): Controls randomness. Lower values make outputs less random; near zero the model becomes more deterministic. Default: `0.7`.
- **Timeout** (type: number, field: `timeout`): Maximum time a request can take, in milliseconds. Default: 360000 (six minutes).
- **Max retries** (type: number, field: `maxRetries`): Maximum number of retries to attempt for failed requests. Default: two.
- **Top P** (type: number, field: `topP`): Nucleus sampling parameter controlling diversity. A value of zero point five means the model considers half of the likelihood-weighted options. We recommend changing either **Top P** or **Sampling Temperature**, don't change both. Default: `1`.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

