# Loudy.ai API Reference

## Base URL
```
https://api.loudy.ai
```

## Common Headers
所有接口需要：
```
X-API-Key: <YOUR_API_KEY>
```

## Endpoints

### 1. 获取奖池列表
```
GET /app-api/open-api/v1/earning-pools
```
Query: (none)

Response:
```json
{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "id": 123,
      "sponsor": "Sponsor Name",
      "price": "$4,000",
      "curator": "Curator Name",
      "distribution": "Equal Share",
      "activityStart": "2024-01-01T00:00:00Z",
      "activityEnd": "2024-01-31T00:00:00Z",
      "platform": "X / Twitter",
      "brief": "Task description",
      "briefLink": "https://...",
      "status": "Ongoing"
    }
  ]
}
```

### 2. 获取奖池详情
```
GET /app-api/open-api/v1/earning-pools/{id}
```

### 3. 提交任务
```
POST /app-api/open-api/v1/earning-pool-tasks/submit
Content-Type: application/json

{
  "earningPoolId": 123,
  "taskLink": ["https://x.com/xxx/status/123"],
  "languageType": "zh_CN"
}
```

### 4. 查询我的任务列表（分页）
```
GET /app-api/open-api/v1/earning-pool-tasks?pageNo=1&pageSize=10
```
Query:
- `pageNo` (required): 页码，从1开始
- `pageSize` (required): 每页条数，最大100
- `earningPoolId` (optional): 奖池ID
- `taskStatus` (optional): 任务状态

### 5. 查询任务状态
```
GET /app-api/open-api/v1/earning-pool-tasks/{id}
```

Response:
```json
{
  "code": 200,
  "data": {
    "id": 456,
    "earningPoolId": 123,
    "userId": 789,
    "kolXHandle": "@handle",
    "sponsor": "Sponsor Name",
    "taskStatus": "SUBMITTED",
    "taskLinks": ["https://x.com/xxx/status/123"],
    "walletAddress": "0x...",
    "txn": "0x...",
    "auditStatus": 0
  }
}
```

## 状态说明

### auditStatus (审核状态)
- `0` - 未审核
- `1` - 审核通过
- `2` - 审核拒绝

### status (奖池状态)
- `Ongoing` - 进行中
- `Completed` - 已结束
