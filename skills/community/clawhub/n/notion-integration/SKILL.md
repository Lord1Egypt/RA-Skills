# SKILL.md — Notion Integration

## Metadata

- **Name:** notion
- **Description:** Integrate with Notion's API v1 to search pages and databases, read and create content, manage database entries, add comments, and archive pages.
- **Trigger Phrases:** "search Notion", "find Notion page", "create Notion page", "query Notion database", "get Notion content", "Notion integration", "add Notion comment", "update Notion properties", "Notion API", "archive Notion page", "Notion database", "sync to Notion", "Notion block", "read Notion page", "Notion token"
- **Version:** 2.0.0

---

## 1. Capabilities

This skill enables the following operations against the Notion API v1:

1. **Search pages and databases** — Full-text search across a workspace via `POST /search`
2. **Get page content** — Retrieve page metadata and all blocks via `GET /pages/{id}` and `GET /blocks/{id}/children`
3. **Create a page** — Create a new page under a parent (page or database) via `POST /pages`
4. **Update page properties** — Patch title, status, select, date, checkbox, and other property types via `PATCH /pages/{id}`
5. **Create a database** — Create a new database under a parent page via `POST /databases`
6. **Query a database** — Filter, sort, and paginate database entries via `POST /databases/{id}/query`
7. **Add a comment** — Post a comment to a page via `POST /comments`
8. **Archive / delete a page** — Move a page to trash via `PATCH /pages/{id}` with `archived: true`

---

## 2. Trigger Phrases

Activate this skill when the user says (or implies) any of the following:

1. "search Notion for [query]"
2. "find a Notion page about [topic]"
3. "get the content of this Notion page"
4. "read a Notion page"
5. "create a new page in Notion"
6. "add a new entry to my Notion database"
7. "query my Notion task database"
8. "update Notion page properties"
9. "add a comment to that Notion page"
10. "archive the Notion page [title]"
11. "create a Notion database"
12. "sync data to Notion"
13. "Notion integration setup"
14. "use the Notion API"
15. "Notion page [title]"

---

## 3. Prerequisites

### 3.1 Notion Integration Token (Internal Integration)

1. Go to **https://www.notion.so/profile/integrations**
2. Click **"New integration"**
3. Fill in:
   - **Name:** a descriptive label (e.g., "OpenClaw Bot")
   - **Associated workspace:** select your workspace
   - **Type:** Internal
4. Click **Submit**
5. Copy the **Internal Integration Token** — it starts with `secret_`

### 3.2 Share Pages / Databases with the Integration

By default, an integration can only see content it has been explicitly given access to.

1. Open the target page or database in Notion
2. Click the **`···`** (three-dot) menu in the top-right corner
3. Select **"Add connections"** or **"Connect to"**
4. Find and enable your integration by name
5. The integration can now access that page (and its children if appropriate)

### 3.3 Required Configuration

Store the token as an environment variable:

```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Or set it in the OpenClaw gateway config under `plugins.entries.notion.config.token`.

---

## 4. Detailed Steps — API Reference

**Base URL:** `https://api.notion.com/v1`  
**Auth:** `Authorization: Bearer {NOTION_TOKEN}`  
**Notion-Version:** `2022-06-28` (required in all request headers)

All requests use JSON. Errors follow the Notion error format.

---

### 4.1 Search Pages / Databases

**Endpoint:** `POST https://api.notion.com/v1/search`

**When to use:** The user wants to find pages or databases by keyword.

**Request headers:**

```
Authorization: Bearer {NOTION_TOKEN}
Notion-Version: 2022-06-28
Content-Type: application/json
```

**Request body:**

```json
{
  "query": "quarterly report",
  "filter": { "value": "page", "property": "object" },
  "sort": { "direction": "descending", "timestamp": "last_edited_time" },
  "page_size": 10
}
```

- `filter.value`: `"page"`, `"database"`, or omit entirely to search both
- `page_size`: max 100 per page

**Success response (200):**

