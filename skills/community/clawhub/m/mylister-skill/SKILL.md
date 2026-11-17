---
name: lister
description: Natural language task and list management for MyLister through its public API.
---

# Lister — Natural Language Task Management

**Skill name:** `lister`
**Description:** Natural language task management with MyLister.dev — add, view, update, move, and organize to-do items across lists via conversational commands.

## When to Use This Skill

Use this skill whenever the user wants to manage tasks, to-do items, or lists using natural language. Trigger phrases include (but are not limited to):

- **"create a new list"** — create a new list
- **"delete my list"** — delete a list
- **"add to list"** — create a new task item
- **"get my lists"** — view all lists or items in a list
- **"priority items"** — see urgent/important items
- **"mark done"** — complete an item
- **"remove item"** — delete an item
- **"update item"** — change an item's text or priority
- **"move item"** — transfer an item to another list
- **"note for item"** — attach a note to an item
- **"comment on item"** — add, view, update, or delete comments on shared items
- **"comment on note"** — add, view, update, or delete comments on item notes
- **"reminder"** — add or update simple item reminders
- **"project list"** — create project lists and project items with start/end/duration/assignee metadata
- **"export list"** — export a list as JSON or HTML
- **"email list"** — email a list to someone
- **"export priority"** — export all priority items
- **"email priority"** — email priority items to someone
- **"export item"** — export one item as JSON or HTML
- **"email item"** — email one item
- **"attachment"** — upload or remove an item attachment
- **"upload image/voice"** — upload media and optionally associate it with a list or item
- **"API health/version"** — inspect the deployed API status

## Configuration

The following environment variables must be set before invoking the skill:

| Variable | Required | Description |
|----------|----------|-------------|
| `LISTER_BASE_URL` | No | Lister API base URL. Defaults to `https://api.mylister.dev` |
| `LISTER_API_KEY` | **Yes** | API key for authenticating with the Lister API via `X-API-Key` |
| `LISTER_PRODUCTION_BASE_URL` | No | Optional production API base URL override (defaults to `https://api.mylister.dev`) |
| `LISTER_STAGING_BASE_URL` | No | Optional staging API base URL override |
| `LISTER_PRODUCTION_API_KEY` | No | Optional production API key override for environment switching |
| `LISTER_STAGING_API_KEY` | No | Optional staging API key override for environment switching |
| `LISTER_CONTACTS` | No | Optional JSON contact directory for email alias resolution. Supports either object map (`{"name":"email"}`) or array entries (`{"name","email","alias","aliases":[]}`) |

## How to Invoke

The skill exposes a `handleCommand(input: string): Promise<string>` function. Pass any natural language string and receive a formatted response.

**CLI:**
```bash
node dist/index.js <natural language command>
```

**As a module:**
```typescript
import { handleCommand } from './dist/index.js';
const result = await handleCommand('add "buy milk" to my groceries list');
console.log(result);
```

## Supported Commands

### 1. Add Item
Add a new task to a specific list. Use quotes for the task text. Mark items as priority with the word "priority" or "urgent".

| Pattern | Example |
|---------|---------|
| `add "text" to my [list] list` | `add "call Notary" to my today list` |
| `create "text" in [list] list` | `create "review contract" in work list` |
| `put "text" on my [list] list` | `put "walk the dog" on my errands list` |
| `add "text" to my [list] list` (priority) | `add "fix server outage" to my today list urgent` |
| `add "text" to my [list] list reminder tomorrow at 9am` | `add "call Mama" to my today list reminder tomorrow at 9am` |
| `add "text" to my [list] list with note "details"` | `add "ship dashboard" to my work list with note "needs QA"` |
| `add "text" to my [list] list with comment "details"` | `add "review plan" to my project list with comment "shared context"` |
| `add "text" to my [project] list starts YYYY-MM-DD due YYYY-MM-DD for N hours assigned to [user]` | `add "design milestone" to my launch list starts 2026-09-01 due 2026-09-05 for 3 hours assigned to larry@example.com` |

**Keywords:** `add`, `create`, `new`, `put`

**Create payload support:** item creation can include inline `notes`, inline `comments`, `reminder`, and project metadata (`startDate`, `endDate`, `durationMinutes`, `assignedTo`) when those phrases are present.

Project metadata is accepted by the API for project lists. If no assignee is supplied, the API assigns the item to the project owner. An explicit assignee must be the owner or an edit/admin collaborator.

