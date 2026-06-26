---
name: instagram-analytics
description: "Track Instagram performance and analytics. Use when the user says 'Instagram analytics', 'Instagram metrics', 'how are my Reels doing', 'Instagram reach', 'IG engagement', 'Instagram follower growth', or wants to see reach, followers, interactions, and Reels performance for their Instagram Business account."
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://boring-doc.aiagent-me.com/getting-started/mcp.html
    requires:
      config:
        - MCP Connector link from boring.aiagent-me.com (contains embedded auth token)
---

# Instagram Analytics

Track your Instagram performance — reach, followers, interactions, Reels metrics, and post-level engagement. Powered by [Boring](https://boring-doc.aiagent-me.com).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL (`https://boring.aiagent-me.com/mcp/t/xxxxx...`) contains an embedded authentication token. Treat it like a password — do not share it publicly.
- **Token scope**: The embedded token is **read-only** for analytics. It can only fetch performance metrics and account metadata. It cannot publish, delete, or modify any content on your social media accounts.
- **Token storage**: The token is stored server-side in Boring's database (MongoDB on DigitalOcean). It is never written to your local filesystem. You can regenerate or revoke it anytime at [boring.aiagent-me.com/settings](https://boring.aiagent-me.com/settings).
- **Data flow**: Analytics queries are sent from Boring's server (Google Cloud, us-central1) to the platform's API on your behalf. Only performance metrics are retrieved — no content is uploaded or modified.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP link.
- **Third-party service**: This skill relies on [Boring](https://boring.aiagent-me.com), an open-source social media management tool. Source code: [github.com/snoopyrain](https://github.com/snoopyrain).

## Prerequisites

1. **Sign up** at [boring.aiagent-me.com](https://boring.aiagent-me.com) with Google
2. **Connect Instagram** — requires an Instagram Business or Creator account
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token — treat it like a password)
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Available Tools

| Tool | Data Source | Best For |
|------|-----------|----------|
| `boring_get_performance` | Real-time platform API | Account-level overview (reach, followers, interactions) |
| `boring_get_video_analytics` | Real-time platform API | Per-post/Reel metrics (views, likes, comments, shares) |
| `boring_get_posts_performance` | Daily snapshots (collected at 2 AM) | Historical post performance over date ranges |
| `boring_get_publish_history` | Boring database | Publishing history and status tracking |

## Workflow

### Step 1: List Accounts

Call `boring_list_accounts` and filter for `instagram` platform.

### Step 2: Determine What the User Wants

| User Request | Tool to Use |
|-------------|------------|
| "How is my Instagram doing?" | `boring_get_performance` |
| "Show my best Reels" | `boring_get_video_analytics` |
| "Instagram performance this month" | `boring_get_posts_performance` |
| "What did I post on IG?" | `boring_get_publish_history` |

### Step 3: Fetch Data

#### Account-Level Performance
```
boring_get_performance(
  account_id="<account_id>",
  platform="instagram",
  period="week"       // "day", "week", or "month"
)
```

#### Per-Post Analytics (Real-Time)
```
boring_get_video_analytics(
  account_id="<account_id>",
  platform="instagram",
  limit=20             // max 100
)
```

#### Historical Post Performance (Snapshots)
```
boring_get_posts_performance(
  account_id="<account_id>",
  since="2025-12-01",
  until="2025-12-31",
  limit=20
)
```

### Step 4: Present Results

Format the data clearly:
- **Account overview**: Show reach, followers, profile views in a summary table
- **Post analytics**: Rank posts by engagement, highlight top Reels
- **Historical**: Show trends over time, compare Reels vs Photos vs Carousels

## Instagram Metrics

| Metric | Description |
|--------|-------------|
| `reach` | Accounts reached |
| `follower_count` | Total followers |
| `profile_views` | Profile visits |
| `total_interactions` | Likes + comments + saves + shares |
| `ig_reels_avg_watch_time` | Average Reels watch time |
| `ig_reels_video_view_total_time` | Total Reels view time |

## Error Handling

| Error | Solution |
|-------|----------|
| `InvalidApiKey` | MCP link may be invalid — regenerate it at boring.aiagent-me.com Settings |
| `InvalidAccountId` | Run `boring_list_accounts` to get valid IDs |
| `TokenExpired` | Reconnect account at boring.aiagent-me.com |
| No data returned | Account may be newly connected — data collection runs daily at 2 AM |

## Documentation

Full API docs: [boring-doc.aiagent-me.com](https://boring-doc.aiagent-me.com)
