# AI Agent Tool node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `AI Agent Tool node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.toolaiagent`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the AI Agent Tool node in n8n. Follow technical documentation to integrate the AI Agent Tool node into your workflows.

## 关键操作 / 参数线索

- **Description**: Give a description to the LLM of this agent's purpose and scope of responsibility. A good, specific description tells the parent agent when to delegate tasks to this agent for processing.
- **Prompt (User Message)**: The prompt to the LLM explaining what actions to perform and what information to return.
- **Require Specific Output Format**: Whether you want the node to require a specific output format. When turned on, n8n prompts you to connect one of the output parsers described on the main agent page.
- **Enable Fallback Model**: Whether to enable a fallback model. When enabled, n8n prompts you to connect a backup chat model to use in case the primary model fails or isn't available.

## 常用选项线索

- **System Message**: A message to send to the agent before the conversation starts.
- **Max Iterations**: The maximum number of times the model should run to generate a response before stopping.
- **Return Intermediate Steps**: Whether to include intermediate steps the agent took in the final output.
- **Automatically Passthrough Binary Images**: Whether binary images should be automatically passed through to the agent as image type messages.
- **Batch Processing**: Whether to enable the following batch processing options for rate limiting:
- **Batch Size**: The number of items to process in parallel. This helps with rate limiting but may impact the log output ordering.
- **Delay Between Batches**: The number of milliseconds to wait between batches.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

