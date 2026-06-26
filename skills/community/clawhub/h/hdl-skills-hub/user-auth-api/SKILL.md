---
id: user-auth-api
slug: user-auth-api
name: 用户身份认证 API
description: 供 OpenClaw 调用，用于通过用户名和密码获取 HDL 系统的身份令牌 (AccessToken)。该 Token 是调用其他业务接口（如产品查询）的前提。
version: 1.1.0
tools: [login, refreshToken]
tags: [auth, login, token, documentation, refresh]
permissions: [authenticated]
priority: 100
---

# 1. 强制认证与安全约束
- **无 Token 不调用 (STRICT)**: 严禁在没有有效 `accessToken` 的情况下调用任何业务接口。
- **凭据源 (STRICT)**: 所有系统凭据（AppKey, ApSecret）必须且只能从根目录下的 `.env` 文件（路径：`../.env`）读取。**严禁向用户询问这些信息**。
- **自动获取/刷新机制**:
  1. **首次调用**: 若当前无 Token，AI 必须主动执行 [hdl-skills-hub](../SKILL.md) 定义的分步引导获取。
  2. **令牌刷新**: 若业务接口返回 401（Unauthorized），AI 必须静默尝试 `refreshToken`。
  3. **认证失败**: 若登录或刷新均失败，AI 必须告知用户认证已失效，并重新启动分步引导。
- **Header 规范**: 所有业务接口必须在 Header 中携带 `Authorization: Bearer {accessToken}`。

# 2. 接口详细说明

## 2.1 用户登录 (login)
- **接口地址**: `https://gateway.hdlcontrol.com/basis-footstone/user/oauth/login`
- **请求方式**: `POST`
- **内容类型**: `application/json;charset=UTF-8`

### 2.1.1 请求参数 (JSON Body)
| 字段名 | 类型 | 必选 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `loginName` | String | **是** | 用户名或手机号。 | `"19210818109"` |
| `loginPwd` | String | **是** | 用户登录密码。 | `"123456"` |
| `grantType` | String | **是** | 授权类型，固定为 `"password"`。 | `"password"` |
| `appKey` | String | **是** | (BaseDTO) 应用标识，取自 `${HDL_APP_KEY}`。 | `${HDL_APP_KEY}` |
| `timestamp` | Long | **是** | (BaseDTO) 13位毫秒级时间戳。 | `1774425423000` |
| `sign` | String | **是** | (BaseDTO) 安全签名，详见 [sign-encryption-api](../sign-encryption-api/SKILL.md)。 | `"abc123xyz..."` |

### 2.1.2 响应参数 (Result<LoginVO>)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `code` | Integer | 状态码（0 表示成功）。 |
| `isSuccess` | Boolean | 是否成功。 |
| `msg` | String | 错误提示信息。 |
| `data.accessToken` | String | 访问令牌（用于后续业务请求）。 |
| `data.refreshToken` | String | 刷新令牌。 |
| `data.expiresIn` | Long | Token 有效期（秒）。 |

### 2.1.3 登录成功示例 (Response)
```json
{
  "code": 0,
  "isSuccess": true,
  "msg": "登录成功",
  "data": {
    "accessToken": "ey...",
    "refreshToken": "rf...",
    "expiresIn": 7200
  }
}
```

## 2.2 刷新 Token (refreshToken)
- **接口地址**: `https://gateway.hdlcontrol.com/basis-footstone/mgmt/user/idmOauth/refreshToken`
- **请求方式**: `POST`

### 2.2.1 请求参数
| 字段名 | 类型 | 必选 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `refreshToken` | String | **是** | 登录返回的刷新令牌。 | `"rf_abc123"` |
| `appKey` | String | **是** | 取自 `${HDL_APP_KEY}`。 | `${HDL_APP_KEY}` |
| `timestamp` | Long | **是** | 13位毫秒级时间戳。 | `1774425423000` |
| `sign` | String | **是** | 安全签名。 | `"xyz..."` |

---

# 3. 核心交互场景设计

### 场景 A: 任务恢复链路 (Conversational)
1. **用户**: “查一下方悦面板。”
2. **AI**: (检测未登录) -> “🔑 **HDL 认证** - 请提供您的 **用户名**。”
3. **用户**: “19210818109”
4. **AI**: “好的。现在请提供 **登录密码**。”
5. **用户**: “******”
6. **AI**: (自动结合 .env 中的 AppKey/Secret 登录成功) -> “登录成功！正在为您查询方悦面板... ✅”

### 场景 B: 认证失败
1. **AI**: “❌ **认证失败**：用户名或密码不正确。让我们重新开始。请输入您的 **用户名**：”。

---

# 4. 调用策略
1. **静默刷新**: 当业务请求返回 401 时，AI 必须优先调用 `refreshToken`。
2. **凭据持久化**: 登录成功后，AI 应在当前会话内存中持久化 Token，并遵循隐私规则不再展示。
3. **安全隔离**: 严禁在日志或答复中打印 `accessToken`。
