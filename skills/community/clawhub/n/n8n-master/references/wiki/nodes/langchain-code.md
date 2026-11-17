# LangChain Code node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `LangChain Code node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.code`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the LangChain Code node in n8n. Follow technical documentation to integrate LangChain Code node into your workflows.

## 关键操作 / 参数线索

- **Execute**: use the LangChain Code node like n8n's own Code node. This takes input data from the workflow, processes it, and returns it as the node output. This mode requires a main input and output. You must create these connections in **Inputs** and **Outputs**.
- **Supply Data**: use the LangChain Code node as a sub-node, sending data to a root node. This uses an output other than main.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

