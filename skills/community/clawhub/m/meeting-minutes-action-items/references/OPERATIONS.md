# 操作字段与结果

## 整理会议纪要

`meeting.analyze` 使用 `multipart/form-data`，在 `file` 与 `transcript` 中二选一。文件支持 TXT、MD、VTT、SRT、DOCX、PDF，最大 10 MiB；文字为 20 至 120000 字符。必填 `timezone`，可选 `title`、`meeting_date`（`YYYY-MM-DD`）与 `instructions`。

结果包含 `summary`、`decisions`、`action_items`、`risks`、`open_questions`、`follow_up_message`、`coverage` 和 `limitations`。行动项包含 `task`、可空 `owner`、可空 `due_date`、`priority`、`status`、`tentative`、`confidence` 与可核验证据。

## 导出会议交付物

`meeting.export` 接收当前用户七日内成功的 `analyze_task_id`，以及 1 至 3 个 `formats`：`markdown`、`docx`、`pdf`。返回私有 `artifacts`，导出不会发送消息、创建日历或写入任务系统。
