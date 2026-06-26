# Notion Brain — MCP Commands

Use native Notion MCP tools — NOT `mcporter`. The connected tools are:
- `notion-search` — find existing pages
- `notion-create-pages` — create pages under a parent page or data source
- `notion-update-page` — update properties, replace content, or append content
- `notion-fetch` — read a page's full content and schema

Content uses **Notion-flavored Markdown**, not JSON block arrays.

---

## 1) Search for an existing page

Use before creating when the topic may already exist.

```json
notion-search({
  "query": "Decision Memo — Notion Routing Skill",
  "page_size": 5,
  "max_highlight_length": 100
})
```

To search within a specific parent page:

```json
notion-search({
  "query": "weekly rollup",
  "page_url": "YOUR_KNOWLEDGE_HUB_PAGE_ID"
})
```

---

## 2) Create a page under 🧠 Knowledge Hub

Parent page ID: `YOUR_KNOWLEDGE_HUB_PAGE_ID`

```json
notion-create-pages({
  "parent": { "page_id": "YOUR_KNOWLEDGE_HUB_PAGE_ID" },
  "pages": [{
    "properties": { "title": "Research Summary — MCP Routing Patterns — 2026-03-22" },
    "content": "Summary: A durable synthesis of Notion routing and write patterns.\n\n## Key findings\n\n- Finding one\n- Finding two\n\n## Recommendations\n\n- Recommendation here"
  }]
})
```

Use for: research summaries, decision memos, security audits, weekly rollups, contact notes, strategic docs.

---

## 3) Create a page under 💼 Work Hub

Parent page ID: `YOUR_WORK_HUB_PAGE_ID`

```json
notion-create-pages({
  "parent": { "page_id": "YOUR_WORK_HUB_PAGE_ID" },
  "pages": [{
    "properties": { "title": "Meeting Prep — QBR — 2026-03-22" },
    "content": "Purpose: Walk in with the right context, decisions, and talking points.\n\n## Talking points\n\n- Point one\n- Point two"
  }]
})
```

Use for: project plans, project status, meeting prep, work execution artifacts.

---

## 4) Create a page under ✍️ Content Hub

Parent page ID: `YOUR_CONTENT_HUB_PAGE_ID`

```json
notion-create-pages({
  "parent": { "page_id": "YOUR_CONTENT_HUB_PAGE_ID" },
  "pages": [{
    "properties": { "title": "Draft — Why Teams Need Better AI Operating Systems" },
    "content": "Thesis: Most AI efforts fail because they are tool-first instead of operating-system-first.\n\n## Working outline\n\n- Section one\n- Section two"
  }]
})
```

Use for: article drafts, outlines, content experiments.

---

## 5) Create a page under 💰 Finance Hub

Parent page ID: `YOUR_FINANCE_HUB_PAGE_ID`

```json
notion-create-pages({
  "parent": { "page_id": "YOUR_FINANCE_HUB_PAGE_ID" },
  "pages": [{
    "properties": { "title": "Financial Snapshot — 2026-03" },
    "content": "Summary: Cash position improved and risk remains concentrated in one sector.\n\n## Highlights\n\n- Highlight one\n- Highlight two"
  }]
})
```

Use for: durable financial summaries, not transaction-by-transaction logging.

---

## 6) Create a quick capture in 📥 Inbox DB

Data source ID: `YOUR_INBOX_DB_ID`
Title property: `Name` (example)

Available properties:
- `Name` (title) — required
- `Area` — example values: 💼 Work, 💰 Finance, 💪 Health, 🏡 Home, 🧠 Knowledge, 📝 Personal
- `Source` — example values: Owner, Agent, Email, Meeting, Idea
- `Priority` — one of: 🔴 Urgent, 🟡 Soon, 🟢 Someday
- `Status` — one of: New, Processing, Done, Archived (default: New)
- `Notes` — free text
- `Date Added` — use expanded date format

