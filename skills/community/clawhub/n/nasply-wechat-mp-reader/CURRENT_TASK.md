# WeChat MP Reader — Current Task Handoff

Last updated: 2026-04-02

## What this is
A reusable skill under `skills/wechat-mp-reader/` for:
- extracting full WeChat Official Account articles
- identifying the account behind an article
- listing an account's articles
- managing WeChat MP backend session state

## Current status
Core path is working:
1. QR login can obtain a fresh MP backend session.
2. `search <account name>` works with a valid session.
3. `article <url>` works.
4. `article <url> --with-account-articles` works.
5. Non-canonical WeChat article pages now use local Playwright WebKit fallback with no `we-mp-rss` dependency in the main script.
6. Local cache now stores `biz/name -> fakeid/avatar/signature` in `scripts/cache/account_cache.json`.
7. Publish times now expose both display-friendly and raw values in output (`publish_time` + `publish_time_raw`).
8. Markdown cleanup has been upgraded to preserve more structure, including emphasis and blockquote semantics.

## Key implementation facts
- Main script: `skills/wechat-mp-reader/scripts/wechat_mp_reader.py`
- Session helpers:
  - `skills/wechat-mp-reader/scripts/wechat_mp_reader/auth.py`
  - `skills/wechat-mp-reader/scripts/wechat_mp_reader/session_store.py`
  - `skills/wechat-mp-reader/scripts/wechat_mp_reader/qr_login.py`
- Account cache:
  - `skills/wechat-mp-reader/scripts/wechat_mp_reader/account_cache.py`
  - `skills/wechat-mp-reader/scripts/cache/account_cache.json`
- Current browser fallback uses local Playwright WebKit only; the main script no longer depends on `we-mp-rss`.

## Proven workflow
Best path:
- article URL
- parse `biz/mid/idx/sn` if present
- fetch page
- if page is non-canonical, use browser fallback
- extract `mp_name/biz/author/title/publish_time/content`
- recover `fakeid` from cache or `searchbiz`
- list account articles through `appmsgpublish`

## Known remaining improvements
1. Expand cache usage and invalidation strategy if needed.
2. Consider exposing additional stable downstream fields if consumers need them (for example source mode / fetched via).
3. Continue improving markdown/body cleanup if richer article layouts still produce noisy output.
4. Continue polishing the skill-managed QR-login/session acquisition path in docs and ergonomics; live end-to-end validation now works directly through the main script without helper bridge scripts.

## Recent commits
- `7d09ed8` — Use local WebKit fallback for wechat mp reader
- `cf75020` — Remove container fallback from wechat mp reader
- `5e2d5d4` — Document local mode and add raw publish times
- `c48ea07` — Improve wechat mp reader markdown cleanup

## Resume checklist for a new session
1. Read `skills/wechat-mp-reader/CURRENT_TASK.md`
2. Read `skills/wechat-mp-reader/SKILL.md`
3. Read `skills/wechat-mp-reader/references/design.md`
4. Read `memory/2026-04-01.md`
5. Read `memory/2026-04-02.md`
6. If testing live, prefer the skill-managed session path: `session check` or `session login-start` / `session login-status`, then run `article <url> --with-account-articles` directly via the main script.
