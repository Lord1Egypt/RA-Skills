# Notion

The only platform here that other people can read without a terminal, and the only one where notes are rows in a database rather than files. Driven through the REST API.

**Contents:** [Requirements](#requirements) · [The Database](#the-database) · [Operations](#operations) · [Property Shapes](#property-shapes) · [Blocks for Notes](#blocks-for-notes) · [Limits That Bite](#limits-that-bite) · [Errors](#errors) · [Fallback](#fallback) · [Notion Traps](#notion-traps)

**Before writing**, read `notion_database_id` in `~/Clawic/data/notes/config.yaml` and the property map in `## Platform Facts`. Notion rejects any property name it does not recognize, so writing without the map produces a 400 on every note until the map is read.

This file covers using Notion as a note store. Building against the API — OAuth, webhooks, bulk backfills, relation and rollup mechanics, pagination edge cases — is `notion-api-integration`.

## Requirements

A Notion account and an internal integration the user creates at notion.so/my-integrations. The user stores the key themselves; the skill only references it.

- **The key is a secret**: never written under `~/Clawic/data/`. Record only its pointer — `env:NOTION_API_KEY` or `file:~/.config/notion/api_key` — in `## Platform Facts` (`memory-template.md`).
- **Each page or database must be shared with the integration** in the Notion UI ("..." → Connect to → the integration). A database that was never shared returns 404 on an object the user can see in their browser — this is the single most common Notion failure and it is not a permissions bug in the code.
- API version pinning is required on every request via the `Notion-Version` header. Header values and endpoint shapes below were current at 2026-07; confirm against Notion's changelog before assuming an old script still works.

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)   # the user's own file; never copied into ~/Clawic/data/
AUTH=(-H "Authorization: Bearer $NOTION_KEY" -H "Notion-Version: 2025-09-03" -H "Content-Type: application/json")
```

## The Database

One database for notes, with properties that mirror the corpus-wide frontmatter so nothing is lost when a note moves between platforms:

| Property | Type | Values |
|---|---|---|
| Name | Title | The claim (SKILL.md Rule 2) |
| Type | Select | Meeting, Decision, Project, Journal, Research, Quick |
| Date | Date | The event date, not the creation date |
| Tags | Multi-select | The same vocabulary as `tags:` elsewhere |
| Project | Text | The project name — a pointer into the shared `projects/` box |
| Status | Select | Draft, Active, Superseded, Archived |

Record the database id and the exact property names in `## Platform Facts` the first time they are read. Property names are case-sensitive and a renamed property breaks every write silently until the map is refreshed.

## Operations

```bash
# search
curl -sX POST "https://api.notion.com/v1/search" "${AUTH[@]}" \
  -d '{"query": "pricing"}'

# create a note as a database row
curl -sX POST "https://api.notion.com/v1/pages" "${AUTH[@]}" \
  -d '{
    "parent": {"database_id": "'"$DB"'"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Pricing: staying at three tiers"}}]},
      "Date": {"date": {"start": "2026-07-26"}},
      "Type": {"select": {"name": "Meeting"}},
      "Tags": {"multi_select": [{"name": "product"}, {"name": "pricing"}]}
    }
  }'

# add body content to that page
curl -sX PATCH "https://api.notion.com/v1/blocks/$PAGE_ID/children" "${AUTH[@]}" \
  -d '{"children": [
    {"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Decisions"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"Three tiers stay; revisit at 500 customers"}}]}},
    {"type":"to_do","to_do":{"rich_text":[{"text":{"content":"@alice: send the pricing deck — 2026-08-04"}}],"checked":false}}
  ]}'

# read a page and its content
curl -s "https://api.notion.com/v1/pages/$PAGE_ID" "${AUTH[@]}"
curl -s "https://api.notion.com/v1/blocks/$PAGE_ID/children" "${AUTH[@]}"
```

Creating a note is **two calls**: the page with its properties, then its blocks. A failure between them leaves a titled page with no body — check the second call's status and retry it rather than creating a second page.

