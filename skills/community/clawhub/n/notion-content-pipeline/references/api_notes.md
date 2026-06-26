# Notion API Notes

## Critical constraints

- **Notion API version:** `2022-06-28` — use this. The `2025-09-03` version has breaking
  changes to `data_sources` and is not backward compatible.
- **Block limit per request:** 100 blocks max when appending children. Batch in chunks of 100.
- **Rich text length limit:** 2000 chars per rich_text object. Chunk long content to 1900.
- **Rate limits:** ~3 requests/second. Add `time.sleep(0.3)` between batch calls.

## Overwrite pattern

Notion doesn't support replacing all blocks in a page. The correct "overwrite" pattern is:
1. Archive the old page (`PATCH /pages/{id}` with `{"archived": true}`)
2. Create a fresh page as a sibling under the same parent
3. Update the sync map with the new page ID

Do **not** try to delete individual blocks and re-push — too fragile.

## Block types supported

| Markdown     | Notion block type       |
|-------------|-------------------------|
| `# Heading` | `heading_1`             |
| `## Heading`| `heading_2`             |
| `### Heading`| `heading_3`            |
| `> Quote`   | `quote`                 |
| `- Item`    | `bulleted_list_item`    |
| `1. Item`   | `numbered_list_item`    |
| `` ```code ``` `` | `code`            |
| `---`       | `divider`               |
| paragraph   | `paragraph`             |

## Database property types

| Type     | API schema                              |
|----------|-----------------------------------------|
| Title    | `{"title": {}}`                         |
| Text     | `{"rich_text": {}}`                     |
| Select   | `{"select": {"options": [...]}}`        |
| URL      | `{"url": {}}`                           |
| Date     | `{"date": {}}`                          |
| Number   | `{"number": {}}`                        |
| Checkbox | `{"checkbox": {}}`                      |

## Integration setup

1. Go to https://www.notion.so/my-integrations
2. Create integration → copy the token (starts with `secret_`)
3. Open the parent page in Notion → click "..." → "Add connections" → select your integration
4. The integration must be connected to the page/DB to read or write it

## Getting a page ID

From the URL: `https://notion.so/My-Page-{ID-with-dashes}`  
Or: `https://notion.so/{workspace}/{32-char-id}`  
The ID is the last 32 chars (with or without hyphens — both work in the API).
