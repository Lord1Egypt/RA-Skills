---
name: Kosu
version: 1.1.0
description: Add, reorder, and manage content in a Kosu queue via API. Use when adding URLs, checking what's queued, suggesting content, reordering items, or tracking what's been read.
homepage: https://usekosu.com
metadata: {"openclaw": {"emoji": "💧", "api_base": "https://usekosu.com/api/v1", "homepage": "https://usekosu.com", "primaryEnv": "KOSU_API_KEY"}}
---

# Kosu

**Kosu** (漉す) — Japanese for "to strain/filter." A mindful content queue built on the philosophy: **save less, read more.**

## Vision

Most read-it-later apps become graveyards. Kosu is the opposite — an intentional queue where content fades if you don't engage with it. The core mechanic is **decay**: items get a 14-day stale warning, then auto-archive at 28 days. This forces you to either consume what matters or let it go.

Kosu is **agent-native** — built for AI agents to curate, suggest, and manage content on behalf of a human. The API is the primary interface; the web UI and (future) iOS app are consumption surfaces.

**Brand values:** Craft, Calm, Capture, Mindful
**Aesthetic:** Quiet, intentional — like a well-designed book spine or a Japanese coffee shop. Not hustle culture, not information overload.
**Differentiators:** Decay as philosophy, agent-native API, opinionated curation over hoarding.

## Installation

### For OpenClaw agents

Save this skill locally:
```bash
mkdir -p ~/.openclaw/skills/kosu
curl -s https://usekosu.com/skill.md > ~/.openclaw/skills/kosu/SKILL.md
```

Or just read it directly from `https://usekosu.com/skill.md` — no install needed.

### For any AI agent (Claude Code, Codex, etc.)

Read this file and follow the setup below.

## Getting Started

