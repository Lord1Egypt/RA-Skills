# Databases and Schemas

Creating, reading and changing the container your rows live in. Endpoints below use the `2022-06-28` shape; on `2025-09-03` the same calls address a data source (`data-sources.md`).

**Contents:** [Read the Schema First](#read-the-schema-first) · [Query](#query) · [Create a Database](#create-a-database) · [Property Definition Shapes](#property-definition-shapes) · [Changing a Schema](#changing-a-schema) · [Renames, Ids, and Why Code Breaks](#renames-ids-and-why-code-breaks) · [Relations and Rollups](#relations-and-rollups) · [Deleting Things](#deleting-things) · [Finding Databases](#finding-databases)

**Before writing to any database**, open its `schemas/<data-source>.md` box if `## Boxes` in `~/Clawic/data/notion-api-integration/memory.md` names one. If it does not exist, retrieve the schema and create it — that is the work, not overhead.

## Read the Schema First

```bash
curl 'https://api.notion.com/v1/databases/DATABASE_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

The response's `properties` object is keyed by **property name**, and each value carries `id` and `type`. Both matter: names are what you send in most payloads, ids are what survive a rename. Copy select/status option names verbatim — they are case-sensitive values your filters will compare against.

## Query

```bash
curl -X POST 'https://api.notion.com/v1/databases/DATABASE_ID/query' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "status": {"equals": "Done"}},
    "sorts": [{"property": "Due", "direction": "ascending"}],
    "page_size": 100
  }'
```

- No filter returns everything, paginated — on a 4,000-row source that is 40 requests (SKILL.md Rule 4). Filter server-side whenever the API can express it.
- Filter grammar, compound shapes and the type-matching rule: `filters.md`. Cursor loop: `pagination.md`.
- The query returns page objects, which means relation/rollup/people values are capped at 25 entries per row (`properties.md`).

## Create a Database

```bash
curl -X POST 'https://api.notion.com/v1/databases' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"type": "page_id", "page_id": "PARENT_PAGE_ID"},
    "title": [{"type": "text", "text": {"content": "Tasks"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"status": {}},
      "Due": {"date": {}},
      "external_id": {"rich_text": {}}
    }
  }'
```

- The parent must be a page, and that page must be inside the connected subtree (`auth.md`).
- Exactly one `title` property, always. Its name is yours to choose; `Name` is the convention and `title` is its id.
- `{"status": {}}` creates the property with Notion's default groups; option sets for `status` are not fully authorable through the API in the way `select` is, so verify the resulting groups before writing values against them.
- Add `external_id` at creation on anything that mirrors another system. Retrofitting it means a full backfill (`bulk.md`).

## Property Definition Shapes

Definitions (in a database payload) are not values (in a page payload). Values are in `properties.md`.

| Type | Definition |
|---|---|
| title | `{"title": {}}` |
| rich_text | `{"rich_text": {}}` |
| number | `{"number": {"format": "number"}}` — also `dollar`, `euro`, `percent` |
| select | `{"select": {"options": [{"name": "High", "color": "red"}]}}` |
| multi_select | `{"multi_select": {"options": [...]}}` |
| status | `{"status": {}}` |
| date · checkbox · url · email · phone_number · people · files | `{"<type>": {}}` |
| relation | `{"relation": {"database_id": "…", "type": "dual_property", "dual_property": {}}}` |
| rollup | `{"rollup": {"relation_property_name": "Company", "rollup_property_name": "Revenue", "function": "sum"}}` |
| formula | `{"formula": {"expression": "prop(\"A\") + 1"}}` |
| unique_id | `{"unique_id": {"prefix": "TASK"}}` |

## Changing a Schema

```bash
curl -X PATCH 'https://api.notion.com/v1/databases/DATABASE_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Priority": {"select": {"options": [{"name": "P0", "color": "red"}]}}}}'
```

- The PATCH is a merge over the properties you name; untouched properties stay. It is not a replace, which is why sending a full schema you built from a stale read is how options get lost.
- **Sending an option list replaces that property's option list.** Any option missing from your payload is removed from the schema and stripped from every page that had it — no confirmation, no undo, no record of which pages changed. Read the current options, add to them, send the union.
- Rename a property: `{"properties": {"Old Name": {"name": "New Name"}}}`. Delete one: `{"properties": {"Old Name": null}}` — and deleting a property deletes its values everywhere.
- Under `write_mode: confirm-writes`, every schema change ships with the count of rows that hold a value for the affected property, obtained by a query before the PATCH.

## Renames, Ids, and Why Code Breaks

A UI rename keeps the property **id** and changes the **name**. Payloads keyed by name break; payloads keyed by id do not. That asymmetry explains most "it worked last month" reports.

- Store both in the schema box. When a `validation_error` says a property does not exist, look up its id in the box and check whether that id is still present under a different name — that distinguishes a rename from a deletion in one call.
- Property *ids* are URL-encoded strings (`%7BdX`), not UUIDs. They look like junk and are stable; keep them verbatim.
- After any confirmed rename, update `schemas/<data-source>.md` in the same turn and note it in `## Gotchas` if existing code or saved filter payloads referenced the old name.

## Relations and Rollups

- A **dual property** relation creates the mirror property on the target automatically; a single property relation does not. Dual is the default worth wanting — without the mirror, "which tasks does this company have" needs a full scan.
- The target of a relation is a database (a data source on `2025-09-03`). Changing the target is a schema change that drops existing links.
- Rollups are computed by Notion and **read-only through the API**. Sending one in a page payload is a 400 with no field named.
- A rollup reads through exactly one relation. Anything needing a second hop or a condition the rollup functions do not offer gets computed in code and written to a plain `number` (SKILL.md Data Model Defaults).
- Rollup and formula values can lag immediately after a write. Do not read one back in the same loop iteration you wrote its input.

## Deleting Things

- A database is archived like a page: `PATCH /v1/pages/{database_page_id}` is not it — archive the database via its own PATCH with `"archived": true`. It goes to the trash, restorable by the user.
- Deleting a property or an option is not restorable and takes the data with it (above).
- Anything listed in `readonly_targets` in `config.yaml` is never modified, whatever the request.

## Finding Databases

```bash
curl -X POST 'https://api.notion.com/v1/search' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"value": "database", "property": "object"}, "page_size": 100}'
```

Returns only databases shared with the integration, subject to index lag (`search.md`). Use it once to discover, then work from stored ids.

**After any schema read or change**, write the property table — names, ids, types, writable, option lists, relation targets — to `~/Clawic/data/notion-api-integration/schemas/<data-source>.md`, with the retrieval date and the API version, and add its line to `## Boxes` in the same turn. Update `### Data Sources` in `memory.md` with the row count and its date. This box is what stops the next session from paying for the same `validation_error`.
