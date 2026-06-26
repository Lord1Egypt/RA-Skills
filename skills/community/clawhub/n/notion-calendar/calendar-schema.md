# Calendar Database Schema

Calendar-like workflows work best when the target database has these verified fields:

| Field | Type | Why it matters |
|-------|------|----------------|
| Title | `title` | Human-readable event or task name |
| Date | `date` | Drives calendar placement |
| Status | `status` or `select` | Draft, Scheduled, Done, Cancelled |
| Owner | `people` or `rich_text` | Who owns the item |
| Notes | `rich_text` | Context without opening the page |

## Discovery Workflow

1. Retrieve the database container by `database_id`.
2. Read its child `data_sources`.
3. Retrieve the chosen `data_source_id`.
4. Confirm the actual property names before writing.

## Date Semantics

- Single-day items: use `start` only.
- Timed items: use `start` with timezone-aware timestamp.
- Multi-day items: use both `start` and `end`.
- All-day items: use date-only values and confirm no hidden timezone expectation.

## Safe Naming Pattern

If multiple date fields exist, prefer explicit names such as `Publish Date`, `Meeting Time`, or `Launch Window` over a generic `Date`.
