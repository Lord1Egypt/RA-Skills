# Pages — Create, Update, Archive

A page is properties plus a block tree. This file is the properties and lifecycle half; content is `blocks.md`, and per-type value shapes are `properties.md`.

**Contents:** [Retrieve](#retrieve) · [Create in a Database](#create-in-a-database) · [Create Under a Page](#create-under-a-page) · [Update Properties](#update-properties) · [Archive, Trash, Restore](#archive-trash-restore) · [Icons and Covers](#icons-and-covers) · [Ids and URLs](#ids-and-urls) · [Duplicating and Templating](#duplicating-and-templating)

## Retrieve

```bash
curl 'https://api.notion.com/v1/pages/PAGE_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

Returns properties, parent, icon, cover, `archived`/`in_trash`, timestamps — **not content**, and relation/rollup/people capped at 25 entries (SKILL.md Rule 8). A page retrieve is a summary; treating it as the page is the quiet data-loss bug of this API.

## Create in a Database

```bash
curl -X POST 'https://api.notion.com/v1/pages' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "DATABASE_ID"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Ship the importer"}}]},
      "Status": {"status": {"name": "In Progress"}},
      "Due": {"date": {"start": "2026-08-14"}},
      "external_id": {"rich_text": [{"text": {"content": "recAbc123"}}]}
    },
    "children": []
  }'
```

- On `2025-09-03` the parent is `{"type": "data_source_id", "data_source_id": "…"}` (`data-sources.md`).
- Property keys must match the schema exactly, including case and spaces (SKILL.md Rule 1).
- Properties you omit are left at their default — omission is not the same as clearing (`properties.md`).
- `children` may carry the initial block tree in the same request, which halves the request count on an import. Nesting inside a create is limited to two levels; deeper trees are appended afterwards to the ids the response returns.
- **Before creating a row that mirrors an external record, filter on its `external_id` first.** One extra request per record buys idempotency for reruns (SKILL.md Rule 6).

## Create Under a Page

```bash
curl -X POST 'https://api.notion.com/v1/pages' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "PARENT_PAGE_ID"},
    "properties": {"title": {"title": [{"text": {"content": "Meeting notes"}}]}},
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Agenda"}}]
      }}
    ]
  }'
```

The only property a non-database page has is `title`, and its key is literally `title`. Sending database-style property names here is a `validation_error`.

## Update Properties

```bash
curl -X PATCH 'https://api.notion.com/v1/pages/PAGE_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"status": {"name": "Done"}}}}'
```

- The PATCH merges: named properties are replaced, unnamed ones untouched. There is no partial update *within* a property — sending one item to a `multi_select` or `relation` replaces the whole list. Read, merge, write.
- Read-only types in a payload produce a 400 with no field named: `formula`, `rollup`, `created_time`, `created_by`, `last_edited_time`, `last_edited_by`, `unique_id`.
- Updating a page bumps `last_edited_time`, which is what polling-based sync watches — a no-op write is not free, it is an event (`sync.md`).
- Overwriting one property across many pages is a destructive operation for the Output Gates: state the count first.

## Archive, Trash, Restore

```bash
curl -X PATCH 'https://api.notion.com/v1/pages/PAGE_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"archived": true}'
```

- Newer versions expose the same state as `in_trash`; accept both when reading, and send the one your pinned version documents.
- Archived pages leave query results by default and are restorable by the user from the trash. `"archived": false` restores one through the API.
- Archiving a page archives its children. Archiving a database row does not delete anything permanently — the emptying of the trash does, and that is a user action.
- Archiving is the safe destructive operation in this API. Block deletion and option removal are the unsafe ones (`databases.md`).

## Icons and Covers

```bash
curl -X PATCH 'https://api.notion.com/v1/pages/PAGE_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "icon": {"type": "emoji", "emoji": "🚀"},
    "cover": {"type": "external", "external": {"url": "https://example.com/cover.jpg"}}
  }'
```

External covers must be publicly reachable URLs — Notion fetches them, it does not proxy your auth. Uploaded images: `files.md`.

## Ids and URLs

- A page URL ends in the 32-hex id, usually with the title slugged in front of it: `.../Meeting-notes-abc123…`. Dashes in the id are optional in every request.
- A database URL carries the database id before `?v=`; the part after is a view id and is not addressable (`data-sources.md`).
- Ids are stable across renames and moves. Storing ids rather than titles is why the memory boxes survive a workspace reorganization.
- `id_format` in `config.yaml` decides whether examples and stored notes use the dashed or compact form. It changes nothing functionally; consistency makes grep work.

## Duplicating and Templating

There is no duplicate-page endpoint. Duplication is: retrieve the source page, retrieve its block tree recursively, create the new page with the properties, then append the blocks (`blocks.md`).

- Cost is one request per page plus one per ~100 blocks per level — a 50-block page is 3-4 requests, and a 200-page duplication run belongs in `bulk.md`.
- Unsupported block types come back as `unsupported` and cannot be recreated; state which ones dropped rather than producing a silently incomplete copy.
- A duplicated page does not inherit integration connections reliably (`auth.md`).
- When a duplication pattern gets used more than once, save the block skeleton to `~/Clawic/data/notion-api-integration/artifacts/template-<what>.md` and index it in `## Boxes` — rebuilding a template payload from the UI is an hour nobody budgets twice.
