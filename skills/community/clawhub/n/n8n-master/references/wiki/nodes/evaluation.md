# Evaluation node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Evaluation node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.evaluation`
- node group: `core-nodes`

## 核心要点

- Documentation for the Evaluation node in n8n, a workflow automation platform. Includes guidance on usage and links to examples.

## 关键操作 / 参数线索

- **Set Outputs**: Write the results of an evaluation back to a data table or Google Sheet dataset.
- **Set Metrics**: Record metrics scoring the evaluation performance to n8n's **Evaluations** tab.
- **Check If Evaluating**: Branches the workflow execution logic depending on whether the current execution is an evaluation.
- **Source:** Select the location to which you want to output the evaluation results. Default value is **Data table**.
- When **Source** is **Data table**:
- **Data table:** Select a data table by name or ID
- When **Source** is **Google Sheets**:
- **Credential to connect with**: Create or select an existing Google Sheets credentials.
- **Document Containing Dataset**: Choose the spreadsheet document you want to write the evaluation results to. Usually this is the same document you select in the Evaluation Trigger node.
- Select **From list** to choose the spreadsheet title from the dropdown list, **By URL** to enter the url of the spreadsheet, or **By ID** to enter the `spreadsheetId`.
- You can find the `spreadsheetId` in a Google Sheets URL: `https://docs.google.com/spreadsheets/d/spreadsheetId/edit#gid=0`.
- **Sheet Containing Dataset**: Choose the sheet you want to write the evaluation results to. Usually this is the same sheet you select in the Evaluation Trigger node.
- Select **From list** to choose the sheet title from the dropdown list, **By URL** to enter the url of the sheet, **By ID** to enter the `sheetId`, or **By Name** to enter the sheet title.
- You can find the `sheetId` in a Google Sheets URL: `https://docs.google.com/spreadsheets/d/aBC-123_xYz/edit#gid=sheetId`.
- **Name**: The Google Sheet column name to write the evaluation results to.
- **Value**: The value to write to the Google Sheet.
- **Name**: The name to use for the metric.
- **Value**: The numeric value to record. Once you run your evaluation, you can drag and drop values from previous nodes here. Metric values must be numeric.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

