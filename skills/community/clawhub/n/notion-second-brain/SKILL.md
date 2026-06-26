---
name: second-brain
version: 0.4.0
description: Files messages from Telegram into the user's Notion second brain — books, fleeting notes, tasks — consistently and without clarifying questions.
activation:
  keywords:
    - notion
    - book
    - finished reading
    - just read
    - highlights
    - takeaways
    - quote
    - note
    - remember
    - todo
    - inbox
    - second brain
  patterns:
    - "(just |finally )?finished (reading )?[A-Z]"
    - "(reading|started) [A-Z][a-zA-Z' ]+ by"
    - "remind(er)? (me )?to"
    - "remember to"
    - "save (this|that) (to|in) notion"
    - "add (this|that) to (my )?(inbox|notes|notion)"
  tags:
    - notion
    - second-brain
    - notes
    - books
    - productivity
    - capture
  exclude_keywords:
    - dry-run
  max_context_tokens: 2500
---

# Second Brain

You file the user's incoming messages into their Notion workspace. The user sends short, unstructured messages from Telegram; you classify them and write them to the right database with the right shape. Consistency is the product — the user must be able to trust that "save this" always lands in the same place, tagged the same way.

## Workspace contract

This skill assumes a **`Second Brain` parent page exists in the user's Notion workspace**, with the expected databases living as children of it. The skill never creates this structure — that's the job of the separate `second-brain-setup` skill.

**On every capture, before writing:**

1. Search Notion for a page titled `Second Brain` (exact match, top-level).
2. If not found, do **not** create databases or write anywhere. Reply to the user with exactly:
   > `No "Second Brain" workspace found in your Notion. Run setup first by messaging "set up my second brain".`
   Then stop.
3. If found, look for the target database (`Reading List`, `Inbox`, etc.) as a child of that page. If the specific database is missing, reply:
   > `Found Second Brain but the "<DB name>" database is missing. Run "set up my second brain" to repair the structure.`

Once the parent + target DB are confirmed, proceed with the capture. Cache the parent page ID and DB IDs in working memory for the rest of the turn so you don't re-search per write.

## Databases

The skill writes to two databases under the `Second Brain` parent. Do not invent new databases — if something doesn't fit, route to **Inbox**.

### Reading List (the user's books database)
| Field | Type | Notes |
|---|---|---|
| Name | Title | Book name, title-cased |
| Type | Select | Always `Book` for book entries |
| Status | Select | `In progress` (currently reading), `Done` (finished), `Not started` (want to read) |
| Score | Number/rating | 1–5. Only set if the user explicitly gave a rating ("loved it", "5 stars", "would recommend"). Never invent a score. |
| Author | Text | Full name if known. Omit if unclear — do not guess. |
| Link | URL | Only if the user pasted a URL (Goodreads, Amazon, etc.) |
| Review(Sum up) | Text | Takeaways and quotes go HERE, not as page body. Use this format: `**Takeaways:**\n- bullet\n- bullet\n\n**Quotes:**\n> quote 1\n> quote 2` |
| Tags | Multi-select | Must come from existing tag options — never create new ones |

Status mapping from natural language:
- "finished", "done", "just read" → `Done`
- "reading", "currently reading", "started" → `In progress`
- "want to read", "added to list", "on my list" → `Not started`

### Inbox
| Field | Type | Notes |
|---|---|---|
| Note | Title | The raw message, lightly cleaned |
| Type | Select | `Thought` / `Task` / `Resource` / `Reference` |
| Processed | Checkbox | Always `false` on capture |
| Date | Date | Today |

## Routing rules

Apply in order. First match wins.

1. **Mentions a book** (title + author, "finished X", "reading X by Y", highlights/quotes from a named book) → **Reading List**
2. **Action item** ("remind me to", "remember to", "todo:", imperative verb directed at future self) → **Inbox**, Type=`Task`
3. **URL or article reference** (contains http/https, "read this", "check out") → **Inbox**, Type=`Resource`
4. **Reference material** (definition, fact, quote without a book context) → **Inbox**, Type=`Reference`
5. **Everything else** → **Inbox**, Type=`Thought`

## Behaviour

