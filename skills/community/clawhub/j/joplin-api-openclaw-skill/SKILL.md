---
name: joplin
description: Manage Joplin notes via Server API - create, read, edit, search notes, notebooks, todos, and kanban boards
allowed-tools: Bash(node *, op *)
metadata: {"openclaw": {"requires": {"bins": ["node"], "optional_bins": ["op"], "config": ["~/.joplin-server-config"]}, "emoji": "📓", "homepage": "https://joplinapp.org"}}
---

# Joplin Server API Skill

Manage Joplin notes via the Joplin Server REST API (based on [joppy](https://github.com/marph91/joppy)).

## CRITICAL: Always Execute Commands

**NEVER assume or hallucinate results.** You MUST:

1. **Always run the actual commands** using the Bash tool
2. **Check for errors** in JSON responses - report any errors to the user
3. **Show real data** from the API responses
4. If config is missing, offer to retrieve from 1Password or create manually

## Setup

Credentials can be configured in two ways:

### Option A: Config File

Create `~/.joplin-server-config`:

```bash
JOPLIN_SERVER_URL=https://your-joplin-server.com
JOPLIN_EMAIL=your-email@example.com
JOPLIN_PASSWORD=your-password
# Optional: skip TLS verification for self-signed certificates (security risk!)
# JOPLIN_SKIP_TLS_VERIFY=true
```

### Option B: 1Password

If user prefers 1Password, retrieve credentials and create the config:

```bash
# Get credentials from 1Password (adjust vault/item name as needed)
JOPLIN_URL=$(op read "op://Private/Joplin Server/url" 2>/dev/null)
JOPLIN_EMAIL=$(op read "op://Private/Joplin Server/username" 2>/dev/null)
JOPLIN_PASS=$(op read "op://Private/Joplin Server/password" 2>/dev/null)

# Write config file
cat > ~/.joplin-server-config << EOF
JOPLIN_SERVER_URL=$JOPLIN_URL
JOPLIN_EMAIL=$JOPLIN_EMAIL
JOPLIN_PASSWORD=$JOPLIN_PASS
EOF
chmod 600 ~/.joplin-server-config
```

Ask user for their 1Password vault name and item name if different from "Private/Joplin Server".

## Client Usage

All commands use the bundled JavaScript client:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js <command> [args...]
```

### Available Commands

| Command | Description |
|---------|-------------|
| `ping` | Health check (no auth required) |
| `login` | Authenticate and verify connection |
| `list-notebooks` | List all notebooks |
| `list-notes` | List all notes |
| `get-note <id>` | Get note content |
| `add-notebook <title>` | Create a new notebook |
| `add-note <title> [parent_id] [body]` | Create a new note |
| `modify-note <id> <field> <value>` | Modify a note field |
| `delete-note <id>` | Delete a note |
| `search <query>` | Search notes by title/content |

### Response Format

All commands return JSON. Errors include an `error` field:

```json
{"id": "abc123", "title": "My Note"}   // Success
{"ok": false, "error": "..."}          // Failure
```

## Workflow: First Time Setup

When user first invokes this skill:

```bash
# Step 1: Check if config exists
cat ~/.joplin-server-config 2>/dev/null || echo "CONFIG_MISSING"

# Step 2: If config exists, test connection
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js ping
```

If config is missing, ask user which setup method they prefer:

1. **1Password** - Ask for vault/item name, then run:
   ```bash
   JOPLIN_URL=$(op read "op://VAULT/ITEM/url")
   JOPLIN_EMAIL=$(op read "op://VAULT/ITEM/username")
   JOPLIN_PASS=$(op read "op://VAULT/ITEM/password")
   cat > ~/.joplin-server-config << EOF
   JOPLIN_SERVER_URL=$JOPLIN_URL
   JOPLIN_EMAIL=$JOPLIN_EMAIL
   JOPLIN_PASSWORD=$JOPLIN_PASS
   EOF
   chmod 600 ~/.joplin-server-config
   ```

2. **Manual** - User creates `~/.joplin-server-config` with:
   ```
   JOPLIN_SERVER_URL=https://your-server.com
   JOPLIN_EMAIL=your-email
   JOPLIN_PASSWORD=your-password
   ```

## Common Operations

### List Notebooks

```bash
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js list-notebooks
```

### List All Notes

```bash
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js list-notes
```

### Read a Note

```bash
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js get-note <note_id>
```

### Create a Notebook

```bash
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js add-notebook "My Notebook"
```

### Create a Note

```bash
# Basic note
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js add-note "My Note Title"

# Note in a specific notebook
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js add-note "My Note Title" <notebook_id>

# Note with body content
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js add-note "My Note Title" <notebook_id> "Note body here"
```

### Modify a Note

```bash
# Update title
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js modify-note <note_id> title "New Title"

# Update body
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js modify-note <note_id> body "New body content"
```

### Search Notes

```bash
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js search "search term"
```

### Delete a Note

```bash
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js delete-note <note_id>
```

## Sync Lock

The API client automatically handles Joplin's sync lock protocol:

- Acquires a sync lock before write operations (add, modify, delete)
- Releases the lock after the operation completes
- Read operations (list, get, search) don't require locks

## Item Types

| Type | Value | Description |
|------|-------|-------------|
| Note | 1 | Markdown notes |
| Folder | 2 | Notebooks |
| Resource | 4 | Attachments |
| Tag | 5 | Tags |
| NoteTag | 6 | Note-tag links |

## Note Content Format

Notes are returned as objects with these fields:

```json
{
  "id": "abc123def456",
  "parent_id": "parent-folder-uuid",
  "title": "My Note Title",
  "body": "Note content in markdown...",
  "created_time": "2024-01-15T10:30:00.000Z",
  "updated_time": "2024-01-15T10:30:00.000Z",
  "type_": "1",
  "markup_language": "1"
}
```

## TODOs

All TODOs go into the **"TODOs" notebook**.

### Daily TODOs

Daily planning notes follow this naming format:

```
TODO#dd.mm.yy <Wd>
```

Where `<Wd>` is a 2-letter weekday: `Mo`, `Tu`, `We`, `Th`, `Fr`, `Sa`, `Su`

**Examples:**
- `TODO#16.03.26 Su` (Sunday, March 16, 2026)
- `TODO#17.03.26 Mo` (Monday, March 17, 2026)

**Content format:** One checkbox per line for individual tasks:

```markdown
- [ ] Morning standup
- [ ] Review PR #123
- [ ] Deploy to staging
- [x] Send weekly report
```

### General TODOs

Non-daily TODOs (projects, ideas, recurring tasks) also go in the "TODOs" notebook but:
- Don't follow the `TODO#dd.mm.yy` naming format
- Each note represents one individual task or topic
- Use descriptive titles like "Fix authentication bug" or "Research caching options"

## Kanban Notes (YesYouKan)

When editing kanban-formatted notes:

1. **Column headings** use `#` - Keep exact names: `# Backlog`, `# In progress`, `# Done`
2. **Task headings** use `##`
3. **Never modify** the `kanban-settings` code block at the end
4. **Preserve blank lines** exactly as they appear

## Error Handling

| Error | Meaning |
|-------|---------|
| `CONFIG_MISSING` | No `~/.joplin-server-config` file |
| `Authentication failed` | Wrong credentials or server unreachable |
| `Request timeout` | Server not responding (check URL) |
| `Sync target has exclusive lock` | Another client is syncing |
| `404` | Item not found |

## Troubleshooting

If auth fails:

```bash
# Test server reachability
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js ping

# Test login
node ${CLAUDE_SKILL_DIR}/scripts/joplin-server-api.js login

# Check config file
cat ~/.joplin-server-config
```