```json
{
  "object": "list",
  "results": [
    {
      "object": "page",
      "id": "abcd1234-abcd-1234-abcd-1234abcd1234",
      "properties": {
        "title": {
          "title": [{ "type": "text", "text": { "content": "Q3 Quarterly Report" } }]
        }
      },
      "last_edited_time": "2024-11-01T12:00:00.000Z",
      "url": "https://www.notion.so/abcd1234abcd1234abcd1234abcd1234"
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

**Error response (401/403):**

```json
{
  "object": "error",
  "code": "unauthorized",
  "message": "Make sure the token is valid and the page is shared with your integration."
}
```

---

### 4.2 Get Page Content

**Endpoint:** `GET https://api.notion.com/v1/pages/{page_id}`

**When to use:** The user wants to read a specific page's metadata and properties.

**Page ID extraction:** The ID is the 32-character hex string (with hyphens) at the end of the Notion URL.

```
URL:  https://www.notion.so/Team/Project-Status-1234abcd1234abcd
ID:   1234abcd-1234-abcd-1234-abcd1234abcd1234
```

**Success response (200):** Returns page object with `properties`, `url`, `parent`, `created_time`, and `last_edited_time`.

**To retrieve the page's block content (the actual text):**

**Endpoint:** `GET https://api.notion.com/v1/blocks/{page_id}/children?page_size=100`

**Success response (200):**

```json
{
  "object": "list",
  "results": [
    {
      "id": "block-uuid-here",
      "type": "paragraph",
      "has_children": false,
      "paragraph": {
        "rich_text": [
          {
            "type": "text",
            "text": { "content": "Hello world", "link": null },
            "annotations": { "bold": false, "italic": false, "strikethrough": false, "underline": false, "code": false, "color": "default" }
          }
        ]
      }
    },
    {
      "id": "heading-block-uuid",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{ "type": "text", "text": { "content": "Section Title" } }]
      }
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

**Common block types:** `paragraph`, `heading_1`, `heading_2`, `heading_3`, `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `code`, `quote`, `callout`, `divider`, `image`, `video`, `embed`, `bookmark`, `table`, `table_row`, `child_page`, `unsupported`

**To check if a block has children and fetch them recursively:**

```json
{
  "id": "parent-block-id",
  "type": "toggle",
  "has_children": true,
  ...
}
# Follow up with: GET /v1/blocks/{parent-block-id}/children
```

---

### 4.3 Create a Page

**Endpoint:** `POST https://api.notion.com/v1/pages`

**When to use:** The user wants to create a new Notion page.

**Option A — Create as a child of an existing page (sub-page):**

```json
{
  "parent": { "type": "page_id", "page_id": "parent-page-id" },
  "properties": {
    "title": {
      "title": [{ "type": "text", "text": { "content": "New Project Page" } }]
    }
  },
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{ "type": "text", "text": { "content": "Project kickoff notes." } }]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{ "type": "text", "text": { "content": "Goals" } }]
      }
    }
  ]
}
```

**Option B — Create as a new entry in a database:**

```json
{
  "parent": { "type": "database_id", "database_id": "database-id" },
  "properties": {
    "Name": { "title": [{ "type": "text", "text": { "content": "New Task" } }] },
    "Status": { "select": { "name": "To Do" } },
    "Priority": { "select": { "name": "High" } },
    "Due Date": { "date": { "start": "2024-12-31" } },
    "Estimate": { "number": 3 }
  }
}
```

**Success response (200):** Returns the created page object with `id` and `url`.

**Error (400) — missing title:**

```json
{
  "object": "error",
  "code": "validation_error",
  "message": "title is missing and is required."
}
```

**Error (400) — unknown property:**

```json
{
  "object": "error",
  "code": "validation_error",
  "message": "Unknown property 'Foo' in properties."
}
```

---

### 4.4 Update Page Properties

**Endpoint:** `PATCH https://api.notion.com/v1/pages/{page_id}`

**When to use:** The user wants to update a property on an existing page (rename, change status, set due date, etc.).

**Update title:**

```json
{
  "properties": {
    "title": {
      "title": [{ "type": "text", "text": { "content": "Updated Page Title" } }]
    }
  }
}
```

**Update select / status:**

```json
{
  "properties": {
    "Status": { "select": { "name": "In Progress" } }
  }
}
```

**Clear a select (set to null):**

```json
{
  "properties": {
    "Status": { "select": null }
  }
}
```

**Update date:**

