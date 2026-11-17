# HTTP 请求、上传、幂等与任务轮询

令 `BASE=${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net/api/v1}`。每个新业务动作生成 UUID `Idempotency-Key`；所有请求携带 `Authorization: Bearer ${MEETING_MINUTES_ACTION_ITEMS_API_KEY:-$AI_SKILLS_API_KEY}`。文件入口使用 `multipart/form-data`；直接文字也可用该入口。其他入口使用 `Content-Type: application/json`。

- `POST /api/v1/meeting-minutes-action-items/meeting.analyze`；`GET /api/v1/meeting-minutes-action-items/meeting.analyze/tasks/{task_id}`
- `POST /api/v1/meeting-minutes-action-items/meeting.export`；`GET /api/v1/meeting-minutes-action-items/meeting.export/tasks/{task_id}`

```sh
curl -sS -X POST "$BASE/meeting-minutes-action-items/meeting.analyze" \
  -H "Authorization: Bearer ${MEETING_MINUTES_ACTION_ITEMS_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: $REQUEST_UUID" \
  -F "file=@meeting.vtt" -F "timezone=Asia/Shanghai"
```

`200` 表示完成，`202` 表示已接收。收到 `202` 后有限退避轮询对应 `/tasks/{task_id}`，读取 `succeeded`、`partial`、`failed` 与 `artifacts`。优先读取 `errors.code`，兼容 `error.code`。结果不确定时只重放相同输入和原键。
