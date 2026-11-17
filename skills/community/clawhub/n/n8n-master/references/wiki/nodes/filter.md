# Filter

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Filter` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.filter`
- node group: `core-nodes`

## 核心要点

- Documentation for the Filter node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- Use the data type dropdown to select the data type and comparison operation type for your condition. For example, to filter for dates after a particular date, select **Date & Time > is after**.
- The fields and values to enter into the condition change based on the data type and comparison you select. Refer to Available data type comparisons for a full list of all comparisons by data type.
- When they meet all conditions: Create two or more conditions and select **AND** in the dropdown between them.
- When they meet any of the conditions: Create two or more conditions and select **OR** in the dropdown between them.

## 常用选项线索

- **Ignore Case**: Whether to ignore letter case (turned on) or be case sensitive (turned off).
- **Less Strict Type Validation**: Whether you want n8n to attempt to convert value types based on the operator you choose (turned on) or not (turned off). Turn this on when facing a "wrong type:" error in your node.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

