---
name: linkhut
description: LinkHut bookmark management API integration with managed OAuth. Save, organize, search, and manage bookmarks with tags, notes, and privacy settings. Use this skill when users want to save bookmarks, search saved links, organize bookmarks with tags, or manage their reading list.
---

# LinkHut

![LinkHut](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/linkhut.png)

Manage bookmarks from chat -- save links, organize with tags, search your collection, and maintain a reading list. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkhut) for hosted OAuth.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect LinkHut |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect LinkHut |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  LinkHut API     │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

## Install

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

## Quick Start

```javascript
// 1. Save a bookmark
clawlink_call_tool({ tool: "linkhut_add_bookmark", parameters: { url: "https://example.com/article", tags: "reading tech" } })

// 2. Search your bookmarks
clawlink_call_tool({ tool: "linkhut_get_bookmarks", parameters: { tag: "tech" } })

// 3. List all tags
clawlink_call_tool({ tool: "linkhut_get_all_tags", parameters: {} })
```

## Authentication

ClawLink handles OAuth with LinkHut. No API keys needed. Connect at [claw-link.dev/dashboard?add=linkhut](https://claw-link.dev/dashboard?add=linkhut).

## Connection Management

```javascript
// List connections
clawlink_list_integrations()

// Verify by listing bookmarks
clawlink_call_tool({ tool: "linkhut_get_bookmarks", parameters: {} })
```

## Security & Permissions

- **Read** tools are safe and require no confirmation
- **Write** tools require confirmation before execution
- Bookmark deletion is high-impact and irreversible

## Tool Reference

### Bookmark Operations

| Tool | Description | Mode |
|------|-------------|------|
| `linkhut_add_bookmark` | Save a new bookmark with tags, notes, and privacy settings | Write |
| `linkhut_get_bookmarks` | Retrieve bookmarks with filtering by tag, date, or URL | Read |
| `linkhut_update_bookmark` | Update bookmark metadata (title, description, tags) | Write |
| `linkhut_delete_bookmark` | Delete a bookmark by URL | Write |

### Tag Operations

| Tool | Description | Mode |
|------|-------------|------|
| `linkhut_get_all_tags` | List all tags with usage counts | Read |

## Code Examples

### Example 1: Save and organize bookmarks

```javascript
// Save a bookmark with tags and notes
await clawlink_call_tool({
  tool: "linkhut_add_bookmark",
  parameters: {
    url: "https://example.com/great-article",
    tags: "reading ai machine-learning",
    extended: "Great overview of transformer architectures",
    toread: true
  }
});

// Find bookmarks tagged "ai"
const bookmarks = await clawlink_call_tool({
  tool: "linkhut_get_bookmarks",
  parameters: { tag: "ai" }
});
```

### Example 2: Search and manage

```javascript
// Get a specific bookmark by URL
const bookmark = await clawlink_call_tool({
  tool: "linkhut_get_bookmarks",
  parameters: { url: "https://example.com/specific-page" }
});

// Update bookmark tags
await clawlink_call_tool({
  tool: "linkhut_update_bookmark",
  parameters: {
    url: "https://example.com/specific-page",
    tags: "updated-tag new-tag"
  }
});
```

### Example 3: Tag overview

```javascript
// List all tags and their counts
const tags = await clawlink_call_tool({
  tool: "linkhut_get_all_tags",
  parameters: {}
});

// Get bookmarks from a specific date
const dailyBookmarks = await clawlink_call_tool({
  tool: "linkhut_get_bookmarks",
  parameters: { date: "2026-06-08" }
});
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm `linkhut` is connected.
2. Call `clawlink_list_tools --integration linkhut` to see the live catalog.
3. Use `clawlink_search_tools({ query: "bookmark", integration: "linkhut" })` to find specific tools.

## Execution Workflow

```
READ (safe):     get_bookmarks → get_all_tags
WRITE (confirm): add_bookmark → update_bookmark
DELETE (high):   delete_bookmark
```

## Notes

- Tags are space-separated when specifying multiple tags
- Bookmarks can be marked as private (not shared) or read/unread (`toread`)
- Delete requires the exact URL of the bookmark
- Update is idempotent -- repeated calls produce the same result

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| 401 Unauthorized | OAuth token expired -- reconnect at dashboard |
| 404 Not Found | Bookmark with that URL does not exist |
| 409 Conflict | Bookmark with that URL already exists (use update instead) |
| 422 Unprocessable | Missing required URL parameter |

## Troubleshooting

### Tools Not Visible
- Start a fresh OpenClaw chat to reload plugin catalog
- Call `clawlink_list_integrations` to confirm pairing

### Bookmark Already Exists
- Use `linkhut_update_bookmark` instead of `linkhut_add_bookmark`
- Use `linkhut_get_bookmarks` with the URL to check if it exists first

## Resources

- LinkHut: https://linkhut.org/
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkhut
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkhut)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
