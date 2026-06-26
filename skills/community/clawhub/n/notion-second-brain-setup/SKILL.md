---
name: second-brain-setup
version: 0.4.0
description: One-shot Notion workspace scaffolder for the second-brain skill. Creates or adopts the "Second Brain" parent page and its child databases (Reading List, Inbox) using the exact Notion MCP tools — no freelance pages.
activation:
  keywords:
    - set up my second brain
    - setup my second brain
    - initialize notion
    - scaffold notion
    - bootstrap notion
    - second brain setup
    - repair second brain
    - fix second brain
  patterns:
    - "set ?up (my )?second brain"
    - "(initialize|scaffold|bootstrap) (my )?(notion|second brain)"
    - "(repair|fix|reset) (my )?second brain"
  tags:
    - notion
    - second-brain
    - setup
    - onboarding
  exclude_keywords:
    - dry-run
  max_context_tokens: 3000
---

# Second Brain Setup

## STRICT RULES — read first

You will execute a **fixed sequence of Notion MCP tool calls**. You are NOT to invent pages, write markdown content, or call any tool not listed in the sequence below.

✅ **The only output of this skill:**
1. One **page** titled exactly `Second Brain` (no body content, no icon, no cover)
2. One **database** titled exactly `Reading List` as a child of that page
3. One **database** titled exactly `Inbox` as a child of that page

❌ **Forbidden — even if your training suggests them:**
- ❌ PARA pages (Projects / Areas / Resources / Archives)
- ❌ "Building a Second Brain" overview, methodology, or wiki content
- ❌ "Book Notes", "Meeting Notes", "Daily Notes", "Quick Links"
- ❌ Any markdown body content on the `Second Brain` parent page
- ❌ Calling `notion-create-pages` to create something that should be a database
- ❌ Adding emojis, covers, or decorative properties anywhere

If you find yourself about to call `notion-create-pages` with a `content` field longer than 0 characters, STOP — you are about to do the wrong thing.

## Tool sequence

Execute in order. Stop and report on first hard failure.

### Step 0 — Find an accessible parent page (PREREQUISITE)

The Notion integration can only create pages under a page it has been shared with. There is no "workspace root" creation path.

Call `notion-search` with:
```json
{"query": "", "query_type": "internal"}
```

This returns every page the integration can see. From the results:

- If you see a page already titled exactly `Second Brain`, save its `page_id` as `SECOND_BRAIN_ID` and skip to Step 2.
- Otherwise, pick any visible page as `INTEGRATION_PARENT_ID`. Prefer one that looks like a top-level workspace page (no parent, or named like `Home`, `Workspace`, `IronClaw`, etc.).
- If the search returns zero results, STOP and reply to the user with exactly:
  > `No pages accessible to the integration. In Notion, create a page (e.g. "IronClaw") and share it with the integration (... → Connections → IronClaw), then run setup again.`

### Step 1 — Create the `Second Brain` parent page

Only run this step if `SECOND_BRAIN_ID` was not found in Step 0.

Call `notion-create-pages` with **exactly this payload — no other fields**:
```json
{
  "pages": [
    {
      "parent": {"type": "page_id", "page_id": "<INTEGRATION_PARENT_ID>"},
      "properties": {"title": "Second Brain"}
    }
  ]
}
```

**Do NOT include any of these fields**, even as empty values: `content`, `icon`, `cover`, `template_id`, `children`, `tags`, `description`. The `pages[0]` object must contain exactly two keys: `parent` and `properties`. If you write any other key, you are violating this skill.

Save the returned `page_id` as `SECOND_BRAIN_ID`.

### Step 2 — Find or adopt `Reading List`

Call `notion-search` with:
```json
{"query": "Reading List", "query_type": "internal"}
```

If a database (not a page) named exactly `Reading List` exists:
- If its parent is already `SECOND_BRAIN_ID`, do nothing — record `READING_LIST_ID` and skip to Step 3.
- If its parent is something else, call `notion-move-pages` to move it under `SECOND_BRAIN_ID`. Record `READING_LIST_ID`.
- Do NOT modify its existing schema, even if it differs from the spec below. Adopt as-is.

If not found, call `notion-create-database` with:
```json
{
  "parent": {"type": "page_id", "page_id": "<SECOND_BRAIN_ID>"},
  "title": [{"type": "text", "text": {"content": "Reading List"}}],
  "properties": {
    "Name": {"title": {}},
    "Type": {"select": {"options": [
      {"name": "Book"}, {"name": "Article"}, {"name": "Podcast"}, {"name": "Video"}
    ]}},
    "Status": {"select": {"options": [
      {"name": "Not started"}, {"name": "In progress"}, {"name": "Done"}
    ]}},
    "Score": {"number": {"format": "number"}},
    "Author": {"rich_text": {}},
    "Link": {"url": {}},
    "Review(Sum up)": {"rich_text": {}},
    "Tags": {"multi_select": {"options": []}}
  }
}
```

Record `READING_LIST_ID` from the response.

### Step 3 — Find or adopt `Inbox`

Same pattern as Step 2. Search → adopt-and-move if exists → otherwise create with:
```json
{
  "parent": {"type": "page_id", "page_id": "<SECOND_BRAIN_ID>"},
  "title": [{"type": "text", "text": {"content": "Inbox"}}],
  "properties": {
    "Note": {"title": {}},
    "Type": {"select": {"options": [
      {"name": "Thought"}, {"name": "Task"}, {"name": "Resource"}, {"name": "Reference"}
    ]}},
    "Processed": {"checkbox": {}},
    "Date": {"date": {}}
  }
}
```

### Step 4 — Report

Reply to the user with exactly this format (filling URLs from tool responses):

```
Second Brain ready ✓
• Second Brain page: <url>
• Reading List (created|adopted|moved): <url>
• Inbox (created|adopted|moved): <url>

If captures don't work, make sure the IronClaw integration is connected to the Second Brain page (… → Connections → IronClaw). Sharing the parent cascades to children.
```

## MCP call rules

- **Never pass `null` for any field.** Omit the field. Empty string is also wrong for most fields — omit instead.
- **Never include `template_id` or `cover`** unless you have real values. These are the most common null-pass mistakes.
- **Date fields** are `YYYY-MM-DD` strings only.
- **`notion-search` rate limit is 30/min** — do not search more than necessary. One search per database name in this skill is enough.
- **If a tool call fails with `-32602`**, strip every field that is not strictly required by the tool's documented schema and retry once. Do not retry the same payload.
- **Database vs data source:** `notion-create-database` returns a `database_id`. The corresponding `data_source_id` (for queries later) appears in the response under the data sources array. Save both if returned.

## What not to do

- Do not call `notion-create-pages` to create `Reading List` or `Inbox` — they are databases, not pages. Use `notion-create-database`.
- Do not write any explanatory or methodological content into Notion. The user already knows what a second brain is.
- Do not search for `Reading List` or `Inbox` more than once each.
- Do not delete, rename, or restructure existing data. Only add what's missing.
- Do not run any captures during setup. Stop after Step 4's report.
