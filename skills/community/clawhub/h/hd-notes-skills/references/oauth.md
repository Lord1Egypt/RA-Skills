# OAuth 授权配置（话袋笔记）

## 概述

使用 **OAuth 2.0 Device Authorization Grant** 让用户在浏览器中完成授权，换取 **API Key**，再写入本地/运行环境配置。适用于「配置话袋笔记」「连接话袋」等场景；首次调用开放接口前若缺少凭证，也应引导用户走本流程。

话袋开放接口的调用侧模型（详见 [配置（必须先完成）](config.md)、[话袋笔记 API 详细参考](api-details.md)）为：

- **`USER-UUID` 请求头**：与话袋用户 **`unique_id`** 一致，用于**唯一标识用户**与数据归属；配置为环境变量 **`HUADAI_USER_UUID`**。在多人聊天场景中，用于划定「仅该用户」可访问的笔记边界，保证**私密性**。
- **`Authorization` 请求头**：值为 **API Key**，用于**身份校验与鉴权登录**（证明调用方为已授权用户），配置为 **`HUADAI_API_KEY`**。

> 说明：OAuth 步骤里的「授权轮询码」仅用于向 `/oauth/token` **兑换**上述凭证；它不是“设备号/设备绑定标识”。话袋笔记 Skill **不做设备绑定**、也不使用 `Device-Id` 之类的请求头。

---

## 自动触发条件

每次调用 API 前，先检查是否已具备调用所需配置（至少 **`HUADAI_API_KEY`**，以及受保护接口要求的 **`HUADAI_USER_UUID`**，见 [配置（必须先完成）](config.md)）。

若缺失，**应发起 OAuth 授权流程**（无需用户先说「配置」），说明需要先完成授权再使用；授权完成并写入配置后，再继续执行用户原本请求。

---

## 手动配置（可选）