## Property Shapes

Every property type has its own JSON shape; a wrong shape is a 400, not a coercion.

| Type | Shape |
|---|---|
| Title | `{"title": [{"text": {"content": "..."}}]}` |
| Rich text | `{"rich_text": [{"text": {"content": "..."}}]}` |
| Select | `{"select": {"name": "Meeting"}}` |
| Multi-select | `{"multi_select": [{"name": "a"}, {"name": "b"}]}` |
| Date | `{"date": {"start": "2026-07-26"}}` |
| Checkbox | `{"checkbox": true}` |
| Number | `{"number": 42}` |

A `select` value that does not exist yet is created by the write; a typo therefore becomes a permanent option in the dropdown. Validate against the recorded property map before writing.

## Blocks for Notes

`heading_2` for sections · `paragraph` for prose · `bulleted_list_item` for points · `numbered_list_item` for ordered steps · `to_do` for action items (they render as checkboxes and are what the user will tick) · `callout` for a decision worth surfacing · `divider` between sections.

Tables exist as `table` blocks and are laborious to build through the API. For a note routed to Notion, prefer bullets with the fields inline (`@alice — 2026-08-04 — send the pricing deck`) over a table.

## Limits That Bite

| Limit | Consequence |
|---|---|
| ~3 requests/second average | A 40-note import is a rate-limited job, not a loop; batch and pause |
| 100 results per page | Any listing needs `start_cursor` pagination or it silently returns a truncated corpus |
| 100 blocks per append call | A long note is several PATCH calls, in order |
| 2000 characters per rich-text object | A long paragraph must be split into multiple text objects |
| Integration sees only what is shared with it | Search returns a partial corpus and looks like a working search |

The pagination limit is the dangerous one: a search that stops at 100 looks successful. Any "not found" answer from Notion states whether pagination was followed (`retrieval.md`).

## Errors

| Status | Usual cause | First move |
|---|---|---|
| 401 | Key missing, revoked, or the wrong workspace | Confirm the key resolves; never print it |
| 404 on an object the user can see | The page or database was never shared with the integration | Share it in the UI, then retry |
| 400 `validation_error` | Property name or shape wrong | Re-read the property map; names are case-sensitive |
| 429 | Rate limit | Honour `Retry-After`; do not retry immediately |
| 409 | Conflicting concurrent edit | Re-read the page and reapply |

## Fallback

If the key is absent, the integration lacks access, or the API is unreachable: write locally, stamp `platform: local (fallback from notion)`, and say it in one line (SKILL.md Rule 1). Note content going to Notion leaves the machine — never route a type there that the user has not routed there themselves.

## Notion Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Debugging a 404 as a code bug | The database was never shared with the integration | Share first, then debug |
| Assuming a search returned everything | It stops at 100 with no warning | Paginate, and say whether you did |
| Writing without the property map | Every write 400s until the names are right | Read and record the map once |
| A typo in a `select` value | Creates a permanent bogus option in the dropdown | Validate against the map |
| Building tables through the API | Slow, brittle, and hard to read afterwards | Bullets with fields inline |
| Treating a partial two-call create as done | A titled page with no body, indistinguishable from an empty note | Check both calls, retry the second |
| Storing the key anywhere in `~/Clawic/data/` | It syncs, it is backed up, it is now exposed | Pointer only |
| Routing durable notes here without an export cadence | Databases flatten on export; relations and views do not survive | Quarterly export (`migration.md`) |

**Write triggers for this file** — in the same turn: the database id, the exact property names and the key's pointer (never the key) to `## Platform Facts` in `~/Clawic/data/notes/memory.md`; `notion_database_id` and the routing choice to `config.yaml` and `## Note Map`; every action item found in a Notion page to `actions.md` with `Source: notion:<Page>`; the quarterly export cadence to the `## Due` table. Formats and thresholds: `memory-template.md`.
