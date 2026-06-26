---
name: moss-platform-quick-auth
description: B-only Quick Auth for Moss platform. Use only api-login / api-register (no email code flow).
---

# Moss Platform Quick Auth (B-only)

仅使用 **方案 B（无验证码）**：
- `POST /studio-api/v1/auth/quick/api-login`
- `POST /studio-api/v1/auth/quick/api-register`

禁止使用：
- `send-code`
- `login`
- `register`

## Base URL

`https://<host>/studio-api/v1/auth/quick/*`

## Required Inputs

- `host`（例如 `studio.mosi.cn`）
- `email`

## Flow (B-only)

### 1) 先尝试 api-login

```bash
curl -sS -X POST "https://<host>/studio-api/v1/auth/quick/api-login" \
  -H 'Content-Type: application/json' \
  --data '{"email":"<email>"}'
```

### 2) 若返回 USER_NOT_EXIST，则 api-register

```bash
curl -sS -X POST "https://<host>/studio-api/v1/auth/quick/api-register" \
  -H 'Content-Type: application/json' \
  --data '{"email":"<email>"}'
```

## Success Fields

- `user_id`
- `access_token`
- `refresh_token`
- `expires_in`
- `api_key`
- `temp_password`（仅注册返回，一次性）

## Output Contract

返回给用户：
- 使用了哪个 endpoint
- 结果状态（login success / register success / error code）
- `user_id`
- `expires_in`
- 凭据（按需脱敏展示）

## Error Handling

- `USER_NOT_EXIST` → api-login 切换到 api-register
- `EMAIL_EXISTS` → api-register 切回 api-login
- `ACCOUNT_BANNED` → 终止并提示

## Security

- 默认脱敏展示凭据，除非用户明确要原文。
- 明确提示 `temp_password` 仅返回一次，必须立即保存。