```json
notion-create-pages({
  "parent": { "data_source_id": "YOUR_INBOX_DB_ID" },
  "pages": [{
    "properties": {
      "Name": "Capture — Pricing idea — 2026-03-22",
      "Area": "💼 Work",
      "Source": "Agent",
      "Priority": "🟡 Soon",
      "Status": "New",
      "date:Date Added:start": "2026-03-22",
      "date:Date Added:is_datetime": 0
    }
  }]
})
```

Use `data_source_id` (not `database_id`) for the Inbox DB. Adjust property names and select values to match your schema.

---

## 7) Append content to an existing page

Use when the right move is extending a page rather than creating a duplicate.
First fetch the page to see existing content:

```json
notion-fetch({ "id": "REPLACE_WITH_PAGE_ID" })
```

Then append via update_content or replace_content:

```json
notion-update-page({
  "page_id": "REPLACE_WITH_PAGE_ID",
  "command": "update_content",
  "content_updates": [{
    "old_str": "## Recommendations\n\n- Existing recommendation",
    "new_str": "## Recommendations\n\n- Existing recommendation\n- New recommendation added"
  }]
})
```

Or to fully replace content (use with care):

```json
notion-update-page({
  "page_id": "REPLACE_WITH_PAGE_ID",
  "command": "replace_content",
  "new_str": "## Updated Section\n\nFresh content replaces everything."
})
```

Use `replace_content` for weekly rollups and project status pages that should show the latest version, not a stack of appended updates.

---

## 8) Update page properties

```json
notion-update-page({
  "page_id": "REPLACE_WITH_PAGE_ID",
  "command": "update_properties",
  "properties": { "title": "Decision Memo — Updated Title" }
})
```

For database pages, use the exact property names from the data source schema.

---

## Content size limits

Notion API limits:
- Max ~2000 characters per rich text element
- For content longer than ~1500 words, split into multiple create/update calls
- Keep each content payload focused; add long sections via follow-up append calls

## Duplicate handling

Always search before creating when:
- The title contains a person name, project name, or recurring topic
- The content type recurs (weekly rollup, project status, financial snapshot)
- You are unsure whether the page already exists

When a duplicate is found:
- For rollups and status pages: use `replace_content` to supersede the old version
- For knowledge pages: use `update_content` to append new findings
- For captures: skip the write entirely and note the existing page

## Comments API

Add review markers or metadata to pages without editing the page content.

```json
// Create a comment on a page
POST https://api.notion.com/v1/comments
{
  "parent": { "page_id": "PAGE_ID" },
  "rich_text": [{ "text": { "content": "The agent reviewed 2026-03-22. Content is current." } }]
}
```

Use comments for:
- reviewed markers
- flagging stale content for refresh
- adding context notes without cluttering the page body
- tracking when content was last verified

Do NOT use comments for:
- actual content that should be searchable (put that in the page body)
- conversation threads (use your chat system for that)

## Long content splitting

Notion limits each rich text element to ~2000 characters. For content longer than ~1500 words:

1. Create the page with the first section of content
2. Use `notion-update-page` with `update_content` to append subsequent sections
3. Keep each payload under 1500 words to stay safely within limits

Example flow for a 3000-word research summary:
```
Step 1: notion-create-pages → title + summary + first 1500 words
Step 2: notion-update-page (update_content) → next 1500 words
```

Do not try to send the entire content in one call if it exceeds ~1500 words.

## Webhooks (future capability)

Notion supports webhooks for change notifications. Not yet wired up, but when enabled this would allow:
- detect when the owner adds or edits content in Notion → sync back to agent memory or another local system
- detect when the owner drops something in Inbox DB → the agent processes it
- two-way sync instead of one-way push
- trigger agent workflows from Notion changes

Webhook setup requires:
- register a webhook endpoint via Notion API
- configure which databases/pages to watch
- OpenClaw hooks endpoint to receive events

This is a v2 capability — document it here so it's not forgotten.

## Operational advice

- Search first when duplicate risk is non-trivial
- Use Inbox DB for ambiguous or low-structure captures
- Use parent pages for durable artifacts
- Append instead of recreate when a page already exists
- Write to workspace memory too when the information matters for agent continuity
