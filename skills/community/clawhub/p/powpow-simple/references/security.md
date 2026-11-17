# Security Architecture & Platform API

> 仅维护/排查时参考。SKILL.md 运行时不需要通读。

> **v1.0.5 起**：本 skill 不再携带任何脚本——所有网络与凭据操作由配套执行层
> **powpow-cli**（`clawhub install powpow-cli`）承担。安全基线由 powpow-cli
> 在代码层强制：密码仅经用户终端 TTY 隐藏输入进入（不进对话、不进 argv）、
> 会话文件 0600/目录 0700、写操作缺省 dry-run（`--confirm` 才执行）、
> `platformUrl` 白名单锁定官方域名。本 skill 只剩对话编排文案。

## Why this skill is safe to distribute

This skill holds **no scripts and no platform secrets**:

| Item | Guarantee |
|---|---|
| Platform secrets | None bundled — every operation goes through the platform's own HTTP API (via powpow-cli) |
| Identity | JWT from a real login; you can only post as yourself |
| User password | Never seen by the agent; the user runs powpow-cli login on their own terminal (hidden TTY input) |
| Write actions | publish / create-digital-human / delete-post are dry-run by default in powpow-cli; `--confirm` required |
| Rate limits / moderation | Enforced server-side (10 posts/hr/user, content moderation) |
| Unsplash key | User-supplied, optional (images are optional) |

### Files that must never leave the user's machine
- `<POWPOW_STATE_DIR>/session.json` (default `~/.powpow/session.json`) — the
  logged-in user's JWT (auto-expires ~7 days), file mode 0600. Written to the
  user's state directory, never into any skill bundle.

## Platform API endpoints used

- `POST /api/auth/login` — `{step:1, username, password}` → JWT (cookie `powpow_token`)
- `GET  /api/digital-humans?scope=all&search=...` — list/search digital humans (login required)
- `GET  /api/amap/place/text?keywords=...` — place-name search (login required;
  returns GCJ-02, converted to WGS-84 client-side by geocode.js). The endpoint
  path is platform-internal and must not be surfaced to the user either — refer
  to it as 「地图数据库」 in any internal discussion (never to the user).
- `POST /api/upload/post-image` — local image upload (multipart `file`; login required)
- `POST /api/posts` — create post (login required; server enforces limits & moderation)
- `GET  /api/posts/{id}` — verify a post
- `DELETE /api/posts/{id}` — delete own post (test cleanup)
- `POST /api/digital-humans` — create a digital human (login required;
  consumes 2 badges, expires after 30 days)
- `POST /api/digital-humans/generate-avatar` — AI avatar from the persona
  (login required; 8~30s; needs a reference image URL by platform design)
- `GET  /api/badges/balance?userId=...` — badge balance pre-check

Note: the JWT is bound to a device fingerprint (User-Agent + Accept-Language). The API client pins these headers at login and reuses them automatically. If you see `DEVICE_MISMATCH` or 401, just re-login.
