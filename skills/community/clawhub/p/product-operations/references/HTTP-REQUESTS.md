# HTTP 请求

请求使用 Bearer Token，并为每次逻辑操作生成一个不会重复使用的幂等键：

```sh
curl -sS -X POST "${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1/product-operations/operation.plan" \
  -H "Authorization: Bearer ${PRODUCT_OPERATIONS_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 生成的UUID" \
  -d '{"product_name":"秋季会员活动","goal":"30天新增1000名注册用户","start_date":"2026-09-05","end_date":"2026-10-04","channels":["wechat","xiaohongshu"],"budget":"3000.00","team_size":2}'
```

同步请求成功时返回 `status: succeeded`。任务详情接口为：

`GET /api/v1/product-operations/{operation}/tasks/{task_id}`

响应头 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged` 和 `X-AI-Skills-Billing-Balance` 分别表示计费币种、本次扣费和剩余余额。

每次重试同一逻辑请求时沿用原幂等键；参数发生变化时必须使用新键。HTTP 422 表示字段错误，402 表示余额或限额不足，409 表示幂等键冲突。
