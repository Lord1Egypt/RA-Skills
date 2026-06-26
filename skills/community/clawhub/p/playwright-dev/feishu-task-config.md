## 飞书任务 API 配置（2026-03-06 23:22 更新）

### ✅ 成功配置

**API 版本:** v2  
**Endpoint:** `POST https://open.feishu.cn/open-apis/task/v2/tasks`  
**Token 类型:** tenant_access_token（应用身份）

### 🔑 Token 获取

```powershell
$body = @{
    app_id = "cli_a91d70683c789bc7"
    app_secret = "t0am3JU79N9TSEPgrk7GKbVLHmCdRGUe"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" -Method Post -Body $body -Headers @{ "Content-Type" = "application/json" }
$token = $response.tenant_access_token
```

### 📋 创建任务

```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    summary = "任务内容"
    done = $false
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/task/v2/tasks" -Method Post -Body $body -Headers $headers
$task_id = $response.data.task.task_id
$task_url = $response.data.task.url
```

### ⚠️ v1 vs v2 区别

| 参数 | v1 API | v2 API |
|------|--------|--------|
| 内容字段 | `content` | `summary` |
| origin | 必填（需要应用内部 ID） | 自动填充 |
| Token | user_access_token | tenant_access_token |
| 推荐度 | ❌ 不推荐 | ✅ 推荐 |

### 🎯 应用信息

- **App ID:** `cli_a91d70683c789bc7`
- **App Secret:** `t0am3JU79N9TSEPgrk7GKbVLHmCdRGUe`
- **用户 ID:** `ou_e3a0d4a64a9e0932ee919b97f17ec210`

### 📌 注意事项

1. v2 API 不需要 `origin` 参数（自动使用应用信息）
2. 使用应用身份 token（tenant_access_token），不是用户身份 token
3. 内容字段是 `summary`，不是 `content`
4. 任务 URL 从 `response.data.task.url` 获取
