# Summarize

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Summarize` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.summarize`
- node group: `core-nodes`

## 核心要点

- Documentation for the Summarize node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Aggregation**: Select the aggregation method to use on a given field. Options include:
- **Append**: Append
- If you select this option, decide whether you want to **Include Empty Values** or not.
- **Average**: Calculate the numeric average of your input data.
- **Concatenate**: Combine together values in your input data.
- **Separator**: Select the separator you want to insert between concatenated values.
- **Count**: Count the total number of values in your input data.
- **Count Unique**: Count the number of unique values in your input data.
- **Max**: Find the highest numeric value in your input data.
- **Min**: Find the lowest numeric value in your input data.
- **Sum**: Add together the numeric values in your input data.
- **Field**: Enter the name of the field you want to perform the aggregation on.

## 常用选项线索

- **Each Split in a Separate Item**: Use this option to generate a separate output item for each split out field.
- **All Splits in a Single Item**: Use this option to generate a single item that lists the split out fields.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