### 2. Get / List Items
View all items in a specific list, or show all lists if no list name is given.

| Pattern | Example |
|---------|---------|
| `get my [list] list` | `get my today list` |
| `show [list] list` | `show work list` |
| `list [list] list` | `list groceries list` |
| `get my lists` (no list name) | `get my lists` → shows all lists |
| `view [list] list` | `view personal list` |
| `find [list] list` | `find work list` |

**Keywords:** `get`, `show`, `list`, `view`, `find`, `search`

### 3. Priority Items
Get all items marked as priority/urgent across all lists.

| Pattern | Example |
|---------|---------|
| `get priority items` | `get priority items` |
| `show urgent items` | `show urgent items` |
| `get important items` | `get important items` |

**Keywords:** `priority`, `urgent`, `important` (combined with `get`/`show`/`list`)

### 4. Mark Done
Mark a task item as completed.

| Pattern | Example |
|---------|---------|
| `mark item [id] done` | `mark item 123 done` |
| `complete item [id]` | `complete item 456` |
| `finish item [id]` | `finish item 789` |
| `done item [id]` | `done item 101` |

**Keywords:** `mark`, `complete`, `done`, `finish`

### 5. Remove Item
Delete a task item permanently.

| Pattern | Example |
|---------|---------|
| `remove item [id]` | `remove item 123` |
| `delete item [id]` | `delete item 456` |
| `drop item [id]` | `drop item 789` |
| `clear item [id]` | `clear item 101` |

**Keywords:** `remove`, `delete`, `drop`, `clear`

### 6. Update Item
Change an item's text or set it as priority.

| Pattern | Example |
|---------|---------|
| `update item [id] to "new text"` | `update item 123 to "call Notary at 3pm"` |
| `edit item [id] to "new text"` | `edit item 456 to "buy organic milk"` |
| `change item [id] to "new text"` | `change item 789 to "schedule dentist"` |
| `update item [id]` (priority) | `update item 123 priority` |

**Keywords:** `update`, `edit`, `change`, `modify`, `rename`

### 7. Move Item
Transfer an item from its current list to another list.

| Pattern | Example |
|---------|---------|
| `move item [id] to my [list] list` | `move item 123 to my work list` |
| `transfer item [id] to [list] list` | `transfer item 456 to personal list` |

**Keywords:** `move`, `transfer`

### 8. Add Note
Attach a note to an item.

| Pattern | Example |
|---------|---------|
| `note for item [id]: "text"` | `note for item 123: "remember to bring documents"` |
| `memo for item [id]: "text"` | `memo for item 789: "waiting on response"` |

**Keywords:** `note`, `memo`

### 8c. Attachments and Media
Upload files directly from the local filesystem, or remove an existing item attachment/image.

| Pattern | Example |
|---------|---------|
| `attach file [path] to item [id]` | `attach file "C:\\docs\\plan.pdf" to item 123` |
| `delete attachment [attachment_id] from item [id]` | `delete attachment 456 from item 123` |
| `upload image [path] to item [id]` | `upload image "C:\\images\\brief.png" to item 123` |
| `upload voice [path] to item [id] transcribe` | `upload voice "C:\\audio\\note.webm" to item 123 transcribe` |
| `remove image from item [id]` | `remove image from item 123` |
| `get file URL for [file_key] expires [seconds]` | `get file URL for attachments/lists/... expires 3600` |

Uploads use multipart form data. The skill keeps the API key header but deliberately lets `fetch` set the multipart boundary.

### 8a. Item Comments
Add, view, update, or delete comments on an item. This is useful for shared items.

| Pattern | Example |
|---------|---------|
| `comment on item [id]: "text"` | `comment on item 123: "looks good"` |
| `show comments for item [id]` | `show comments for item 123` |
| `update comment [comment_id] on item [id] to "text"` | `update comment 456 on item 123 to "updated"` |
| `delete comment [comment_id] from item [id]` | `delete comment 456 from item 123` |

### 8b. Note Comments
Add, view, update, or delete comments on a note attached to an item.

| Pattern | Example |
|---------|---------|
| `comment on note [note_id] for item [id]: "text"` | `comment on note 456 for item 123: "agree"` |
| `show comments for note [note_id] on item [id]` | `show comments for note 456 on item 123` |
| `update comment [comment_id] on note [note_id] for item [id] to "text"` | `update comment 789 on note 456 for item 123 to "updated"` |
| `delete comment [comment_id] from note [note_id] on item [id]` | `delete comment 789 from note 456 on item 123` |

