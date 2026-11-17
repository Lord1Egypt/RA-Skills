# Schedule Trigger node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Schedule Trigger node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.scheduletrigger`
- node group: `core-nodes`

## 核心要点

- Learn how to use the Schedule Trigger node in n8n. Follow technical documentation to integrate Schedule Trigger node into your workflows.

## 关键操作 / 参数线索

- Seconds trigger interval
- Minutes trigger interval
- Hours trigger interval
- Days trigger interval
- Weeks trigger interval
- Months trigger interval
- Custom (Cron) interval
- **Seconds Between Triggers**: Enter the number of seconds between each workflow trigger. For example, if you enter `30` here, the trigger will run every 30 seconds.
- **Minutes Between Triggers**: Enter the number of minutes between each workflow trigger. For example, if you enter `5` here, the trigger will run every 5 minutes.
- **Hours Between Triggers**: Enter the number of hours between each workflow trigger.
- **Trigger at Minute**: Enter the minute past the hour to trigger the node when it runs, from `0` to `59`.
- **Days Between Triggers**: Enter the number of days between each workflow trigger.
- **Trigger at Hour**: Select the hour of the day to trigger the node.
- **Weeks Between Triggers**: Enter the number of weeks between each workflow trigger.
- **Trigger on Weekdays**: Select the day(s) of the week you want to trigger the node.
- **Months Between Triggers**: Enter the number of months between each workflow trigger.
- **Trigger at Day of Month**: Enter the day of the month the day should trigger at, from `1` to `31`. If a month doesn't have this day, the node won't trigger. For example, if you enter `30` here, the node won't trigger in February.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

