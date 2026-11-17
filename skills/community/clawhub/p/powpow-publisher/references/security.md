# Security Architecture & Platform API

> For maintenance/troubleshooting only. SKILL.md runtime does not require reading this.

## Why this skill is safe to distribute

This skill holds **no platform secrets**:

| Item | Guarantee |
|---|---|
| Platform secrets | None bundled — every operation goes through the platform's own HTTP API |
| Identity | JWT from a real login; you can only post as yourself |
| User password | Never stored; used only in memory, once, to obtain a short-lived (~7-day) token |
| Rate limits / moderation | Enforced server-side (10 posts/hr/user, content moderation) |
| Unsplash key | User-supplied, optional (images are optional) |

The skill never reads, writes, or ships any credential files. The only state it
writes is the user's own session token, stored in the user's state directory
(see below), never inside the skill bundle.

`config.json` contains ONLY `{ "platformUrl", "unsplashAccessKey"(optional),
"sessionMaxAgeDays", "skillVersion" }`. Never add Supabase keys, service roles,
or admin tokens to this skill.

### Files that must never leave the user's machine
- `<POWPOW_STATE_DIR>/session.json` (default `~/.powpow/session.json`) — the
  logged-in user's JWT (auto-expires ~7 days). Written to the user's state
  directory, never into the (possibly read-only) skill bundle.

## Platform API endpoints used

- `POST /api/auth/login` — `{step:1, username, password}` → JWT (cookie `powpow_token`)
- `GET  /api/digital-humans?scope=all&search=...` — list/search digital humans (login required)
- `GET  /api/amap/place/text?keywords=...` — place-name search (login required;
  returns GCJ-02, converted to WGS-84 client-side by geocode.js). The endpoint
  path is platform-internal and must not be surfaced to the user; in internal
  discussion refer to it neutrally as the place-lookup service (never name it
  to the user).
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