### 9. Export List
Export a list to JSON or HTML format.

| Pattern | Example |
|---------|---------|
| `export my [list] list` | `export my today list` (defaults to JSON) |
| `export my [list] list as json` | `export my work list as json` |
| `export my [list] list as html` | `export my today list as html` |
| `export my [list] list as html theme dark` | `export my projects list as html theme dark` |
| `export my [list] list with archived` | `export my today list with archived` |

**Keywords:** `export`, `as json`, `as html`, `theme`, `with archived`

### 9a. Export Item
Export one item as JSON or HTML.

| Pattern | Example |
|---------|---------|
| `export item [id]` | `export item 123` |
| `export item [id] as html` | `export item 123 as html theme dark` |

### 10a. Email Item
Email (or send) one item as an HTML export.

| Pattern | Example |
|---------|---------|
| `email item [id]` | `email item 123` |
| `email item [id] to [email|name|nickname]` | `email item 123 to user@example.com`<br/>`email item 123 to "Sarah"` |
| `send item [id]` | `send item 123` |
| `send item [id] to [email|name|nickname]` | `send item 123 to "Sarah"` |

### 10. Email List
Email (or send) a list to yourself or someone else.

| Pattern | Example |
|---------|---------|
| `email my [list] list to email@example.com` | `email my today list to maik@example.com` |
| `email my [list] list to [name|nickname]` | `email my today list to "Mom"` |
| `send my [list] list to email@example.com` | `send my today list to maik@example.com` |
| `email my [list] list` | `email my work list` (sends to your email) |
| `send my [list] list` | `send my work list` (sends to your email) |
| `email my [list] list theme dark` | `email my projects list theme dark` |
| `send my [list] list theme dark` | `send my projects list theme dark` |

**Keywords:** `email`, `send`, `to`

### 11. Export Priority Items
Export all priority/urgent items across all lists.

| Pattern | Example |
|---------|---------|
| `export priority items` | `export priority items` (defaults to JSON) |
| `export priority items as html` | `export priority items as html` |
| `export priority items as html theme dark` | `export priority items as html theme dark` |

**Keywords:** `export`, `priority`, `urgent`, `important`

### 12. Email Priority Items
Email (or send) all priority items to yourself or someone else.

| Pattern | Example |
|---------|---------|
| `email priority items to email@example.com` | `email priority items to maik@example.com` |
| `email priority items to [name|nickname]` | `email priority items to "Alex"` |
| `send priority items to email@example.com` | `send priority items to maik@example.com` |
| `email priority items` | `email priority items` (sends to your email) |
| `send priority items` | `send priority items` (sends to your email) |
| `email priority items theme dark` | `email priority items theme dark` |
| `send priority items theme dark` | `send priority items theme dark` |

**Keywords:** `email`, `send`, `priority`, `urgent`, `important`

### 13. Create List
Create a new list.

| Pattern | Example |
|---------|---------|
| `create a new list called [name]` | `create a new list called Projects` |
| `make a new list named [name]` | `make a new list named Work` |
| `create a new list called [name] notebook` | `create a new list called Journal notebook` |
| `create a new project list called [name]` | `create a new project list called Website Launch` |
| `create a new list called [name] project` | `create a new list called Client Projects project` |

**Keywords:** `create`, `make`, `add`

**List types:** `standard`, `notebook`, and `project` are supported. `journal` maps to `notebook`.
An existing list can change type with `update my [list] list to project` (or `notebook`/`standard`).

### 14. Delete List
Delete an existing list (all items are permanently removed).

| Pattern | Example |
|---------|---------|
| `delete my [list] list` | `delete my old projects list` |
| `delete list [name]` | `delete list Archive` |
| `delete my [list] list permanently` | `delete my Archive list permanently` |

**Keywords:** `delete`

**Note:** List name matching is case-insensitive.

Permanent lists require the explicit `permanently` or `force` qualifier; the API sends this as `?force=true`.

### 15. Search
Search across all lists and items.

| Pattern | Example |
|---------|---------|
| `search for [query]` | `search for meeting` |
| `find [query]` | `find contract` |
| `search for [query] with notes` | `search for call with notes` |

**Keywords:** `search`, `find` (combined with search terms, not list name)

**Note:** The production API includes notes by default; `with notes` remains supported for clarity.

### 16. Lists Summary
Get a summary of all lists with item counts.

