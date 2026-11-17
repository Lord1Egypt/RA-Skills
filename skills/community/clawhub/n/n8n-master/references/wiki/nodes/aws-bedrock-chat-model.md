# AWS Bedrock Chat Model node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `AWS Bedrock Chat Model node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.lmchatawsbedrock`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the AWS Bedrock Chat Model node in n8n. Follow technical documentation to integrate AWS Bedrock Chat Model node into your workflows.

## 关键操作 / 参数线索

- **Model**: Select the model that generates the completion.

## 常用选项线索

- **Maximum Number of Tokens**: Enter the maximum number of tokens used, which sets the completion length.
- **Sampling Temperature**: Use this option to control the randomness of the sampling process. A higher temperature creates more diverse sampling, but increases the risk of hallucinations.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

