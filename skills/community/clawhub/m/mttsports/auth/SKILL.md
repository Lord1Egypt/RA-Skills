---
name: mttsports-auth
description: "Use when the task is specifically about `mttsports auth`: checking login state, logging in, refreshing tokens, or logging out. Prefer `--output json`, never expose secrets, and verify state before chaining room or session commands."
---

# mttsports auth

When this sub-skill is loaded, the task is already in the `mttsports auth` domain.

## Core Rules

1. If login state is unclear, run `mttsports auth status --output json` first.
2. Use structured commands for login. For email captcha login, send the captcha first and then log in.
3. Never guess tokens and never write raw tokens into extra files.
4. Prefer `--output json` for auth commands so room and session flows can reuse key fields.

## Intent To Command

| Intent | Recommended Command | Notes |
|---|---|---|
| Check whether the user is logged in | `mttsports auth status --output json` | Default entry point |
| Send email login captcha | `mttsports auth send-email-captcha --email ... --output json` | Required before captcha login |
| Explicit email and password login | `mttsports auth login --email ... --password ... --output json` | Common for local debugging |
| Email captcha login | `mttsports auth login --email ... --captcha ... --output json` | Send captcha first, then log in |
| pubID plus password login | `mttsports auth login --pub-id ... --password ... --output json` | For accounts with known pubID |
| Refresh token | `mttsports auth refresh --output json` | Requires an existing login state |
| Clear local login state | `mttsports auth logout --output json` | Removes local credentials |

## Common Examples

```bash
mttsports auth status --output json
mttsports auth send-email-captcha --email you@example.com --output json
mttsports auth login --email you@example.com --password '***' --output json
mttsports auth login --email you@example.com --captcha '123456' --output json
mttsports auth login --pub-id PUB123 --password '***' --output json
mttsports auth refresh --output json
mttsports auth logout --output json
```

## Command Schema

### `mttsports auth status`

```json
{
  "logged_in": true,
  "endpoint": "https://...",
  "email": "user@example.com",
  "uid": "12345",
  "pub_id": "pub_xxx",
  "token_expired_at": "2026-04-02T12:34:56Z",
  "token_expired_time": 1712061296,
  "token_expired": false
}
```

### `mttsports auth login`

```json
{
  "logged_in": true,
  "login_type": "LOGIN_TYPE_PUBID",
  "uid": "12345",
  "pub_id": "pub_xxx",
  "token_expired_at": "2026-04-02T12:34:56Z",
  "token_expired_time": 1712061296
}
```

### `mttsports auth send-email-captcha`

```json
{
  "sent": true,
  "email": "user@example.com",
  "expired_at": 1712061296,
  "expired_time": "2026-04-02T12:34:56Z"
}
```

### `mttsports auth refresh`

```json
{
  "refreshed": true,
  "token_expired_at": "2026-04-02T12:34:56Z",
  "token_expired_time": 1712061296
}
```

### `mttsports auth logout`

```json
{
  "logged_out": true
}
```

## Notes

1. Captcha login requires `auth send-email-captcha` first, then `auth login --captcha ...`. Do not skip the send step.
2. `--email` and `--pub-id` cannot be passed together. `--captcha` is only for email login.
3. Before continuing into room or session flows, confirm `uid` and `pub_id` from `auth status` or `auth login`.
4. If the next goal is a full game flow, return to the "Common Workflows" section in [`../SKILL.md`](../SKILL.md).
