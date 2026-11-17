# Convert to File

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Convert to File` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.converttofile`
- node group: `core-nodes`

## 核心要点

- Documentation for the Convert to File node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Convert to CSV**
- **Convert to HTML**
- **Convert to ICS**
- **Convert to JSON**
- **Convert to ODS**
- **Convert to RTF**
- **Convert to Text File**
- **Convert to XLS**
- **Convert to XLSX**
- **Move Base64 String to File**
- **File Name**: Enter the file name for the generated output file.
- If the first row of the file contains header names, turn on the **Header Row** option.
- **Put Output File in Field**. Enter the name of the field in the output data to contain the file.
- **Event Title**: Enter the title for the event.
- **Start**: Enter the date and time the event will start. All-day events ignore the time.
- **End**: Enter the date and time the event will end. All-day events ignore the time. If unset, the node uses the start date.
- **All Day**: Select whether the event is an all day event (turned on) or not (turned off).
- **Attendees**: Use this option to add attendees to the event. For each attendee, add:

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

