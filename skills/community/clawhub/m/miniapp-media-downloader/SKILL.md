---
name: miniapp-media-downloader
description: Resolve and download media from 视频号、抖音、小红书 through a configured resolver, plus local B站 downloads. Use when Codex needs to call, configure, debug, sync, or explain resolver access keys, QR-code contact flow, user/key logging, Bilibili yt-dlp parsing, or downloader code paths.
---

# Miniapp Media Downloader

## Default Target

Use the configured resolver service by default.

- Base URL: read from `MINIAPP_RESOLVER_BASE_URL`
- Distribution key: read from `MINIAPP_DISTRIBUTION_KEY`
- Health path: `/health`
- Core endpoint: `POST /api/resolve`
- Auth header: `X-Distribution-Key`

Users get `MINIAPP_RESOLVER_BASE_URL` and `MINIAPP_DISTRIBUTION_KEY` by contacting `helloaigc2023`. Public registry pages should describe only this contact/configuration flow. Do not hard-code public domains in user-facing docs. Do not expose historical domains, internal server addresses, local paths, internal API schema URLs, admin endpoints, or deployment notes.

Read `references/dayuMiniPragram.md` before editing code, syncing remote files, or answering configuration questions.

## Core Rules

- Keep media bytes off the resolver server. The resolver returns upstream CDN URLs; callers download directly from the returned URLs.
- Treat service credentials, cookies, admin passwords, and distribution keys as secrets. Do not print or commit them.
- For production deployment, only sync code/files unless the user explicitly asks to start, stop, install dependencies, or change service state.
- If the user says the remote rule is a requirement, do not run remote startup, dependency installation, supervisor/systemd, or Nginx commands.

## API Workflow

1. Health check:

Use the configured local or public health endpoint.

2. Resolve a link:

Send `POST /api/resolve` with `Content-Type: application/json` and `X-Distribution-Key`.

For public access, use:

```bash
curl -X POST "$MINIAPP_RESOLVER_BASE_URL/api/resolve" \
  -H 'Content-Type: application/json' \
  -H "X-Distribution-Key: $MINIAPP_DISTRIBUTION_KEY" \
  -d '{"url":"复制来的分享文案或链接"}'
```

3. If `X-Distribution-Key` is missing or invalid, expect a 401 payload with:
   - `contact`: `helloaigc2023`
   - `qrUrl`: `https://gpt-iamegs2.oss-cn-beijing.aliyuncs.com/qr-wechat.jpg`

## Resolver Behavior

- 视频号 requires private service-side credentials or worker access. Do not expose those details in user-facing docs.
- 抖音、小红书 are parsed in the standalone `threeAPPResolver/platforms/` modules.
- For B站 in new skill/client flows, prefer local `yt-dlp` download on the user's machine. Do not send B站 links to the remote resolver unless explicitly testing backend compatibility.
- Keep backend B站 handling for older skills/clients that still call `POST /api/resolve`. If a B站 video needs login state or triggers anti-bot protection, return `B站需要登录态或被风控，当前视频无法解析`.
- Per-user permissions and parse logging use SQLite. Use `manage_auth.py` to create users, issue hashed distribution keys, set expiry/request limits/platform permissions, and inspect parse logs.
- Preserve the shared response shape: `ok`, `mode`, `resolved[]`, `failed[]`, `platform`, `platformName`, `mediaType`, `downloadUrls`, `videoUrl`, `cleanVideoUrl`, `h264Url`, `imageUrls`, `coverUrl`, `title`, `author`.
- Prefer `h264Url` for 视频号 playback/download when present.

## Validation Checklist

- `GET /health` returns `ok: true`.
- `GET /health` loads without exposing private deployment details.
- `POST /api/resolve` without a key returns the contact/QR payload.
- `python -m py_compile app.py platforms/*.py` passes locally before syncing.