```json
{
  "properties": {
    "Due Date": { "date": { "start": "2024-12-31", "end": "2025-01-15" } }
  }
}
```

**Clear date:**

```json
{
  "properties": {
    "Due Date": { "date": null }
  }
}
```

**Update number:**

```json
{
  "properties": {
    "Estimate": { "number": 8 }
  }
}
```

**Update checkbox:**

```json
{
  "properties": {
    "Complete": { "checkbox": true }
  }
}
```

**Update people (by email):**

```json
{
  "properties": {
    "Assignee": { "people": [{ "object": "user", "id": "user-id-or-email" }] }
  }
}
```

**Update multi-select:**

```json
{
  "properties": {
    "Tags": { "multi_select": [{ "name": "urgent" }, { "name": "frontend" }] }
  }
}
```

**Success response (200):** Returns the updated page object.

---

### 4.5 Create a Database

**Endpoint:** `POST https://api.notion.com/v1/databases`

**When to use:** The user wants to create a new database (table) under a parent page.

**Request body:**

```json
{
  "parent": { "type": "page_id", "page_id": "parent-page-id" },
  "title": [{ "type": "text", "text": { "content": "Project Tracker" } }],
  "properties": {
    "Name": { "title": {} },
    "Status": {
      "select": {
        "options": [
          { "name": "To Do", "color": "red" },
          { "name": "In Progress", "color": "yellow" },
          { "name": "Done", "color": "green" }
        ]
      }
    },
    "Priority": {
      "select": {
        "options": [
          { "name": "High", "color": "red" },
          { "name": "Medium", "color": "orange" },
          { "name": "Low", "color": "blue" }
        ]
      }
    },
    "Due Date": { "date": {} },
    "Estimate": { "number": { "format": "number" } },
    "Complete": { "checkbox": {} },
    "URL": { "url": {} }
  }
}
```

**Success response (200):** Returns the created database object. Save the `id` field — it is used as `database_id` in subsequent queries and page creation.

**Note:** Once created, the property schema (types and names) is fixed. To change it, you must modify the database in the Notion UI.

---

### 4.6 Query a Database

**Endpoint:** `POST https://api.notion.com/v1/databases/{database_id}/query`

**When to use:** The user wants to list, filter, and sort entries in a Notion database.

**Basic query — return all entries (up to 100):**

```json
{
  "page_size": 100
}
```

**With filter — Status equals "In Progress":**

```json
{
  "filter": {
    "property": "Status",
    "select": { "equals": "In Progress" }
  }
}
```

**With filter — Due Date before a date:**

```json
{
  "filter": {
    "property": "Due Date",
    "date": { "before": "2024-12-31" }
  }
}
```

**With filter — Title contains text:**

```json
{
  "filter": {
    "property": "Name",
    "title": { "contains": "launch" }
  }
}
```

**With compound filter (AND):**

```json
{
  "filter": {
    "and": [
      { "property": "Status", "select": { "equals": "To Do" } },
      { "property": "Priority", "select": { "equals": "High" } }
    ]
  }
}
```

**With compound filter (OR):**

```json
{
  "filter": {
    "or": [
      { "property": "Status", "select": { "equals": "Done" } },
      { "property": "Status", "select": { "equals": "Cancelled" } }
    ]
  }
}
```

**Sort by Due Date ascending:**

```json
{
  "sorts": [{ "property": "Due Date", "direction": "ascending" }]
}
```

**Sort by multiple fields:**

```json
{
  "sorts": [
    { "property": "Status", "direction": "ascending" },
    { "property": "Priority", "direction": "ascending" }
  ]
}
```

**Pagination — get next page:**

```json
{
  "start_cursor": "cursor-string-from-previous-response",
  "page_size": 100
}
```

**Success response (200):**

```json
{
  "object": "list",
  "results": [
    {
      "object": "page",
      "id": "page-uuid",
      "properties": {
        "Name": {
          "title": [{ "text": { "content": "Task A" } }]
        },
        "Status": { "select": { "name": "In Progress" } },
        "Priority": { "select": { "name": "High" } },
        "Due Date": { "date": { "start": "2024-12-01" } }
      },
      "url": "https://www.notion.so/page-uuid"
    }
  ],
  "has_more": true,
  "next_cursor": "next-page-cursor-string"
}
```

