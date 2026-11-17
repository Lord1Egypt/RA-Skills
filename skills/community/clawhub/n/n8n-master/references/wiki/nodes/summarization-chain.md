# Summarization Chain node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Summarization Chain node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.chainsummarization`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the Summarize Chain node in n8n. Follow technical documentation to integrate Summarize Chain node into your workflows.

## 关键操作 / 参数线索

- **Use Node Input (JSON)** and **Use Node Input (Binary)**: summarize the data coming into the node from the workflow.
- You can configure the **Chunking Strategy**: choose what strategy to use to define the data chunk sizes.
- If you choose **Simple (Define Below)** you can then set **Characters Per Chunk** and **Chunk Overlap (Characters)**.
- Choose **Advanced** if you want to connect a splitter sub-node that provides more configuration options.
- **Use Document Loader**: summarize data provided by a document loader sub-node.

## 常用选项线索

- **Map Reduce**: this is the recommended option. Learn more about Map Reduce in the LangChain documentation.
- **Refine**: learn more about Refine in the LangChain documentation.
- **Stuff**: learn more about Stuff in the LangChain documentation.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

