# OpenAI Chat Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `OpenAI Chat Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmchatopenai`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the OpenAI Chat Model node in n8n. Follow technical documentation to integrate OpenAI Chat Model node into your workflows.

## 关键操作 / 参数线索

- **Chat Completions**: The Chat Completions API endpoint generates a model response from a list of messages that comprise a conversation. The API requires the user to handle conversation state manually, for example by adding a Simple Memory subnode. For new projects, OpenAI recommends to use the Responses API.
- **Responses**: The Responses API is an agentic loop, allowing the model to call multiple built-in tools within the span of one API request. It also supports persistent conversations by passing a `conversation_id`.
- **Web Search**: Allows models to search the web for the latest information before generating a response.
- **File Search**: Allow models to search your knowledgebase from previously uploaded files for relevant information before generating a response. Refer to the OpenAI documentation for more information.
- **Code Interpreter**: Allows models to write and run Python code in a sandboxed environment.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

