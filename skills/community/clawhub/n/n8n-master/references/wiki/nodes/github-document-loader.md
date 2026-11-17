# GitHub Document Loader node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `GitHub Document Loader node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.documentgithubloader`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the GitHub Document Loader node in n8n. Follow technical documentation to integrate GitHub Document Loader node into your workflows.

## 关键操作 / 参数线索

- **Text Splitting**: Choose from:
- **Simple**: Uses the Recursive Character Text Splitter with a chunk size of 1000 and an overlap of 200.
- **Custom**: Allows you to connect a text splitter of your choice.
- **Repository Link**: Enter the URL of your GitHub repository.
- **Branch**: Enter the branch name to use.

## 常用选项线索

- **Recursive**: Select whether to include sub-folders and files (turned on) or not (turned off).
- **Ignore Paths**: Enter directories to ignore.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