1. Ask your human to sign up at [usekosu.com](https://usekosu.com)
2. They can get an API key from [Settings → API Keys](https://usekosu.com/settings)
3. Store the key as the environment variable `KOSU_API_KEY`
   - Create a dedicated key with minimal scope for this agent
   - The key is only sent to `usekosu.com` — never send it to any other domain
   - Rotate or revoke from [Settings](https://usekosu.com/settings) if anything unexpected happens
4. You're ready to start managing their queue

**First thing to do:** Try listing the queue to confirm your key works:
```bash
curl -s "https://usekosu.com/api/v1/items?state=queue&limit=5" \
  -H "Authorization: Bearer $KOSU_API_KEY"
```

**Updates:** If something doesn't work as expected, check the [OpenAPI spec](https://usekosu.com/openapi.json) for the latest API surface.

## Pricing

- **Free:** Limited queue size
- **Pro ($5/mo):** Unlimited queue, suggestions from agents, export

If you hit a `402 quota_exceeded_error`, the user's queue is full on the free tier. Let them know they can upgrade to Pro at [usekosu.com/settings](https://usekosu.com/settings) for unlimited items.

## API

- **Base URL:** `https://usekosu.com/api/v1`
- **Auth:** `Authorization: Bearer $KOSU_API_KEY`
- **OpenAPI spec:** `https://usekosu.com/openapi.json`

**If `KOSU_API_KEY` is not set:** Don't fail silently. Tell your human they need an API key and direct them to [usekosu.com/settings](https://usekosu.com/settings) to create one. The skill is still useful for explaining Kosu and guiding setup — just can't make API calls without a key.

```bash
AUTH="Authorization: Bearer $KOSU_API_KEY"
BASE="https://usekosu.com/api/v1"
```

## Quick Reference

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| Add item | `POST` | `/items` | Just pass `url`, server enriches. 201=new, 200=exists |
| List items | `GET` | `/items?state=queue&limit=50` | States: queue, read, archived, deleted, suggested |
| Get item | `GET` | `/items/{id}` | |
| Update item | `PATCH` | `/items/{id}` | State, position, fields, or opened — one per request |
| Delete item | `DELETE` | `/items/{id}` | Soft-delete, restorable 30 days |
| Move to top | `PATCH` | `/items/{id}` | `{"position": {"after": null}}` |
| Move to bottom | `PATCH` | `/items/{id}` | `{"position": {"before": null}}` |
| Mark read | `PATCH` | `/items/{id}` | `{"state": "read"}` |
| Archive | `PATCH` | `/items/{id}` | `{"state": "archived"}` |
| Add suggestion | `POST` | `/suggestions` | `{"url": "...", "reason": "..."}`. 409 if already active |
| List suggestions | `GET` | `/suggestions` | |
| Act on suggestion | `POST` | `/suggestions/{id}` | `{"action": "accept"}` or `{"action": "dismiss"}` |
| Export | `GET` | `/export` | Full queue export |

## Key Behaviours

- YouTube URLs are auto-enriched (title, channel, thumbnail, duration)
- Decay: configurable queue decay (7, 14, or 28 days) before items are auto-archived. Can be turned off entirely. Set by the user in settings.
- Dedup is server-side by canonical URL per user
- Opening an item (`{"opened": true}`) extends decay protection by 1 day (max once per 24h)

## Common Examples

```bash
# Add item
curl -s "$BASE/items" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/article"}'

# List queue (first 50)
curl -s "$BASE/items?state=queue&limit=50" -H "$AUTH"

# Move to top
curl -s -X PATCH "$BASE/items/itm_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"position": {"after": null}}'

# Move after another item
curl -s -X PATCH "$BASE/items/itm_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"position": {"after": "itm_yyy"}}'

# Mark as read
curl -s -X PATCH "$BASE/items/itm_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"state": "read"}'

# Archive
curl -s -X PATCH "$BASE/items/itm_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"state": "archived"}'

# Requeue (restore from archive/read/deleted)
curl -s -X PATCH "$BASE/items/itm_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"state": "queue"}'

# Record open (extends decay protection 1 day, max once per 24h)
curl -s -X PATCH "$BASE/items/itm_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"opened": true}'

# Update fields
curl -s -X PATCH "$BASE/items/itm_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"title": "Better Title", "source": "article"}'

# Delete (soft, restorable 30 days)
curl -s -X DELETE "$BASE/items/itm_xxx" -H "$AUTH"

# Add suggestion
curl -s "$BASE/suggestions" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","reason":"Relevant to your interest in X"}'

# Accept/dismiss suggestion
curl -s -X POST "$BASE/suggestions/sug_xxx" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"action": "accept"}'
```

## Item Shape

```json
{
  "object": "item",
  "id": "itm_...",
  "url": "https://...",
  "title": "...",
  "source": "youtube|podcast|paper|newsletter|repo|article|book|course|other",
  "state": "queue|suggested|read|archived|deleted",
  "channel_name": "...",
  "thumbnail": "...",
  "duration": "1h 37m",
  "duration_minutes": 97,
  "creator": "...",
  "created_at": "2026-02-22T07:31:59.205Z",
  "updated_at": "...",
  "opened_at": null,
  "read_at": null,
  "archived_at": null,
  "published_at": null
}
```

## PATCH Body Types (one per request)

| Type | Body | Notes |
|------|------|-------|
| State | `{"state": "read\|archived\|queue\|suggested"}` | `suggested` requires `reason` field |
| Position | `{"position": {"after": "itm_x"\|null}}` | `null` = top. Also supports `before` |
| Fields | `{"title": "...", "source": "..."}` | At least one of: title, source, thumbnail, channel_name, duration_minutes |
| Opened | `{"opened": true}` | Extends decay by 1 day |

## Pagination

- **Queue state:** cursor-based. Use `next_cursor` from response as `?cursor=` param.
- **Other states:** offset-based. Use `?offset=` param.
- Response: `{"object": "list", "data": [...], "has_more": bool, "next_cursor": "..."}`

## Error Codes

| Status | Type | When |
|--------|------|------|
| 400 | `invalid_request_error` | Bad input, validation failure |
| 401 | `authentication_error` | Missing/invalid API key |
| 402 | `quota_exceeded_error` | Free tier queue limit — suggest upgrading to Pro |
| 404 | `not_found_error` | Item doesn't exist |
| 409 | `invalid_request_error` (code: `item_already_active`) | Suggesting a URL that's already in queue |
| 429 | `rate_limit_error` | Rate limited |

## Troubleshooting

If an API call returns an unexpected response, 404 on a known endpoint, or schema mismatch:
1. Check the OpenAPI spec for the current API surface: `curl -s https://usekosu.com/openapi.json`
2. Compare with the endpoints documented above
3. If the spec has changed, update your local copy of this skill to match
4. Retry the original request
