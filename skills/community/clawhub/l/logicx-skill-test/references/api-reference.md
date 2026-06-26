## API Surface

LogicX exposes a frontend proxy. Use:

- Health: `/api/health`
- Business APIs: `/api/proxy/*`

Do not call backend `/v1/*` endpoints directly from this skill.

## Auth Rules

The official skill uses `openclaw-public` as the default agent key. LogicX backend accepts it for the public OpenClaw integration.

### Health

```http
GET /api/health
```

No auth required. Returns `{"status":"ok","timestamp":"..."}`.

### Agent bind start

```http
POST /api/proxy/agent/link/start
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
Content-Type: application/json

{"install_id":"openclaw-main"}
```

Response:

```json
{
  "link_code": "lc_xxx",
  "login_url": "http://43.139.104.95:8070/agent/link?code=lc_xxx"
}
```

### Agent bind status

```http
POST /api/proxy/agent/link/status
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
Content-Type: application/json

{"link_code":"lc_xxx","install_id":"openclaw-main"}
```

Responses:

```json
{"status":"pending"}
{"status":"expired"}
{"status":"confirmed","user_token":"at_xxx"}
```

Do not background-poll. Ask the user to finish browser authorization and reply when ready, then check status once. If `confirmed`, persist the returned `user_token`. Link codes expire after 10 minutes. Use the same `install_id` for `link/start` and `link/status`.

### Agent bind confirm

`POST /api/proxy/agent/link/confirm` is the **browser-side** step — the user clicks "确认授权绑定" in the browser after opening the login URL. Do not call this from the agent.

### Agent password login

```http
POST /api/proxy/agent/auth/login
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
Content-Type: application/json

{"email":"user@example.com","password":"secret","install_id":"openclaw-main"}
```

Response:

```json
{"ok":true,"user_token":"at_xxx"}
```

Rate limited: 5 attempts per 15 minutes per IP + email. Returns `429` if exceeded.

### User-scoped calls

All endpoints below require both headers:

```http
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
X-LogicX-User-Token: <LOGICX_USER_TOKEN>
```

## Confirmed Calls

### Current user

```http
GET /api/proxy/user/
```

Response:

```json
{
  "id": "user_xxx",
  "email": "user@example.com",
  "createdAt": "2026-01-01T00:00:00.000Z",
  "role": "user",
  "plan": "free",
  "proExpiresAt": null,
  "maxExpiresAt": null
}
```

`plan` values: `"free"` | `"pro"` | `"max"`. `proExpiresAt` and `maxExpiresAt` are ISO timestamps when the respective plan expires, or `null`.

### Orders

```http
GET /api/proxy/payment/orders
```

Response: `{"orders": [<OrderInfo>, ...]}`

```http
GET /api/proxy/payment/orders/:orderNo
```

Response: `{"order": <OrderInfo>}`

Order shape:

```json
{
  "id": "ord_xxx",
  "orderNo": "202603160001",
  "plan": "pro_monthly",
  "amount": 2900,
  "gateway": "mock",
  "status": "pending",
  "expiresAt": "2026-03-16T12:00:00.000Z",
  "confirmedAt": null,
  "cancelledAt": null,
  "createdAt": "2026-03-16T11:58:00.000Z"
}
```

`status` values: `"pending"` | `"confirmed"` | `"cancelled"` | `"expired"`

`amount` is in cents (分). Divide by 100 for yuan (元).

### Create order

```http
POST /api/proxy/payment/create
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
X-LogicX-User-Token: <LOGICX_USER_TOKEN>
Content-Type: application/json
```

Request: `{"plan":"pro_monthly","gateway":"mock"}`

Available plan IDs:

| ID              | Name      | Price (分) | Days |
|-----------------|-----------|-----------|------|
| pro_monthly     | Pro 月付  | 2900      | 30   |
| pro_quarterly   | Pro 季付  | 7800      | 90   |
| pro_yearly      | Pro 年付  | 26100     | 365  |
| max_monthly     | Max 月付  | 5900      | 30   |
| max_quarterly   | Max 季付  | 15900     | 90   |
| max_yearly      | Max 年付  | 53100     | 365  |

Available gateways: `mock` (test only), `alipay`, `wechat`, `paypal`.

Response: `<OrderInfo>`

### Cancel order

```http
POST /api/proxy/payment/cancel
Content-Type: application/json

{"orderNo":"ORDER_NO"}
```

Response: `{"ok":true}`

### Password change

```http
POST /api/proxy/auth/change-password
Content-Type: application/json

{"currentPassword":"old-password","newPassword":"new-password-min-8-chars"}
```

### Agent unlink

```http
POST /api/proxy/agent/unlink
Content-Type: application/json

{"install_id":"openclaw-main"}
```

## Notes

- `400` on `agent/link/confirm` usually means the `link_code` expired or was already consumed.
- `429` on `agent/auth/login` means rate limit exceeded; wait 15 minutes.
- Auth failures usually mean a bad service key or missing/invalid user token.
- After either login path succeeds, verify the token with `GET /api/proxy/user/`.
