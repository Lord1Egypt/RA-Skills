# Alibaba Cloud Chat Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Alibaba Cloud Chat Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmchatalibabacloud`
- node group: `cluster-sub-nodes`

## 核心要点

- The Alibaba Cloud Chat Model node sends prompts to Alibaba Cloud's conversational models (for advanced AI chains). This page explains how to configure the node in n8n workflows and covers common uses such as generating chat responses, tweaking sampling parameters (temperature, top_p), and limiting output length.

## 关键操作 / 参数线索

- **Model** (type: _options_, field: `model`): The model that generates the completion. Learn more about available models on Alibaba Cloud: Alibaba Cloud Model Studio — Models.
- **Frequency Penalty** (type: _number_, field: `frequencyPenalty`): Positive values penalize new tokens based on how often they appear so far, decreasing the model's likelihood to repeat the same line verbatim. Default: `0`.
- **Maximum Number of Tokens** (type: _number_, field: `maxTokens`): The maximum number of tokens to generate in the completion. The limit depends on the selected model. A value of minus one uses the model's default limit. Default: `-1`.
- **Response Format** (type: _options_, field: `responseFormat`): The output format returned by the node, for example plain text or structured formats. Default: text.
- **Presence Penalty** (type: _number_, field: `presencePenalty`): Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to discuss new topics. Default: `0`.
- **Sampling Temperature** (type: _number_, field: `temperature`): Control randomness. Lower values make output less random, near zero is deterministic. Default: `0.7`.
- **Timeout** (type: _number_, field: `timeout`): Maximum time (in milliseconds) allowed for a request before it's aborted. Default: `360000`.
- **Max Retries** (type: _number_, field: `maxRetries`): Maximum number of retry attempts for failed requests. Default: `2`.
- **Top P** (type: _number_, field: `topP`): Nucleus sampling parameter that controls diversity. 0.5 means half of the probability mass is considered. Adjust **Top P** or **Sampling Temperature**, but not both. Default: `1`.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

