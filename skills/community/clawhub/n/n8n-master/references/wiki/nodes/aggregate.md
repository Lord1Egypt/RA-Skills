# Aggregate

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Aggregate` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.aggregate`
- node group: `core-nodes`

## 核心要点

- Documentation for the Aggregate node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Individual Fields**: Aggregate individual fields separately.
- **All Item Data**: Aggregate all item data into a single list.
- **Input Field Name**: Enter the name of the field in the input data to aggregate together.
- **Rename Field**: This toggle controls whether to give the field a different name in the aggregated output data. Turn this on to add a different field name. If you're aggregating multiple fields, you must provide new output field names. You can't leave multiple fields undefined.
- **Output Field Name**: This field is displayed when you turn on **Rename Field**. Enter the field name for the aggregated output data.
- **Put Output in Field**: Enter the name of the field to output the data in.
- **Include**: Select which fields to include in the output. Choose from:
- **All fields**: The output includes data from all fields with no further parameters.
- **Specified Fields**: If you select this option, enter a comma-separated list of fields the output should include data from in the **Fields To Include** parameter. The output will include only the fields in this list.
- **All Fields Except**: If you select this option, enter a comma-separated list of fields the output should exclude data from in the **Fields To Exclude** parameter. The output will include all fields not in this list.

## 常用选项线索

- **Disable Dot Notation**: The node displays this toggle when you select the **Individual Fields** Aggregate. It controls whether to disallow referencing child fields using `parent.child` in the field name (turned on), or allow it (turned off, default).
- **Merge Lists**: The node displays this toggle when you select the **Individual Fields** Aggregate. Turn it on if the field to aggregate is a list and you want to output a single flat list rather than a list of lists.
- **Include Binaries**: The node displays this toggle for both Aggregate types. Turn it on if you want to include binary data from the input in the new output.
- **Keep Missing And Null Values**: The node displays this toggle when you select the **Individual Fields** Aggregate. Turn it on to add a null (empty) entry in the output list when there is a null or missing value in the input. If turned off, the output ignores null or empty values.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