- **Never ask clarifying questions for captures.** Make a best guess and tell the user what you did. The user can correct after.
- **Always check for duplicates before creating.** For Books, query by Title (case-insensitive); if found, append to existing entry instead of creating a new one.
- **Tags must come from existing options.** Query the multi-select options first. If nothing fits, pick the closest match — do not silently create new tags.
- **Confirmations are short.** One line, with the destination and a checkmark. Examples:
  - `Saved to Reading List — Atomic Habits ✓`
  - `Filed to Inbox (Task) — call dentist ✓`
  - `Updated Reading List — added 2 quotes to Deep Work ✓`
- **If a write fails, say so plainly** and include the Notion error. Do not retry silently.

## Book capture details

When the message mentions finishing or reading a book:

1. Search Reading List by `Name` (case-insensitive). If no exact match, try fuzzy on first 3 significant words. Always set `Type=Book` in the filter to avoid colliding with non-book entries.
2. If found:
   - **Append** to `Review(Sum up)` — read the existing field, add new takeaways/quotes underneath, write the combined value back. Never overwrite.
   - Update `Status` only if the user signaled a transition ("finished" → `Done`, "started" → `In progress`).
   - Set `Score` only if the user explicitly rates this time.
3. If not found, create with:
   - `Type` = `Book` (always)
   - `Status` per the mapping above
   - `Author` only if mentioned
   - `Review(Sum up)` populated only if the user gave actual content. If the message is just "finished X", leave it blank — do not fabricate takeaways.
   - `Score` only if explicitly rated
   - `Link` only if a URL was pasted
4. Tags: pick from existing options based on subject matter. Cap at 3 tags. If no existing tag fits, leave Tags empty.

### Review(Sum up) format

Always write this field as markdown with these sections (omit either if empty):

```
**Takeaways:**
- first takeaway in user's words
- second takeaway

**Quotes:**
> "first quote"
> "second quote"
```

When appending, preserve the existing structure — add new bullets under `**Takeaways:**` and new lines under `**Quotes:**`, don't create duplicate section headers.

## Notion MCP tool sequence

Use these specific tools — do not invent or substitute:

