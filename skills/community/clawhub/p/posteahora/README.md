# PosteAhora CLI

**Social media scheduling & publishing CLI for AI agents and developers** — plan,
schedule, and publish posts across Instagram, TikTok, YouTube, X (Twitter),
Facebook, LinkedIn, Threads, Bluesky, Mastodon, Discord, Telegram, WordPress,
Dev.to, Tumblr, Pinterest and Google Business, programmatically.

The PosteAhora CLI is a thin, zero-dependency command-line interface to the
[PosteAhora](https://posteahora.com) public REST API. It lets developers, scripts,
CI pipelines, and AI agents automate social media publishing — create and schedule
posts, manage a content-idea backlog, upload media, and read analytics — across
every major network from one tool.

> Prefer an MCP integration for your AI agent? Use
> [`@posteahora/mcp`](https://github.com/posteahora/mcp). Prefer raw HTTP? See the
> [REST API reference](https://posteahora.com/docs/api).

---

## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Authentication](#authentication)
- [Commands](#commands)
  - [Accounts](#accounts)
  - [Creating & scheduling posts](#creating--scheduling-posts)
  - [Managing posts](#managing-posts)
  - [Ideas](#ideas)
  - [Analytics](#analytics)
  - [Media uploads](#media-uploads)
- [Supported platforms](#supported-platforms)
- [Configuration](#configuration)
- [Official resources](#official-resources)

---

## Features

- **Publish now, schedule, or draft** posts to one or many channels at once.
- **Multi-platform posting** — one command fans a post out to every connected network.
- **Media uploads** — attach images and video via presigned URLs.
- **Content ideas backlog** — capture and organize ideas before they become posts.
- **Analytics** — read views, likes, comments, shares and more across platforms.
- **AI-agent friendly** — every command has clear output and a `--json` flag.
- **Zero-dependency** — native `fetch`, installs in seconds, runs anywhere Node 18+ runs.

---

## Installation

### From npm (recommended)

```bash
npm install -g @posteahora/cli
# or
pnpm install -g @posteahora/cli
```

The installed command is `posteahora`. You can also run it without installing:

```bash
npx @posteahora/cli --help
```

**Requirements:** Node.js 18 or newer.

---

## Authentication

**Required.** Every command needs a PosteAhora API key.

1. Open PosteAhora → **Settings → API & integrations**.
2. Create a key and copy it (shown once) — it looks like `pah_live_…`.

```bash
posteahora auth --key pah_live_xxxxxxxx
```

The key is validated against the API and stored in `~/.posteahora/config.json`.
In CI or scripts, pass it per-run instead:

```bash
export POSTEAHORA_API_KEY=pah_live_xxxxxxxx
```

Check status any time:

```bash
posteahora auth
```

---

## Commands

### Accounts

List the social accounts connected to your PosteAhora workspace. **Call this first**
— publishing targets an account by its ID.

```bash
posteahora accounts
posteahora accounts --json
```

Returns each account's platform, username, ID, and connection status.

---

### Creating & scheduling posts

**Publish now** to one or more channels (`platform:accountId` pairs from
`posteahora accounts`):

```bash
posteahora post "Launch day 🚀" --to twitter:a1b2 --to linkedin:c3d4
```

**Schedule** for a future time (ISO 8601):

```bash
posteahora post "Morning tip ☕" --to instagram:e5f6 --at 2026-07-20T09:00:00Z
```

**Draft only** (nothing goes live):

```bash
posteahora post "Rough idea" --to twitter:a1b2 --draft
```

**With media** (upload first, then attach the public URL):

```bash
posteahora upload ./reel.mp4
posteahora post "New reel" --to instagram:e5f6 --media https://cdn.posteahora.com/… --at 2026-07-20T09:00:00Z
```

**Multi-platform, multi-line caption** (a heredoc keeps the line breaks — inside
double quotes the shell would publish a backslash-n literally):

```bash
CAPTION=$(cat <<'EOF'
Big news 🚀

We shipped the thing you asked for.

#launch #product
EOF
)

posteahora post "$CAPTION" \
  --to twitter:a1b2 --to linkedin:c3d4 --to threads:g7h8
```

Captions publish byte for byte, so spacing is yours to get right — see
[PUBLISHING.md](PUBLISHING.md#caption-formatting).

**Options:**
- `--to platform:accountId` — target channel (repeatable or comma-separated) **(required)**
- `--media <url>` — attach media (repeatable; use `upload` to get a URL)
- `--at <ISO 8601>` — schedule for a future time (otherwise publishes now)
- `--draft` — create a draft instead of publishing
- `--title <text>` — optional title (used where the platform supports it)
- `--media-type image|video`
- `--post-type post|reel|story`
- `--json` — machine-readable output
- `--hashtags a,b,c` — stored on the post but **not published**; put hashtags in
  the caption text instead

---

### Managing posts

```bash
# List posts (optionally filter by status)
posteahora posts
posteahora posts --status scheduled
posteahora posts --status published --limit 100
```

Status values: `draft`, `scheduled`, `queued`, `published`, `failed`.

---

### Ideas

A lightweight content backlog — brainstorm before you publish.

```bash
posteahora ideas add "5 hooks for launch week" --tags launch,eng
posteahora ideas list
```

---

### Analytics

Read performance across platforms (metrics refresh hourly).

```bash
posteahora analytics
posteahora analytics --period 7d
posteahora analytics --period 90d --platform instagram
```

`--period` = `7d` | `30d` (default) | `90d` | `all`.

---

### Media uploads

Upload an image or video and get a public URL to use with `--media`.

```bash
posteahora upload ./photo.jpg
posteahora upload ./video.mp4
```

See [SUPPORTED_FILE_TYPES.md](SUPPORTED_FILE_TYPES.md) for accepted formats.

---

## Supported platforms

| Platform | Publish | Schedule | Analytics |
|----------|:------:|:--------:|:---------:|
| Instagram | ✅ | ✅ | ✅ |
| TikTok | ✅ | ✅ | ✅ |
| YouTube | ✅ | ✅ | ✅ |
| X (Twitter) | ✅ | ✅ | ✅ |
| Facebook | ✅ | ✅ | ✅ |
| LinkedIn | ✅ | ✅ | — |
| Threads | ✅ | ✅ | ✅ |
| Bluesky | ✅ | ✅ | ✅ |
| Mastodon | ✅ | ✅ | ✅ |
| Discord | ✅ | ✅ | — |
| Telegram | ✅ | ✅ | — |
| WordPress | ✅ | ✅ | — |
| Dev.to | ✅ | ✅ | — |
| Tumblr | ✅ | ✅ | — |
| Pinterest | ✅ | ✅ | ✅ |
| Google Business | ✅ | ✅ | — |

Connect accounts in the PosteAhora app; the CLI targets them by ID.

---

## Configuration

| Setting | Source (in order of precedence) |
|---------|---------------------------------|
| API key | `--key` flag → `POSTEAHORA_API_KEY` → `~/.posteahora/config.json` |
| Base URL | `POSTEAHORA_API_URL` (default `https://api.posteahora.com/functions/v1/api`) |

---

## Official resources

- **Website:** https://posteahora.com
- **Documentation:** https://posteahora.com/docs
- **API reference:** https://posteahora.com/docs/api
- **CLI (npm):** https://www.npmjs.com/package/@posteahora/cli
- **CLI (GitHub):** https://github.com/posteahora/cli
- **MCP server:** https://github.com/posteahora/mcp
- **n8n node:** https://www.npmjs.com/package/n8n-nodes-posteahora

---

## License

MIT
