# giggle-video 实现：giggle.pro

> 本文件是 `SKILL.md` 的实现层，描述如何通过 giggle.pro API 生成视频。

## 基础信息

| 字段              | 值                                                    |
| ----------------- | ----------------------------------------------------- |
| platform id       | `giggle`                                              |
| 网络白名单        | `api.giggle.pro`, `cdn.giggle.pro`                    |
| 认证方式          | Bearer Token                                          |
| API Key 环境变量  | `GIGGLE_API_KEY`                                      |
| Base URL 环境变量 | `GIGGLE_API_BASE`（默认 `https://api.giggle.pro/v1`） |

## 提交生成任务

```
POST ${GIGGLE_API_BASE}/video/generate
Headers:
  Authorization: Bearer ${GIGGLE_API_KEY}
  Content-Type: application/json

Body:
{
  "prompt":       "{prompt}",
  "style":        "{style}",
  "duration":     {duration},
  "aspect_ratio": "{aspect_ratio}",
  "resolution":   "{resolution}"
}

响应:
{
  "task_id": "giggle_task_abc123",
  "status":  "queued",
  "estimatedSeconds": 120
}
```

## 查询任务状态

```
GET ${GIGGLE_API_BASE}/video/status/{task_id}
Headers:
  Authorization: Bearer ${GIGGLE_API_KEY}

响应:
{
  "task_id": "giggle_task_abc123",
  "status":  "queued | processing | completed | failed",
  "progress": 0.75,
  "videoUrl": "https://cdn.giggle.pro/output/xxx.mp4",  // 仅 completed 时存在
  "error":    "..."                                       // 仅 failed 时存在
}
```

轮询策略：间隔 10s，最长等待 600s，超时后保留 task_id 供用户稍后查询。

## 状态映射到接口层

| giggle status       | 接口层 status |
| ------------------- | ------------- |
| queued / processing | in_progress   |
| completed           | completed     |
| failed              | failed        |

## 费用估算

调用前可先查询预估费用（可选）：

```
POST ${GIGGLE_API_BASE}/video/estimate
Body: 同 generate（不实际生成）
响应: { "estimatedCostUSD": 3.50 }
```

超过 $5 时，向用户告知并获取确认后再提交正式请求。

## 错误码对照

| HTTP 状态 | 含义                    | 处理方式                   |
| --------- | ----------------------- | -------------------------- |
| 400       | prompt 不合规或参数无效 | 提示用户修改提示词或参数   |
| 402       | 账户额度不足            | 通知用户充值或联系管理员   |
| 429       | 请求频率超限            | 等待 60s 后重试，最多 3 次 |
| 500/503   | 服务故障                | 记录错误，建议用户稍后重试 |