1. 前往 [话袋开放平台](https://ihuadai.cn/openapi) 创建应用
2. 获取 **`api_key`** 与 **`unique_id`**（用户唯一标识）。
3. 在 `~/.openclaw/openclaw.json`（或当前环境的 Skill 配置）中注入环境变量，**不要在聊天中回显密钥**：

```json
{
  "skills": {
    "entries": {
      "huadai-notes-skill": {
        "env": {
          "HUADAI_BASE_URL": "https://openapi.ihuadai.cn/open/api/v1",
          "HUADAI_API_KEY": "hk_live_你的key",
          "HUADAI_USER_UUID": "用户标识"
        }
      }
    }
  }
}
```

---

## Device Flow 完整流程

以下路径均相对于 **`HUADAI_BASE_URL`**（已包含 `/open/api/v1` 前缀），与 [话袋笔记 API 详细参考](api-details.md) 一致。

### 步骤 1：申请授权码

```
POST https://openapi.ihuadai.cn/open/api/v1/oauth/device/code
Content-Type: application/json
```

请求体（与 `scripts/oauth_poll.py` 一致）：

- **默认（推荐）**：使用预注册应用，请求体为 **空 JSON 对象**：

```json
{}
```

- **覆盖 `client_id`（企业自建等）**：在环境变量中设置 `HUADAI_CLIENT_ID` 后，请求体为：

```json
{
  "client_id": "<你的 HUADAI_CLIENT_ID>"
}
```

> 说明：默认情况下话袋服务端为 OpenClaw 预注册固定 `client_id`，**无需**在请求里传 `client_id`，也**无需**配置 `HUADAI_CLIENT_ID`。仅在需要覆盖时配置环境变量并随请求发送。


**统一结构示例**：

```json
{
  "code": 200,
  "message": "请求成功",
  "data": {
    "code": "abc123...",
    "verification_uri": "https://openapi.ihuadai.cn/api/v1/oauth/authorize?code=abc123...",
    "user_code": "ABCD-1234",
    "expires_in": 600,
    "interval": 5
  }
}
```

| 字段 | 说明 |
|------|------|
| `code`（在 `data` 内） | 授权轮询码，步骤 3 轮询 `/oauth/token` 时使用 |
| `verification_uri` | 授权链接，**发给用户点击** |
| `user_code` | 确认码，**必须展示给用户核对** |
| `expires_in` | 授权码有效期（秒），常见 600 |
| `interval` | 建议轮询间隔（秒），常见 5 |

### 步骤 2：展示授权链接

将 `verification_uri` 与 `user_code` 发给用户，例如：

> 请点击链接完成授权：{verification_uri}  
> **请核对确认码**：`{user_code}`（须与授权页一致后再授权）

**安全**：`user_code` 用于降低钓鱼风险；若页面所示与 Agent 提供的不一致，应拒绝授权。

**发送后立即启动后台轮询**（步骤 3）。

### 步骤 3：轮询等待授权

在用户打开链接操作的同时，**后台轮询** token 端点（不必等用户回复）。

```
POST {HUADAI_BASE_URL}/oauth/token
Content-Type: application/json
```

其中 `{HUADAI_BASE_URL}` 须与步骤 1 一致（例如 `https://openapi.ihuadai.cn/open/api/v1`），完整示例：

```
POST https://openapi.ihuadai.cn/open/api/v1/oauth/token
Content-Type: application/json
```

请求体（`grant_type` 与 `code` 必填；`client_id` 仅在与步骤 1 一致地使用了 `HUADAI_CLIENT_ID` 时需要带上）：

```json
{
  "grant_type": "device_code",
  "code": "{data.code}"
}
```

若已设置 `HUADAI_CLIENT_ID`，则请求体需额外包含 `"client_id": "<与步骤 1 相同的值>"`。

**轮询策略**：

- **间隔**：每 5 秒一次（或与步骤 1 返回的 `interval` 一致）
- **超时**：最多约 10 分钟（与授权码有效期对齐）
- **并行**：轮询在后台执行，不阻塞其他交互

**推荐使用本 Skill 自带脚本**（仓库内路径：`scripts/oauth_poll.py`）：

```bash
export HUADAI_BASE_URL="https://openapi.ihuadai.cn/open/api/v1"
# 可选：export HUADAI_CLIENT_ID="你的 client_id"
result=$(python scripts/oauth_poll.py "{data.code}")
api_key=$(echo "$result" | jq -r '.api_key')
user_uuid=$(echo "$result" | jq -r '.unique_id // .user_uuid // empty')
```

脚本成功时在 **stdout** 打印 `data` 的 JSON；错误信息在 **stderr**，退出码见脚本头部注释（如用户拒绝、过期、超时等）。

**OpenClaw 场景示例**（按需调整路径与 session）：

```yaml
# 后台执行轮询
exec: python scripts/oauth_poll.py "{code}"
  background: true
  env:
    HUADAI_BASE_URL: "https://openapi.ihuadai.cn/open/api/v1"
    # 可选：HUADAI_CLIENT_ID: "你的 client_id"

process: poll
  sessionId: {sessionId}
  timeout: 600000
```

**轮询过程状态**（`data.msg` 或等价字段，以服务端为准）：

| 情形 | 说明 | 处理 |
|------|------|------|
| `authorization_pending` | 用户尚未完成操作 | 继续轮询 |
| `rejected` | 用户拒绝授权 | 停止轮询并提示 |
| `expired_token` | 授权码过期 | 停止轮询，从步骤 1 重试 |
| `already_consumed` | 授权码已使用 | 停止轮询；可能已在其他终端完成 |
| `data` 中含 `api_key` | 授权成功 | 进入步骤 4 |

**授权成功**时，`data` 中至少包含 **`api_key`**；若返回 **`unique_id`** 或 **`user_uuid`**，应与请求头 **`USER-UUID`** 一致，并写入 **`HUADAI_USER_UUID`**。

成功响应示例（统一结构）：

```json
{
  "code": 200,
  "message": "请求成功",
  "data": {
    "client_id": "cli_xxx",
    "api_key": "hk_live_xxx",
    "unique_id": "uu_xxx",
    "key_id": "可选",
    "expires_at": 1742000000
  }
}
```

| 字段 | 说明 |
|------|------|
| `api_key` | 写入 **`HUADAI_API_KEY`**，用于 **`Authorization`** 鉴权登录 |
| `unique_id` / `user_uuid`（若返回） | 写入 **`HUADAI_USER_UUID`**，对应 **`USER-UUID`**，与话袋用户唯一标识一致 |
| `client_id`（若返回） | 可选写入 **`HUADAI_CLIENT_ID`**，便于下次自建应用覆盖时与本次授权一致；使用预注册应用时通常不必保存 |
| `expires_at` | 若存在，为 API Key 等相关过期时间（Unix 秒），可在提示文案中使用 |

### 步骤 4：写入配置并校验

将 **`HUADAI_API_KEY`**、**`HUADAI_USER_UUID`**（与 **`unique_id`** 一致）、**`HUADAI_BASE_URL`** 写入运行环境或 `openclaw.json`（示例见上文）。**`HUADAI_CLIENT_ID`** 仅在需要固定为某自建应用、或希望与响应中的 `client_id` 对齐时再写入。

告知用户时可说明：

- 已可使用话袋笔记 Skill 的保存、搜索等能力；
- **不要在对话中粘贴或展示完整 Key 与 USER-UUID**；
- 多人场景下仅绑定配置中的 **`HUADAI_USER_UUID`** 对应用户，避免他人访问同一笔记数据。

---

## 相关文档

- [配置（必须先完成）](config.md)（请求头与环境变量）
- [话袋笔记 API 详细参考](api-details.md)（HTTP 路径与统一响应）
- 轮询脚本：仓库内 [`scripts/oauth_poll.py`](../scripts/oauth_poll.py)
