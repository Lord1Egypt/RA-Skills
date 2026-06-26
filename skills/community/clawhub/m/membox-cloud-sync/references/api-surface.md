# Membox API Surface

Base URL:

- `https://membox.cloud/api/v1`

## Authentication and Session

Browser-facing account and provider APIs:

- `POST /auth/email/request`
- `POST /auth/email/verify`
- `GET /auth/provider/{provider}/start`
- `GET /auth/provider/{provider}/callback`
- `POST /auth/logout`
- `POST /auth/token/refresh`
- `GET /account/me`

Device Code flow:

- `POST /device/start`
- `GET /device/poll/{device_code}`
- `GET /device/verify/{user_code}`
- `POST /device/verify/{user_code}/confirm`
- `POST /device/verify/{user_code}/deny`

Device start request:

```json
{
  "device_name": "MacBook Pro",
  "platform": "macos",
  "plugin_version": "0.1.0",
  "sign_public_key_b64": "base64-ed25519-public-key",
  "kex_public_key_b64": "base64-x25519-public-key"
}
```

Device start response:

```json
{
  "device_code": "dvc_123",
  "user_code": "ABCD-EFGH",
  "verification_uri": "https://membox.cloud/device",
  "verification_uri_complete": "https://membox.cloud/device?user_code=ABCD-EFGH&auto=1",
  "expires_in": 900,
  "interval": 2
}
```

Operational rule:

- Prefer `verification_uri_complete` over `verification_uri`.
- When the plugin uses trusted-device grants, include the Ed25519 signing and X25519 key-exchange public keys in `POST /device/start`.
- The browser side may auto-finish authorization if the user already has a valid Membox session.
- On headless or VPS environments, the user still needs to open the full link on a trusted browser and complete login there.

Device poll success:

```json
{
  "access_token": "atk_123",
  "refresh_token": "rtk_123",
  "token_type": "Bearer",
  "expires_in": 3600,
  "device_id": "uuid"
}
```

Poll states to handle:

- `authorization_pending`
- `slow_down`
- `expired_token`
- `access_granted`

## Account and Device Management

- `GET /account/providers`
- `POST /account/providers/link/{provider}`
- `DELETE /account/providers/{provider}`
- `GET /devices`
- `POST /devices/{device_id}/revoke`

Representative account payload:

```json
{
  "user_id": "uuid",
  "display_name": "Alice",
  "primary_email": "alice@example.com",
  "providers": [
    {
      "provider": "github",
      "provider_email": "alice@example.com",
      "linked_at": "2026-03-11T00:00:00Z",
      "is_primary": true
    }
  ]
}
```

## Recovery and Device Grant

Recovery material APIs:

- `GET /recovery/materials`
- `POST /recovery/materials/rotate`
- `POST /recovery/bundle/download`

Recovery material status:

```json
{
  "has_recovery_code": true,
  "has_recovery_bundle": true,
  "updated_at": "2026-03-11T00:00:00Z"
}
```

Device grant APIs for trusted-device recovery:

- `POST /devices/{device_id}/grants`
- `GET /devices/grants/pending`
- `POST /devices/grants/{grant_id}/approve`
- `POST /devices/grants/{grant_id}/reject`
- `GET /devices/grants/{grant_id}`

Use these when the user restores a new machine through an already trusted device.

## Sync

- `GET /sync/status`
- `GET /sync/changes?cursor={cursor}`
- `POST /sync/objects/commit`
- `DELETE /sync/objects/{object_id}`

Sync change shape:

```json
{
  "cursor": 1024,
  "changes": [
    {
      "seq": 1024,
      "object_id": "uuid",
      "version": 3,
      "change_type": "upsert",
      "created_by_device_id": "uuid",
      "created_at": "2026-03-11T00:00:00Z"
    }
  ]
}
```

Commit request shape:

```json
{
  "object_id": "uuid",
  "version": 3,
  "manifest": {
    "version": 1,
    "algorithm": "aes-256-gcm",
    "blob_key": "prod/users/ab/.../blob.bin",
    "ciphertext_size": 1234,
    "content_sha256": "..."
  }
}
```

## Export and Account Deletion

- `POST /account/export`
- `GET /account/export/{export_id}`
- `DELETE /account`

## Error Shape

All 4xx and 5xx responses should be treated as:

```json
{
  "error": {
    "code": "device_code_expired",
    "message": "The device code has expired.",
    "request_id": "uuid",
    "details": {}
  }
}
```

The skill should surface `error.code` clearly and use `request_id` for debugging when available.
