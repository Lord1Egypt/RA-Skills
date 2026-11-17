# Reddit (reddit-mcp-buddy)

Reddit browser for reading posts, searching subreddits, and analyzing user activity. Uses the `reddit-mcp-buddy` npm package invoked via MCP stdio.

## Prerequisites

```bash
# No install needed — npx fetches it on first use
# For persistent install:
npm install -g reddit-mcp-buddy
```

## Authentication

| Mode | Rate Limit | Credentials |
|------|------------|-------------|
| Anonymous | 10 req/min | None (default) |
| App-Only | 60 req/min | Client ID + Secret |
| Authenticated | 100 req/min | Client ID + Secret + Username + Password |

To register OAuth credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App"
3. Select **"script"** type (required for 100 rpm tier)
4. Set redirect URI to `http://localhost:8080`
5. Note the Client ID (under "personal use script") and Client Secret

Set env vars: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`

## Actions

### `browse`
Browse posts from any subreddit.

```bash
python3 scripts/reach.py query reddit browse '{"subreddit": "wallstreetbets", "sort": "hot", "time": "day", "limit": 25}'
```

Params:
- `subreddit` (string, default: "all") — Subreddit name without r/ prefix
- `sort` (string, default: "hot") — hot, new, top, rising, controversial
- `time` (string, default: "day") — hour, day, week, month, year, all
- `limit` (int, default: 25) — Max posts to return

### `search`
Search across Reddit or a specific subreddit.

```bash
python3 scripts/reach.py query reddit search '{"query": "AAPL earnings", "subreddit": "wallstreetbets", "sort": "top", "time": "week", "limit": 10}'
```

Params:
- `query` (string, required) — Search terms
- `subreddit` (string, optional) — Filter to specific subreddit
- `sort` (string, default: "relevance") — relevance, hot, top, new, comments
- `time` (string, default: "week") — hour, day, week, month, year, all
- `limit` (int, default: 25)
- `author` (string, optional) — Filter by author
- `flair` (string, optional) — Filter by flair

### `post`
Get a post with full comments.

```bash
python3 scripts/reach.py query reddit post '{"url": "https://www.reddit.com/r/wallstreetbets/comments/xxx"}'
```

Params:
- `url` (string) — Full Reddit URL, OR
- `post_id` (string) — Reddit post ID (e.g., "1abc123")
- `subreddit` (string, optional) — Required with post_id for efficiency
- `sort` (string, optional) — Comment sort order
- `depth` (int, optional) — Comment depth limit

### `user`
Analyze a Reddit user's profile.

```bash
python3 scripts/reach.py query reddit user '{"username": "spez"}'
```

Params:
- `username` (string, required) — Reddit username

### `explain`
Get explanations of Reddit terms.

```bash
python3 scripts/reach.py query reddit explain '{"term": "karma"}'
```

Params:
- `term` (string, required) — Reddit term to explain

## Use cases for Rally

- **Social sentiment** — Search `r/wallstreetbets`, `r/stocks`, `r/investing` for ticker mentions to compute `social_heat`
- **Post volume tracking** — Count ticker mentions over time windows
- **User analysis** — Check credibility of users making stock claims

## Pitfalls

- **Rate limits are strict** — Anonymous mode is only 10 req/min. For production use, register OAuth credentials.
- **Cloud IP blocking** — Reddit may block requests from cloud IP ranges. OAuth authentication helps bypass this.
- **NSFW content** — Some subreddits contain NSFW posts. The connector returns raw content; filter as needed.
- **MCP server startup** — First call may be slow (~5s) as npx downloads the package. Subsequent calls are fast.
