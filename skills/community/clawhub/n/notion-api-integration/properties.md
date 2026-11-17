# Property Values — Write Shapes, Read Shapes, Traps

Every property type has a different write shape, a different read shape, and its own way of failing. Definitions (what a schema declares) are in `databases.md`; this file is values.

**Contents:** [Write Shapes](#write-shapes) · [Read-Only Types](#read-only-types) · [Clearing a Value](#clearing-a-value) · [The 25-Entry Truncation](#the-25-entry-truncation) · [Reading a Single Property](#reading-a-single-property) · [Rich Text Values](#rich-text-values) · [Dates and Time Zones](#dates-and-time-zones) · [Type-Specific Traps](#type-specific-traps)

## Write Shapes

Keys are property **names**, exactly as the schema box records them.

| Type | Write payload |
|---|---|
| title | `{"Name": {"title": [{"text": {"content": "Page title"}}]}}` |
| rich_text | `{"Notes": {"rich_text": [{"text": {"content": "Text"}}]}}` |
| number | `{"Price": {"number": 99.99}}` — bare number, not a string |
| select | `{"Priority": {"select": {"name": "High"}}}` |
| multi_select | `{"Tags": {"multi_select": [{"name": "ops"}, {"name": "urgent"}]}}` |
| status | `{"Status": {"status": {"name": "Done"}}}` |
| date | `{"Due": {"date": {"start": "2026-12-31"}}}` · range: add `"end"` · datetime: ISO 8601 with offset |
| checkbox | `{"Done": {"checkbox": true}}` |
| url · email · phone_number | `{"Link": {"url": "https://example.com"}}` — plain string, or `null` |
| people | `{"Assignee": {"people": [{"object": "user", "id": "USER_ID"}]}}` — ids, never names |
| files | `{"Attachments": {"files": [{"name": "doc.pdf", "type": "external", "external": {"url": "https://…"}}]}}` |
| relation | `{"Company": {"relation": [{"id": "PAGE_ID"}]}}` — page ids in the target source |

Two rules cover most rejections: **rich-text-family types take an array of rich text objects, everything else takes a scalar or a `{"name": …}` object**, and **a write replaces the whole property** — one item in a `multi_select` or `relation` payload wipes the others.

## Read-Only Types

Sending any of these inside `properties` returns a 400 that names no field, which is why it is hard to spot in a large payload:

`formula` · `rollup` · `created_time` · `created_by` · `last_edited_time` · `last_edited_by` · `unique_id`

They are computed or system-owned. To make one of them writable, model the value yourself in a plain property (SKILL.md Data Model Defaults).

## Clearing a Value

Clearing is explicit and type-specific. Omitting a property from a PATCH leaves it untouched — it does not clear it.

```json
{"Due": {"date": null}}
{"Tags": {"multi_select": []}}
{"Notes": {"rich_text": []}}
{"Link": {"url": null}}
{"Company": {"relation": []}}
{"Priority": {"select": null}}
```

Scalars take `null`, list types take `[]`. Sending `[]` to a scalar or `null` to a list is a `validation_error`.

## The 25-Entry Truncation

Inside a page object — from a retrieve *or* from a database query — `relation`, `rollup` and `people` values return at most 25 entries. There is no flag in the response saying "there are more"; the array simply ends.

Consequences worth designing around:

- A rollup computed over 40 related rows returns the correct aggregate, but the relation array under it is short. Trust the aggregate, not the array.
- Migration code that copies relations page-by-page silently drops every link past the 25th on the biggest, most important records.
- "The UI shows 60, the API shows 25" is never a permission problem.

## Reading a Single Property

```bash
curl 'https://api.notion.com/v1/pages/PAGE_ID/properties/PROPERTY_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

- `PROPERTY_ID` is the URL-encoded id from the schema, not the name.
- The response is itself paginated for list-shaped properties: loop `has_more` (`pagination.md`).
- Budget it: one extra request per page per truncated property. A 4,000-row export that needs full relations is 40 query requests plus up to 4,000 property requests — ≈23 minutes at 3 req/s, which is a plan, not a surprise (`bulk.md`).
- Formula and rollup results come back here with their computed type, which is the reliable way to read them.

## Rich Text Values

```json
{
  "type": "text",
  "text": {"content": "Styled", "link": {"url": "https://example.com"}},
  "annotations": {"bold": true, "italic": false, "strikethrough": false,
                  "underline": false, "code": false, "color": "red"}
}
```

- **2,000 characters per rich text object, 100 objects per array.** Longer content is chunked deliberately or moved into page blocks — a 20,000-character string is rejected, and an SDK that splits it for you chooses the split points, not you.
- Mentions (`"type": "mention"`) reference a user, page, database or date and render as a live link. They are the only way to make a property value point at another object without a relation.
- Equations (`"type": "equation"`) carry a LaTeX `expression` with its own, shorter length cap.
- Colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`, each with a `_background` variant.
- Reading rich text: concatenate `plain_text` across the array. Reading only `[0].plain_text` is how half a paragraph goes missing whenever a user bolded a word.

## Dates and Time Zones

- Date-only: `"2026-08-14"`. Datetime: `"2026-08-14T14:00:00.000+02:00"` or a `Z` offset.
- `time_zone` is a separate field and only meaningful with a datetime; setting it alongside an offset that disagrees is a silent inconsistency in the UI.
- Ranges are `start` + `end` on one value, not two properties.
- Notion stores what you send. A workspace whose dates were entered by hand in local time and one whose dates came from an API in UTC will disagree by hours forever — decide once, record it in `## Gotchas`.

## Type-Specific Traps

| Type | Trap |
|---|---|
| select / multi_select | Writing a value that is not in the option list **creates the option**. A typo becomes a permanent schema entry that filters will never match |
| status | Option sets are group-backed and not freely authorable through the API; write only names the schema already has |
| people | Takes user ids. A name or email in the array is a `validation_error`; resolve via `/v1/users` first (`users.md`) |
| relation | Ids must be pages in the target source. A valid page id from elsewhere fails, and the message names the property, not the reason |
| files | External URLs must be publicly reachable; uploaded files use the file-upload reference instead (`files.md`) |
| number | A string `"99.99"` is rejected; a currency symbol in the value is rejected. Format lives in the schema, not the value |
| checkbox | Has no null state — absent means `false`, so "not yet decided" needs a select, not a checkbox |
| title | Every database row has exactly one, and an empty title is legal and produces rows nobody can find in the UI |
| unique_id | Read-only and workspace-assigned; it is not an external key you can set (SKILL.md Data Model Defaults) |

**When a property write fails and re-reading the schema explains why**, update `~/Clawic/data/notion-api-integration/schemas/<data-source>.md` in the same turn — the corrected name, the real type, the current option list — and note the surprise in `## Gotchas` of `memory.md` if it will bite again.