- **`notion-search`** — find the `Second Brain` page and the target database. One search per name max (rate limit: 30/min).
- **`notion-fetch`** — fetch the database to get its `data_source_id` (look for `collection://...` in the response). You need `data_source_id`, not `database_id`, to query rows.
- **`notion-query-data-sources`** (or `notion-query-database-view`) — search for an existing book by `Name`. Use the `data_source_id` from `notion-fetch`.
- **`notion-create-pages`** — create a new row in Reading List or Inbox.

  ### Payload shape — non-negotiable

  Every call has exactly **two top-level keys**: `pages` (array). Nothing else at the top level — **`parent` is NOT a top-level key**, it lives inside each page object.

  ```
  {
    "pages": [
      { "parent": {...}, "properties": {...} }   ← parent goes HERE, inside each page
    ]
  }
  ```

  Each page object has exactly two keys: `parent` and `properties`. No `content`, `icon`, `cover`, `template_id`, `userDefined:*`, `date:*:*`, or any other invented keys. If the schema doesn't list it, do not send it.

  ### Property value rules

  | Notion type | What to send | What NEVER to send |
  |---|---|---|
  | Title (e.g. `Name`, `Note`) | plain string | object, array |
  | Select (e.g. `Type`, `Status`) | exact option string, e.g. `"Resource"` | `"__RESOURCE__"`, lowercase, abbreviations |
  | Number / Score | bare number, e.g. `5` | `"5"`, `{value: 5}` |
  | URL (e.g. `Link`) | plain URL string | object |
  | Checkbox (e.g. `Processed`) | `true` or `false` only | `"YES"`, `"NO"`, `"__NO__"`, `0`, `1`, `null` |
  | Date | `"YYYY-MM-DD"` string, e.g. `"2026-05-14"` | `null`, datetime, year-month-only, `{start, end, is_datetime}` objects, `date:Date:start` keys |
  | Rich text (`Review(Sum up)`, `Author`) | plain string | array of segments |
  | Multi-select (`Tags`) | array of exact existing option strings | new tags not in the database, single string |

  ### Worked examples — copy these shapes exactly

  **Inbox · Resource (URL capture):**
  ```json
  {
    "pages": [{
      "parent": {"type": "data_source_id", "data_source_id": "<inbox_data_source_id>"},
      "properties": {
        "Note": "https://paulgraham.com/greatwork.html",
        "Type": "Resource",
        "Processed": false,
        "Date": "2026-05-14"
      }
    }]
  }
  ```

  **Inbox · Task:**
  ```json
  {
    "pages": [{
      "parent": {"type": "data_source_id", "data_source_id": "<inbox_data_source_id>"},
      "properties": {
        "Note": "refactor the auth module before Friday",
        "Type": "Task",
        "Processed": false,
        "Date": "2026-05-14"
      }
    }]
  }
  ```

  **Inbox · Thought:**
  ```json
  {
    "pages": [{
      "parent": {"type": "data_source_id", "data_source_id": "<inbox_data_source_id>"},
      "properties": {
        "Note": "cities behave like organisms",
        "Type": "Thought",
        "Processed": false,
        "Date": "2026-05-14"
      }
    }]
  }
  ```

  **Inbox · Reference:**
  ```json
  {
    "pages": [{
      "parent": {"type": "data_source_id", "data_source_id": "<inbox_data_source_id>"},
      "properties": {
        "Note": "speed of light ≈ 3 × 10^8 m/s",
        "Type": "Reference",
        "Processed": false,
        "Date": "2026-05-14"
      }
    }]
  }
  ```

  **Reading List · Book (finished, with score):**
  ```json
  {
    "pages": [{
      "parent": {"type": "data_source_id", "data_source_id": "<reading_list_data_source_id>"},
      "properties": {
        "Name": "Sapiens",
        "Type": "Book",
        "Status": "Done",
        "Score": 5,
        "Author": "Yuval Noah Harari",
        "Review(Sum up)": "Great take on the cognitive revolution."
      }
    }]
  }
  ```

  **Date handling:** Always use **today's date** when capturing — query the system for today's date if needed. Never invent a date. If you cannot determine the date, **omit `Date` entirely** rather than guessing.

  **Common failures to never repeat:**
  - ❌ `parent` at the top level (sibling of `pages`) instead of inside each page object
  - ❌ `Processed: "NO"` / `"__NO__"` / `0` — use boolean `false`
  - ❌ `Date: null` or `date:Date:end: null` — omit instead
  - ❌ Inventing properties like `userDefined:URL` or `date:Date:is_datetime` — if it's not in the schema table above, do not send it
  - ❌ Wrapping a single page as a bare object instead of `[ {...} ]`
- **`notion-update-page`** — append to `Review(Sum up)` or update `Status`/`Score` on an existing book.

## Notion MCP call rules

Strict schema validation — common LLM mistakes cause `-32602` errors. Follow on every call:

- **Never pass `null` for any field.** Omit it from the arguments object entirely. Do not include the key with `null`, `""`, or `{}` as a placeholder.
  - ❌ `{"filters": {"created_date_range": {"start_date": null, "end_date": null}}}`
  - ❌ `{"template_id": null, "cover": null}`
  - ✅ Omit those keys
- **Date fields require `YYYY-MM-DD` strings.** No timestamps, no `null`. If you don't have a real date, omit.
- **For `notion-search`**, `{"query": "..."}` is enough. Only add filters with concrete values.
- **If a tool call fails with `-32602`**, strip every offending field and retry **once**. Do not retry the same payload.
- **Rate limit: 30 searches/min, 180 total ops/min.** Reuse cached IDs from earlier in the same turn rather than re-searching.

## Integration access

The Notion integration must be **shared with the `Second Brain` parent page** (Notion: page → `…` menu → Connections → add the integration). Sharing the parent cascades access to all child databases — the user only needs to do it once.

If the parent search returns empty but the user insists they created `Second Brain`, the most likely cause is the integration isn't connected. Tell them plainly:

> `Found no "Second Brain" page — either it doesn't exist yet, or the IronClaw integration isn't connected to it. In Notion: open Second Brain → Connections → add IronClaw.`

Do not silently create a duplicate workspace to work around this.

## What not to do

- Do not summarize back the user's full message — they sent it, they remember it.
- Do not fabricate takeaways or quotes the user didn't provide.
- Do not create new databases, new properties, or new tag options without explicit instruction.
- Do not file the same message into multiple databases.
- Do not mark anything `Processed = true` on capture — that's the triage routine's job.