---

### 4.7 Add a Comment

**Endpoint:** `POST https://api.notion.com/v1/comments`

**When to use:** The user wants to leave a comment on a Notion page.

**Request body — new discussion thread:**

```json
{
  "parent": { "type": "page_id", "page_id": "target-page-id" },
  "rich_text": [
    {
      "type": "text",
      "text": { "content": "This looks great! Let's discuss in the next standup." }
    }
  ]
}
```

**Request body — reply to an existing thread:**

```json
{
  "discussion_id": "discussion-id-from-existing-comment",
  "rich_text": [
    {
      "type": "text",
      "text": { "content": "Agreed. Updating the estimate." }
    }
  ]
}
```

**Success response (200):** Returns the created comment object including `id` and `discussion_id`.

---

### 4.8 Archive / Delete a Page

**Endpoint:** `PATCH https://api.notion.com/v1/pages/{page_id}`

**When to use:** The user wants to move a page to trash.

**Archive a page:**

```json
{
  "archived": true
}
```

**Restore an archived page:**

```json
{
  "archived": false
}
```

**Success response (200):** Returns the updated page object.

**Note:** Notion retains archived pages for 30 days before permanent deletion. Archived pages do not appear in default search results.

---

## 5. Output Format

### 5.1 Success Output

```
✅ Notion API — Success

- Operation: [operation name]
- Page/Database ID: [id]
- Title: [title if available]
- URL: https://www.notion.so/[id]
- Last edited: [ISO timestamp]
- Details: [any additional relevant fields]
```

### 5.2 Error Output

```
❌ Notion API — Error

- Operation: [operation name]
- Error code: [error code string]
- Message: [human-readable error message from Notion]
- Suggestion: [what to try or check]
```

---

## 6. Example Conversations

### Example 1: Search Notion

**User:** "Search Notion for 'project roadmap'"

**Agent (using this skill):**

```
POST /search
Body: { "query": "project roadmap", "page_size": 10 }

✅ Notion API — Success
- Operation: Search pages/databases
- Query: "project roadmap"
- Results: 3 items found

1. 📄 Q4 Project Roadmap (page)
   ID: abcd1234-abcd-1234-abcd-1234abcd1234
   Last edited: 2024-11-01T10:00:00Z
   URL: https://www.notion.so/abcd1234abcd1234abcd1234abcd1234

2. 🗃  Roadmap Tracker (database)
   ID: efgh5678-5678-5678-efgh56785678
   Last edited: 2024-10-28T14:30:00Z
   URL: https://www.notion.so/efgh567856785678efgh56785678

3. 📄 Product Roadmap 2025 (page)
   ID: ijkl9012-9012-9012-ijkl90129012
   Last edited: 2024-10-15T09:00:00Z
   URL: https://www.notion.so/ijkl901290129012ijkl90129012
```

---

### Example 2: Query a Database with Filters

**User:** "Show me all high-priority tasks that are not done in the Sprint database"

**Agent (using this skill):**

```
POST /databases/{database_id}/query
Body: {
  "filter": {
    "and": [
      { "property": "Priority", "select": { "equals": "High" } },
      { "property": "Status", "select": { "does_not_equal": "Done" } }
    ]
  },
  "sorts": [{ "property": "Due Date", "direction": "ascending" }]
}

✅ Notion API — Success
- Operation: Query database "Sprint"
- Filtered: Priority=High AND Status≠Done
- Sorted by: Due Date ↑

1. 🔴 Design Review
   Status: To Do | Priority: High | Due: 2024-12-05
   URL: https://www.notion.so/page-id-1

2. 🔴 API Integration
   Status: In Progress | Priority: High | Due: 2024-12-08
   URL: https://www.notion.so/page-id-2

3. 🔴 Testing Phase
   Status: To Do | Priority: High | Due: 2024-12-10
   URL: https://www.notion.so/page-id-3
```

---

### Example 3: Create a Page with Content

**User:** "Create a new Notion page under 'Projects > Alpha' titled 'Sprint 5 Notes' and add a paragraph that says 'Kicked off sprint 5 planning.'"

**Agent (using this skill):**

