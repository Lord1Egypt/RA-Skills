---
name: juicer
description: Connect Juicer to OpenClaw. Juicer pulls public posts from Instagram, TikTok, X, Facebook, LinkedIn, YouTube, Reddit, Bluesky and more into one place: embed social feeds and walls on any website, track brand mentions, listen to topics and check competitors. Use when the user mentions Juicer, wants social posts on a website or wants social media data from several networks.
version: 1.0.3
metadata:
  openclaw:
    emoji: "🧃"
    homepage: https://developers.juicer.io/mcp-server
    primaryEnv: JUICER_API_KEY
    envVars:
      - name: JUICER_API_KEY
        required: false
        description: Optional. Only needed when the Juicer MCP server is not connected. Get one at https://www.juicer.io/developer
---

# Juicer

Juicer collects public social media posts and turns them into embeddable feeds, social walls and data. This skill connects Juicer and explains what it can do. The task skills build on it:

- `juicer-brand-mentions`: daily alerts when people mention a brand
- `juicer-social-listening`: what people say about a topic
- `juicer-competitor-checker`: what competitors post and what works for them
- `juicer-social-feed`: social posts on a website in one message
- `juicer-social-wall`: a moderated live wall for an event

## Step 1: check if Juicer is already connected

If Juicer tools such as `get_account` are available, call `get_account` and go to Step 3.

## Step 2: connect

Offer the user these options, best first.

**A. Juicer MCP server with browser sign-in (recommended, works for scheduled jobs).**

In the Control UI: Settings → MCP → Add server. Name `juicer`, transport Streamable HTTP, URL `https://api.juicer.io/mcp`. Then sign in when OpenClaw asks.

Or from the CLI:

```bash
openclaw mcp add juicer --url https://api.juicer.io/mcp --transport streamable-http --auth oauth
openclaw mcp login juicer
openclaw mcp doctor juicer --probe
```

`--auth oauth` is required: without it the add step fails with `401 authentication refused`.

`openclaw mcp login juicer` prints a www.juicer.io link and waits a few minutes for it. Give the user that link right away and ask them to open it and approve access. A new user can create a free Juicer account on that page. When they approve, the login finishes by itself ("MCP OAuth credentials saved"). If it times out, run the login again for a fresh link.

`openclaw mcp doctor juicer --probe` should then report `juicer: ok`, and `openclaw mcp probe juicer` lists 33 Juicer tools.

**B. Quick start with only an email (no dashboard, good for a first try).**

Ask the user for their email, then:

```bash
curl -s -X POST https://api.juicer.io/v1/authorize \
  -H 'Content-Type: application/json' \
  -d '{"email":"USER_EMAIL","client_name":"OpenClaw"}'
```

- New email: the response contains a temporary `api_key`. Tell the user to confirm the email Juicer sends them.
- Existing Juicer account: the response contains a link. Ask the user to open it and approve, then poll the `poll_url` every few seconds until the key arrives.

These keys expire after a few hours. For anything scheduled, use option A or a permanent key from https://www.juicer.io/developer.

**C. Permanent API key.** The user creates one at https://www.juicer.io/developer and stores it as `JUICER_API_KEY` in OpenClaw's secrets. Never print the key in chat or write it into files.

## Step 3: check the account before spending credits

`get_account` (or `GET https://api.juicer.io/v1/account`) returns the plan, feed limits and the credit balance.

- Data lookups (`get_data_posts`, `get_data_profiles`) spend credits per platform per call: Facebook 6, Instagram, TikTok and LinkedIn 3, every other platform 1.
- Every new Juicer account gets 30 Sandbox credits once. A full brand check can use 40 or more, so tell the user before a run that would use more than they have.
- Adding a source (`create_source`) costs credits for its first fetch, at the same per-platform rates. On paid API plans each later sync of that source is metered too.
- Creating feeds, moderating posts and getting embed codes do not spend credits; they follow the plan's feed and source limits.
- On the free plan, after the trial: X, TikTok hashtag and keyword, Reddit and LinkedIn sources stop syncing, Bluesky needs Pro or Enterprise and feeds refresh once a day. Faster refresh needs a higher plan; it cannot be changed in the dashboard on the free plan.
- A `402 insufficient_credits` or `422` with an upgrade link is not a failure to hide: show the user the message and the link.

## Without the MCP server (REST)

Base URL `https://api.juicer.io/v1`, header `Authorization: Bearer $JUICER_API_KEY`. Each MCP tool maps to one endpoint:

| Tool | Endpoint |
|---|---|
| `get_account` | `GET /account` |
| `list_platforms` | `GET /platforms` |
| `get_data_posts` | `GET /data/posts?term=&platforms=&term_type=&cursor=` |
| `get_data_profiles` | `GET /data/profiles?term=&platforms=` |
| `create_feed` | `POST /feeds` |
| `update_feed` | `PATCH /feeds/{id}` |
| `create_source` | `POST /feeds/{feed_id}/sources` |
| `list_feed_posts` | `GET /feeds/{feed_id}/posts` |
| `moderate_post` | `POST /feeds/{feed_id}/posts/{id}/approve` (or `/reject`, `/pin`, `/unpin`) |
| `bulk_moderate_posts` | `POST /feeds/{feed_id}/posts/bulk` |
| `get_feed_embed` | `GET /feeds/{feed_id}/embed` |
| `create_social_account_connect_url` | `POST /social_accounts/connect_url` |

Full reference: https://developers.juicer.io

## What each network supports

Call `list_platforms` for the live list. As of October 2026:

| Network | Data lookups by |
|---|---|
| Reddit | keyword (`mentions`), subreddit (`channel`) |
| X | `@handle`, `#hashtag`, mentions of a handle |
| TikTok | `@handle`, `#hashtag`, keyword (`mentions`) |
| Instagram, Facebook, LinkedIn, Bluesky | `@handle` or `#hashtag` only, no keyword search |
| YouTube | `@handle`, channel, `#hashtag` |
| Google | reviews for a place |

Say this plainly when the user asks for something a network cannot do, for example "find every Instagram post that mentions us": Instagram only supports their own account and hashtags.

## Rules

- Destructive actions (delete feed, delete source, hard delete posts, disconnect a social account) need the user's explicit yes first.
- Never invent posts, numbers or accounts. If a lookup returns nothing, say which terms and networks were searched.