| Pattern | Example |
|---------|---------|
| `list summary` | `list summary` |
| `lists summary` | `lists summary` |
| `get list summary` | `get list summary` |

**Keywords:** `summary`

### 17. Archive List
Archive a list (hides it from normal views).

| Pattern | Example |
|---------|---------|
| `archive my [list] list` | `archive my old project list` |

**Keywords:** `archive`

### 18. Unarchive List
Restore an archived list.

| Pattern | Example |
|---------|---------|
| `unarchive my [list] list` | `unarchive my project list` |

**Keywords:** `unarchive`

**Note:** archived lists are automatically searched when resolving list names.

### 19. Share List
Share a list with another user.

| Pattern | Example |
|---------|---------|
| `share my [list] list with [email]` | `share my work list with user@example.com` |
| `share my [list] list with [email] as [perm]` | `share my work list with user@example.com as edit` |

**Keywords:** `share`, `with`, `as`

**Permissions:** `read`, `edit` (default), `admin`

### 20. List Users
Show users who have access to a list.

| Pattern | Example |
|---------|---------|
| `list users for [list] list` | `list users for my work list` |
| `show users of [list] list` | `show users of work list` |

**Keywords:** `users`, `for`, `of`

### 21. Remove User From List
Remove a user's access from a shared list.

| Pattern | Example |
|---------|---------|
| `remove user [email] from my [list] list` | `remove user@example.com from my work list` |

**Keywords:** `remove user`, `from`

### 22. Update Note
Edit the text of an existing note on an item.

| Pattern | Example |
|---------|---------|
| `update note for item [id] note [id]: "text"` | `update note for item abc123 note def456: "updated text"` |
| `edit note for item [id] note [id]: "text"` | `edit note for item abc123 note def456: "new text"` |

**Keywords:** `update note`, `edit note`, `change note`

### 23. Delete Note
Delete a note from an item.

| Pattern | Example |
|---------|---------|
| `delete note for item [id] note [id]` | `delete note for item abc123 note def456` |
| `remove note for item [id] note [id]` | `remove note for item abc123 note def456` |

**Keywords:** `delete note`, `remove note`

### 24. Update List User Permission
Change a user's permission level on a shared list.

| Pattern | Example |
|---------|--------|
| `set user [email] permission on my [list] list to [perm]` | `set user alice@example.com permission on my work list to admin` |
| `change user [email] access on [list] list to [perm]` | `change user bob@example.com access on projects list to read` |

**Permissions:** `read`, `edit`, `admin`

**Keywords:** `update user`, `change user`, `set permission`

### 25. Reorder Lists
Change the display order of lists.

| Pattern | Example |
|---------|--------|
| `reorder lists [id1] [id2] [id3]` | `reorder lists abc123 def456 ghi789` |

**Keywords:** `reorder lists`

### 26. Reorder Items
Change the display order of items within a list.

| Pattern | Example |
|---------|--------|
| `reorder items in my [list] list [id1] [id2]` | `reorder items in my today list abc123 def456` |

**Keywords:** `reorder items`

### 27. Move Completed Items
Move all completed items from one list to another.

| Pattern | Example |
|---------|--------|
| `move completed from my [list] list to my [target] list` | `move completed from my today list to my done list` |

**Keywords:** `move completed`

### 28. Update List
Rename or update a list's properties.

| Pattern | Example |
|---------|--------|
| `rename my [list] list "new name"` | `rename my projects list "Current Projects"` |
| `update my [list] list` | `update my work list` |

**Keywords:** `update list`, `rename list`, `edit list`

### 29. Get List Details
View detailed information about a specific list.

| Pattern | Example |
|---------|--------|
| `show my [list] list details` | `show my today list details` |
| `get [list] list info` | `get work list info` |

**Keywords:** `list details`, `list info`

### 30. Reorder Notes
Set the order of notes embedded in an item.

| Pattern | Example |
|---------|---------|
| `reorder notes for item [id] in order: [note IDs]` | `reorder notes for item 123 in order: 456, 789` |

### 31. API Status
Check the deployed public API without touching list data.

| Pattern | Example |
|---------|---------|
| `check API health` | `check API health` |
| `show API version` | `show API version` |

### 31a. API Environment and Credentials
Switch between configured API environments or apply API keys at runtime.

| Pattern | Example |
|---------|---------|
| `switch to production` | `switch to production` |
| `switch to staging` | `switch to staging` |
| `set API base URL to https://...` | `set API base URL to https://api-staging.mylister.dev` |
| `set API key to your-key` | `set API key to abc123` |
| `set staging API key to your-key` | `set staging API key to abc123` |

