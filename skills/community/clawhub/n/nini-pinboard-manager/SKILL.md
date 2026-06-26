---
name: pinboard-manager
description: >-
  Use this skill for ALL Pinboard bookmark management tasks — this is the go-to
  skill whenever Pinboard (pinboard.in) is involved. Invoke immediately when the
  user wants to: audit or reorganize messy tags, check for broken/dead links,
  identify stale or outdated bookmarks, clean up their bookmark collection, or
  manage their Pinboard account in any way. Also use when the user says 整理书签,
  检查死链, 整理 tag, 书签管理, pinboard cleanup, bookmark audit, tag consistency,
  timeliness check, pinboard 过时检测. Do NOT trigger for: browser bookmark management,
  Raindrop.io, or general URL checking without Pinboard context.
metadata: {"openclaw":{"emoji":"📌","requires":{"bins":["curl"],"env":["PINBOARD_AUTH_TOKEN"]}}}
---

# Pinboard Manager

Interactive Pinboard bookmark management with tag auditing, dead link detection, and content timeliness checking.

## Prerequisites

| Tool | Type | Required | How to get |
|------|------|----------|------------|
| Pinboard account | service | Yes | [pinboard.in](https://pinboard.in/) |
| `PINBOARD_AUTH_TOKEN` | env var | Yes | See [user-config.md](references/user-config.md) |
| `curl` | cli | Yes | Built-in on macOS/Linux |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool or token, directly guide the user through setup step by step.

## First-Time Setup

If `~/.config/nini-skill/pinboard-manager/tag-convention.md` does not exist, run the
**Tag Convention Generator** before any other mode:

1. Fetch all bookmarks via the Pinboard API
2. Analyze existing tags: frequency, patterns, languages, potential typos
3. Present findings to the user:
   - Top 30 tags by frequency
   - Tags that look like typos or duplicates
   - Chinese/non-English tags that may need English equivalents
   - Tags with inconsistent casing or separators
4. Ask the user about their preferred categories (tech, life, culture, etc.)
5. Generate `~/.config/nini-skill/pinboard-manager/tag-convention.md` based on the
   analysis and user input, following the structure in `references/tag-convention.example.md`
6. Confirm with the user before saving

> An example convention is provided at `references/tag-convention.example.md` for
> reference. Users should customize it to match their own bookmarking habits.

## Mode Selection

| User Intent | Mode | Section |
|-------------|------|---------|
| 「pinboard 整理 tag」「pinboard audit」「整理书签」 | Tag Audit | [Tag Audit Mode](#tag-audit-mode) |
| 「pinboard 检查死链」「pinboard check links」 | Dead Link Detection | [Dead Link Detection Mode](#dead-link-detection-mode) |
| 「pinboard 检查时效」「pinboard timeliness check」「pinboard 过时检测」 | Timeliness Check | [Timeliness Check Mode](#timeliness-check-mode) |

## API Helpers

All Pinboard API calls use these patterns:

### Fetch bookmarks

```bash
# Fetch all bookmarks
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json"

# Fetch bookmarks with toread=yes
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json&toread=yes"

# Fetch a specific bookmark by URL
curl -s "https://api.pinboard.in/v1/posts/get?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL"
```

### Update a bookmark (overwrite mode)

**CRITICAL**: Always pass ALL fields to avoid data loss. The `/posts/add` endpoint overwrites the entire bookmark.

```bash
curl -s "https://api.pinboard.in/v1/posts/add?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL&description=ENCODED_TITLE&extended=ENCODED_NOTES&tags=ENCODED_TAGS&shared=ORIGINAL_SHARED&toread=ORIGINAL_TOREAD&replace=yes"
```

Required fields to preserve:

- `url` — the bookmark URL (identifier)
- `description` — title
- `extended` — notes/description
- `tags` — space-separated tag list
- `shared` — `yes` or `no`
- `toread` — `yes` or `no`
- `replace` — MUST be `yes` to update existing

### Delete a bookmark

```bash
curl -s "https://api.pinboard.in/v1/posts/delete?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL"
```

### Rate limiting

Pinboard recommends at most 1 API call per 3 seconds. When making multiple calls (batch updates, link checks), add `sleep 3` between calls.

> **`posts/all` special limit**: This endpoint is rate-limited to **once every 5 minutes**. Cache the result in `/tmp/pinboard_all.json` and reuse it within the same session. If both Tag Audit and Dead Link Detection are run consecutively, reuse the cached file.

## Tag Audit Mode

Audit bookmarks against the tag convention, present issues in batches, apply fixes with confirmation.

See [references/tag-audit.md](references/tag-audit.md) for the complete 5-step workflow.

## Dead Link Detection Mode

Check all bookmarks for broken URLs via HTTP HEAD/GET, report results for user action.

See [references/dead-link.md](references/dead-link.md) for the complete 5-step workflow.

## Timeliness Check Mode

Identify outdated tech bookmarks using heuristic pre-filtering + AI content analysis via Jina Reader. Does NOT auto-delete -- all actions require user confirmation.

See [references/timeliness.md](references/timeliness.md) for the complete 7-step workflow.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `PINBOARD_AUTH_TOKEN not set` | Env var missing | See [user-config.md](references/user-config.md) |
| `403 Forbidden` on API calls | Invalid or expired token | Re-check token at Pinboard settings |
| `429 Too Many Requests` | Rate limit exceeded | Increase sleep between calls; `posts/all` is limited to once per 5 min |
| Partial update lost data | Missing fields in `/posts/add` | Always pass ALL original fields with `replace=yes` |
| Jina Reader empty response | Site blocks Jina Reader or URL is broken | Skip this bookmark, mark as "unable to fetch" |
| Jina Reader timeout | Slow site or network issue | Skip and continue with next candidate |
