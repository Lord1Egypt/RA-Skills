# Comments and Discussions

Comments are a separate object with their own capabilities, and the API sees less of them than the UI does.

## Read

```bash
curl 'https://api.notion.com/v1/comments?block_id=PAGE_OR_BLOCK_ID&page_size=100' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

- Requires the **read comments** capability; without it the call fails even though the page is shared (`auth.md`).
- `block_id` accepts a page id (page-level comments) or a block id (comments anchored to that block).
- Paginated at 100 like everything else (`pagination.md`).
- Each comment carries `discussion_id`, `created_by`, `created_time` and `rich_text`.

## Create

```bash
# New page-level discussion
curl -X POST 'https://api.notion.com/v1/comments' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "PAGE_ID"},
    "rich_text": [{"type": "text", "text": {"content": "Imported 4,180 rows; 20 failed."}}]
  }'
```

```bash
# Reply into an existing discussion
curl -X POST 'https://api.notion.com/v1/comments' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "discussion_id": "DISCUSSION_ID",
    "rich_text": [{"type": "text", "text": {"content": "Retried, all clear."}}]
  }'
```

Send `parent` **or** `discussion_id`, never both. A reply needs the `discussion_id` from a prior read — there is no "reply to comment id".

## What the API Cannot Do With Comments

| Wanted | Reality |
|---|---|
| Edit a comment | No update endpoint |
| Delete a comment | No delete endpoint — a comment posted by an integration stays until a human removes it |
| Resolve a discussion | Not exposed; resolution is a UI action |
| Comment on an inline text range | Anchoring to arbitrary text is a UI feature; the API anchors to a block or a page |
| See comments on unshared pages | Same access model as everything else — 404 |

Because there is no delete, an automation that comments on every change becomes noise a human has to clean by hand. Comment on exceptions, not on successes.

## Useful Patterns

- **Job report**: one page-level comment at the end of an import — counts, failures, duration. It puts the result where the affected people already look, unlike a log file.
- **Exception flag**: comment only on the rows that failed validation, mentioning the owner with a user mention (`users.md`) so they are notified.
- **Human handoff**: a comment carrying the id of the artifact you wrote, so the runbook and the workspace point at each other.

Rate limit applies here too: commenting on 300 rows is 300 requests, ≈100 seconds at 3 req/s, plus whatever else is running on the same token (SKILL.md Rule 5).

Comments are content, not data to mirror. Nothing in this file produces a box of its own — a comment worth keeping is quoted inside the artifact or run record that explains it (`bulk.md`).