---

## API Reference

The skill uses the **Public API (`/v1/`)** endpoints on `https://api.mylister.dev`, which are accessible via API key.

| Method | Endpoint | Purpose |
|--------|----------|----------|
| \`GET\` | \`/v1/lists\` | Fetch all lists (supports \`?includeArchived=true\`) |
| \`POST\` | \`/v1/lists\` | Create a new list (`standard`, `notebook`, or `project`) |
| \`GET\` | \`/v1/lists/{id}\` | Get list details |
| \`PUT\` | \`/v1/lists/{id}\` | Update a list (name, description, etc.) |
| \`DELETE\` | \`/v1/lists/{id}?force=true\` | Delete a list; force is required for permanent lists |
| \`PUT\` | \`/v1/lists/{id}/archive\` | Archive/unarchive a list |
| \`PUT\` | \`/v1/lists/reorder\` | Reorder lists |
| \`GET\` | \`/v1/lists/summary\` | Get lists summary with counts |
| \`POST\` | \`/v1/lists/defaults\` | Create default starter lists |
| \`GET\` | \`/v1/lists/{id}/items\` | Get items in a list |
| \`POST\` | \`/v1/lists/{id}/items\` | Add an item to a list, including optional notes, comments, reminder, project metadata, and attachments |
| \`PUT\` | \`/v1/lists/{id}/items/reorder\` | Reorder items in a list |
| \`POST\` | \`/v1/lists/{id}/items/move-completed\` | Move completed items to the bottom of the same list |
| \`POST\` | \`/v1/lists/{id}/share\` | Share a list with a user |
| \`GET\` | \`/v1/lists/{id}/users\` | Get list users/permissions |
| \`PUT\` | \`/v1/lists/{id}/users/{uid}\` | Update user permission on a list |
| \`DELETE\` | \`/v1/lists/{id}/users/{uid}\` | Remove user from list |
| \`POST\` | \`/v1/lists/{id}/export\` | Export a list (JSON/HTML) |
| \`POST\` | \`/v1/lists/{id}/export/email\` | Email a list |
| \`GET\` | \`/v1/items/{id}\` | Get item details |
| \`PATCH\` | \`/v1/items/{id}\` | Update an item (text, status, priority, archived, reminder) |
| \`DELETE\` | \`/v1/items/{id}\` | Delete an item |
| \`POST\` | \`/v1/items/{id}/export\` | Export one item (JSON/HTML) |
| \`POST\` | \`/v1/items/{id}/export/email\` | Email one item |
| \`POST\` | \`/v1/items/{id}/attachments\` | Upload an item attachment (multipart) |
| \`DELETE\` | \`/v1/items/{id}/attachments/{attachment_id}\` | Delete an item attachment |
| \`DELETE\` | \`/v1/items/{id}/image\` | Remove an item image |
| \`POST\` | \`/v1/items/{id}/comments\` | Add an item comment |
| \`GET\` | \`/v1/items/{id}/comments\` | Get item comments |
| \`PUT\` | \`/v1/items/{id}/comments/{cid}\` | Update an item comment |
| \`DELETE\` | \`/v1/items/{id}/comments/{cid}\` | Delete an item comment |
| \`POST\` | \`/v1/items/{id}/move\` | Move item to another list |
| \`POST\` | \`/v1/items/{id}/notes\` | Add a note to an item |
| \`PUT\` | \`/v1/items/{id}/notes/{nid}\` | Update a note |
| \`DELETE\` | \`/v1/items/{id}/notes/{nid}\` | Delete a note |
| \`PUT\` | \`/v1/items/{id}/notes/reorder\` | Reorder notes |
| \`PATCH\` | \`/v1/items/{id}/notes/{nid}/status\` | Update note status |
| \`POST\` | \`/v1/items/{id}/notes/{nid}/comments\` | Add a note comment |
| \`GET\` | \`/v1/items/{id}/notes/{nid}/comments\` | Get note comments |
| \`PUT\` | \`/v1/items/{id}/notes/{nid}/comments/{cid}\` | Update a note comment |
| \`DELETE\` | \`/v1/items/{id}/notes/{nid}/comments/{cid}\` | Delete a note comment |
| \`GET\` | \`/v1/items/priority\` | Get all priority items |
| \`POST\` | \`/v1/items/priority/export\` | Export priority items (JSON/HTML) |
| \`POST\` | \`/v1/items/priority/export/email\` | Email priority items |
| \`GET\` | \`/v1/search\` | Search across all lists & items |
| \`POST\` | \`/v1/upload/image\` | Upload an image (multipart) |
| \`POST\` | \`/v1/upload/voice\` | Upload voice (multipart, optional transcription) |
| \`GET\` | \`/v1/files/{file_key}/url\` | Generate a presigned file URL |
| \`GET\` | \`/v1/health\` | Public API health |
| \`GET\` | \`/v1/version\` | Deployed API version metadata |

**Authentication:** API key via the `X-API-Key` header for all `/v1/` endpoints. Bearer tokens are not accepted on this public API surface.

**Important:** Always use `/v1/` endpoints on `api.mylister.dev`. Exports may return JSON or HTML; uploads/status responses are JSON. The skill validates the response host and content type accordingly.

## Response Format

Responses are formatted with emoji indicators:

- ✅ Success — followed by details or item lists
- ❌ Error — with explanation of what went wrong
- ❓ Unknown — with helpful suggestions

Item lists include:
- Numbered entries
- 🔥 for priority items
- ✅ for completed items

## Error Handling

The skill validates input before making API calls. Common validation messages:

- Missing quoted text for add/update → prompts user to use quotes
- Missing list name → prompts user to specify a list
- Missing item ID → prompts user to provide an item ID
- List not found → tells user the list name wasn't found
- API errors → surfaces the error message from the API

## File Layout

```
MyLister-Skill/
├── SKILL.md          ← This file (skill definition for OpenClaw)
├── skill.json        ← Skill metadata
├── src/
│   └── index.ts      ← TypeScript source
├── dist/
│   └── index.js      ← Compiled JavaScript (entry point)
├── package.json
└── tsconfig.json
```

## Notes for Agents

1. **Always quote item text** — the parser extracts text between quotes (`" "` or `' '`). If the user doesn't use quotes, ask them to.
2. **List names are case-insensitive** — `today`, `Today`, and `TODAY` all match the same list.
3. **IDs are 24-character hex strings in the public API** (the parser also accepts numeric IDs for compatibility). Responses may include populated creator/assignee data on shared and project items.
4. **The skill auto-resolves list names to IDs** — users don't need to know internal list IDs; they use friendly names.
5. **If the list doesn't exist**, the skill will report an error — it does **not** auto-create lists. The user must create the list first or use an existing one.
6. **Archived lists** are automatically included in list name resolution — if a list name isn't found in active lists, the skill searches archived lists too.
7. **Search** uses the `/v1/search` endpoint. The production API includes note content by default.
8. **Sharing** requires a user ID (email) and permission level (`read`, `edit`, or `admin`).
9. **Item statuses** can be `new`, `in-progress`, or `complete` (the `in-progress` status is new).
10. **Item creation** no longer requires `listId` in the request body — it's derived from the URL path.
11. **API key creation** now returns `201 Created` (was `200 OK`).
12. **Note creation** now returns `201 Created` (was `200 OK`).
13. **The default public API host is `https://api.mylister.dev`**. Override with `LISTER_BASE_URL`, `LISTER_PRODUCTION_BASE_URL`, or `LISTER_STAGING_BASE_URL` per environment.
14. **Comments are first-class resources** on both items and notes. Use the comment endpoints instead of treating item comments as notes.
15. **Move completed** reorders completed items to the bottom of the same list; it no longer moves them to another list.
16. **Notebook lists** are created by passing `type: "notebook"` when the user asks for a notebook or journal list.
17. **Project lists** are created by passing `type: "project"` when the user asks for a project list.
18. **Item creation with notes/comments** uses the `notes` and `comments` arrays in the initial `/v1/lists/{id}/items` request when the user says `with note "..."` or `with comment "..."`.
19. **Project item metadata** is sent in the `project` object with supported fields `startDate`, `endDate`, `durationMinutes`, and `assignedTo`. The API validates `assignedTo`; use the owner or an edit/admin collaborator.
20. **Project items are intentionally excluded from the priority-items surface** by the API; query the project list directly for project work.
21. **Archived item reads** use `GET /v1/lists/{id}/items?includeArchived=true`; the skill now forwards `with archived` for list item reads.
22. **The deployed API exposes item exports, note reorder, attachments, media upload, presigned file URLs, health, and version routes** in addition to list/task CRUD.
