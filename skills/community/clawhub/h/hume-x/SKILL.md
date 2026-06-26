---
name: hume-x
description: X/Twitter CLI and SDK for reading, searching, posting, and engagement via cookie auth.
metadata: {"emoji":"🐦","install":"npm install -g @humebio/hume-x","requires":{"bins":["hume-x"]}}
---

# hume-x

Fast X/Twitter CLI using GraphQL + cookie auth. Full API coverage for tweets, timelines, search, engagement, social, lists, trending, notifications, bookmarks, likes, and scheduled tweets.

## Authentication

Uses cookie-based auth. Credentials are resolved in order:

1. CLI flags: `--auth-token` and `--ct0`
2. Environment variables: `X_AUTH_TOKEN` + `X_CT0` (or `AUTH_TOKEN` + `CT0`)
3. Config file: `~/.config/hume-x/config.json`
4. Browser cookies: Firefox (preferred) or Chrome

Run `hume-x check` to verify credentials. Use `hume-x whoami` to see the logged-in user.

## Posting

```bash
hume-x tweet "hello world"
hume-x tweet "check this out" --media image.png --alt "description"
hume-x reply <id-or-url> "nice thread!"
hume-x quote <id-or-url> "interesting take"
hume-x delete <tweet-id>
```

Supports media upload: images (jpg/png/webp), GIFs, videos with chunked upload.

## Reading

```bash
hume-x read <id-or-url>
hume-x thread <id-or-url>
hume-x replies <id-or-url> -n 50
```

Accepts tweet ID or full URL (e.g. `https://x.com/user/status/123`).

## Timeline

```bash
hume-x home -n 30
hume-x home --following
hume-x home --cursor "abc123" --pages 3
hume-x user-tweets <username> -n 10
```

Supports cursor-based pagination with `--cursor` and `--pages` flags.

## Search

```bash
hume-x search "query" -n 20
hume-x search "from:username" -n 10
hume-x mentions
hume-x mentions --user <username>
```

## Engagement

```bash
hume-x like <tweet-id>
hume-x retweet <tweet-id>
hume-x bookmark <tweet-id>
hume-x pin <tweet-id>
```

## Collections

```bash
hume-x bookmarks
hume-x likes
```

## Social

```bash
hume-x follow <username>
hume-x unfollow <username>
hume-x mute <username>
hume-x block <username>
hume-x following <username>
hume-x followers <username>
```

## Lists

```bash
hume-x lists
hume-x lists --member-of
hume-x list-timeline <list-id>
```

## Trending

```bash
hume-x trending
hume-x trending --tab news
hume-x trending --tab sports
hume-x trending --tab entertainment
```

Tabs: `for-you` (default), `trending`, `news`, `sports`, `entertainment`.

## Notifications

```bash
hume-x notifications
```

## Scheduled Tweets

```bash
hume-x schedule "future tweet" --at "2025-06-01T12:00:00Z"
```

## User Info

```bash
hume-x whoami
hume-x about <username>
```

## Utility

```bash
hume-x check              # verify auth credentials
hume-x query-ids           # show cached GraphQL query IDs
hume-x refresh-ids         # force refresh query IDs from x.com
```

## Output Flags

- `--json` — parsed JSON output (pipe to jq for filtering)
- `--json-full` — raw API response JSON
- `--plain` — plain text without colors
- `--no-color` — disable ANSI colors

```bash
hume-x home --json | jq '.[0].text'
hume-x search "topic" --json -n 5
```

## Global Flags

- `--auth-token <token>` — X auth token
- `--ct0 <token>` — X ct0 CSRF token
- `--timeout <ms>` — request timeout
- `--proxy <url>` — HTTPS/SOCKS5 proxy
- `-n <count>` — number of results (default varies by command)

## Important

- Posting is rate-limited by X. If blocked, wait before retrying.
- Query IDs are auto-scraped from x.com with 24h cache. Use `hume-x refresh-ids` if you get 404 errors.
- Uses curl-impersonate for reliable HTTP requests to X's GraphQL API.
