# Airtable Trigger node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Airtable Trigger node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.airtabletrigger`
- node group: `trigger-nodes`

## 核心要点

- Learn how to use the Airtable Trigger node in n8n. Follow technical documentation to integrate Airtable Trigger node into your workflows.

## 关键操作 / 参数线索

- Every Minute
- Every Hour
- Every Day
- Every Week
- Every Month
- Every X: Check for updates every given number of minutes or hours.
- Custom: Customize the polling interval by providing a cron expression.
- **Fields**: A comma-separated list of fields to include in the output. If you don't specify anything here, the output will contain only the **Trigger Field**.
- **Formula**: An Airtable formula to further filter the results. You can use this to add further constraints to the events that trigger the workflow. Note that formula values aren't taken into account for manual executions, only for production polling.
- **View ID**: The name or ID of a table view. When defined, only returns records available in the given view.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

