# Switch

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Switch` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.switch`
- node group: `core-nodes`

## 核心要点

- Documentation for the Switch node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Rules**: Select this mode to build a matching rule for each output.
- **Expression**: Select this mode to write an expression to return the output index programmatically.
- Create **Routing Rules** to define comparison conditions.
- Use the data type dropdown to select the data type and comparison operation type for your condition. For example, to create a rules for dates after a particular date, select **Date & Time > is after**.
- The fields and values to enter into the condition change based on the data type and comparison you select. Refer to Available data type comparisons for a full list of all comparisons by data type.
- **Rename Output**: Turn this control on to rename the output field to put matching data into. Enter your desired **Output Name**.
- **Fallback Output**: Choose how to route the workflow when an item doesn't match any of the rules or conditions.
- **None**: Ignore the item. This is the default behavior.
- **Extra Output**: Send items to an extra, separate output.
- **Output 0**: Send items to the same output as those matching the first rule.
- **Ignore Case**: Set whether to ignore letter case when evaluating conditions (turned on) or enforce letter case (turned off).
- **Less Strict Type Validation**: Set whether you want n8n to attempt to convert value types based on the operator you choose (turned on) or not (turned off).
- **Send data to all matching outputs**: Set whether to send data to all outputs meeting conditions (turned on) or whether to send the data to the first output matching the conditions (turned off).
- **Number of Outputs**: Set how many outputs the node should have.
- **Output Index**: Create an expression to calculate which input item should be routed to which output. The expression must return a number.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

