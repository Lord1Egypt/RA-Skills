# Google Sheets

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Google Sheets` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.googlesheets`
- node group: `app-nodes`

## 核心要点

- Documentation for the Google Sheets node in n8n, a workflow automation platform. Includes details of operations and configuration, and links to examples and credentials information.

## 关键操作 / 参数线索

- **Document**
- **Create** a spreadsheet.
- **Delete** a spreadsheet.
- **Sheet Within Document**
- **Append or Update Row**: Append a new row, or update the current one if it already exists.
- **Append Row**: Create a new row.
- **Clear** all data from a sheet.
- **Create** a new sheet.
- **Delete** a sheet.
- **Delete Rows or Columns**: Delete columns and rows from a sheet.
- **Get Row(s)**: Read all rows in a sheet.
- **Update Row**: Update a row in a sheet.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