```
POST /pages
Body: {
  "parent": { "type": "page_id", "page_id": "parent-page-id" },
  "properties": {
    "title": { "title": [{ "type": "text", "text": { "content": "Sprint 5 Notes" } }] }
  },
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{ "type": "text", "text": { "content": "Kicked off sprint 5 planning." } }]
      }
    }
  ]
}

✅ Notion API — Success
- Operation: Create page
- Title: Sprint 5 Notes
- Page ID: new-page-id-here
- URL: https://www.notion.so/newpageidhere
- Content: 1 block (paragraph) added
```

---

## 7. Installation Guide

### Step 1 — Create a Notion Integration

1. Visit **https://www.notion.so/profile/integrations**
2. Click **"Develop or manage integrations"**
3. Click **"New integration"**
4. Fill in:
   - **Name:** `OpenClaw` (or any preferred name)
   - **Workspace:** select your workspace
   - **Type:** Internal
5. Click **Submit**
6. Copy and securely store the **Internal Integration Token** (starts with `secret_`)

### Step 2 — Store the Token

Add to your shell profile:

```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Or configure in the OpenClaw gateway config:

```json
{
  "plugins": {
    "entries": {
      "notion": {
        "config": {
          "token": "secret_xxx"
        }
      }
    }
  }
}
```

### Step 3 — Share Pages with the Integration

For the integration to access any page or database:

1. Open the page or database in Notion
2. Click **`···`** in the top-right corner
3. Select **"Add connections"**
4. Find your integration by name and enable it
5. **Note:** If a page has sub-pages, either share the top-level parent (children inherit access) or share each child individually

### Step 4 — Verify Access

Test with a search call:

```
POST https://api.notion.com/v1/search
Authorization: Bearer {NOTION_TOKEN}
Notion-Version: 2022-06-28
Content-Type: application/json
Body: { "query": "test", "page_size": 1 }
```

- **200 response:** Integration is working correctly
- **401 response:** Token is invalid or malformed
- **403 response:** Token is valid but the page is not shared with the integration

---

## 8. Caveats

### 8.1 Rate Limits

| Plan | Requests per minute |
|------|-------------------|
| Free | 3 requests/second (~180/min) |
| Plus | 7 requests/second (~420/min) |
| Business | 15 requests/second (~900/min) |

- **On 429 response:** Notion includes a `Retry-After` header. Wait that many seconds before retrying.
- **Batching:** When creating or updating many pages, add a 500ms–1s delay between calls.
- **Pagination:** Always check `has_more` before making follow-up requests to avoid infinite loops.

### 8.2 Block Structure

- The Notion API returns blocks as a **flat list**, even for nested content.
- Use the `has_children: true` flag on a block to detect children, then fetch them with `GET /blocks/{id}/children`.
- Block IDs are stable but **change on page duplication**. Always re-fetch IDs for newly duplicated pages.

### 8.3 Parent Page vs. Database

- `parent: { "type": "page_id", "page_id": "..." }` creates a standalone sub-page
- `parent: { "type": "database_id", "database_id": "..." }` creates a new row (entry) in that database
- When creating in a database, the `properties` must match the database schema exactly — unknown or mismatched properties cause a `validation_error`

### 8.4 Rich Text

- Rich text is always an **array**, even for a single string. Always wrap content in `[{ ... }]`.
- Maximum length per `rich_text` array item is **2000 characters**. For longer content, split into multiple blocks.

### 8.5 Archived Pages

- `archived: true` moves a page to trash; it remains accessible via API
- Archived pages **do not appear** in default search results
- Notion permanently deletes trash after **30 days**
- To restore: `PATCH /pages/{id}` with `archived: false`

### 8.6 Database Schema Changes

- Changing a database's schema in the Notion UI (add/remove/rename properties) may break existing API calls that reference old property names
- Always call `GET /databases/{id}` first to fetch the current schema before creating or updating entries

### 8.7 ID Formats

- Notion page/database IDs are UUIDs with hyphens: `abcd1234-abcd-1234-abcd-1234abcd1234`
- In API paths, hyphens can be included or omitted: both work
- The 32-char raw ID (no hyphens) is used in internal Notion URLs

---

*Last updated: 2024-12-01 — aligned with Notion API v1, Notion-Version 2022-06-28*
