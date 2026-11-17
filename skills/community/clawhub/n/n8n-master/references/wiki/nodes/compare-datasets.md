# Compare Datasets

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Compare Datasets` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.comparedatasets`
- node group: `core-nodes`

## 核心要点

- Documentation for the Compare Datasets node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Use Input A Version** to treat input stream A as the source of truth.
- **Use Input B Version** to treat input stream B as the source of truth.
- **Use a Mix of Versions** to use different inputs for different fields.
- Use **Prefer** to select either **Input A Version** or **Input B Version** as the main source of truth.
- Enter input fields that are exceptions to **For Everything Except** to pull from the other input source. To add multiple input fields, enter a comma-separated list.
- **Include Both Versions** to include both input streams in the output, which may make the structure more complex.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

