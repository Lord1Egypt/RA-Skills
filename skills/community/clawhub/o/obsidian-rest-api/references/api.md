# Obsidian Local REST API Reference

Plugin: `obsidian-local-rest-api` by Adam Coddington
Version: 3.6.2
Official Docs: https://coddingtonbear.github.io/obsidian-local-rest-api/

## Base URL

```
https://<windows-host-ip>:27124
```

All requests require:
```bash
-H "Authorization: Bearer <api-key>"
-k  # Skip SSL verification (self-signed cert)
```

---

## API Endpoints

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns basic server details |
| GET | `/obsidian-local-rest-api.crt` | Returns SSL certificate |
| GET | `/openapi.yaml` | Returns OpenAPI spec |

---

### Vault Files

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vault/{filename}` | Return file content |
| POST | `/vault/{filename}` | Append content to file |
| PUT | `/vault/{filename}` | Create or update file |
| PATCH | `/vault/{filename}` | Partially update file (heading/block/frontmatter) |
| DELETE | `/vault/{filename}` | Delete file |

**Example - Create file:**
```bash
curl -k -X PUT \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: text/markdown" \
  -d "# Title\nContent" \
  "$URL/vault/my-note.md"
```

**Example - Append to file:**
```bash
curl -k -X POST \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: text/markdown" \
  -d "\n## New Section\nAdded content" \
  "$URL/vault/my-note.md"
```

**Example - Read file:**
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/vault/my-note.md"
```

**Example - PATCH (requires special headers):**
```bash
# Get document map to find available targets
curl -k -H "Authorization: Bearer $KEY" \
  -H "Accept: application/vnd.olrapi.document-map+json" \
  "$URL/vault/my-note.md"

# Append content below a heading
curl -k -X PATCH -H "Authorization: Bearer $KEY" \
  -H "Content-Type: text/markdown" \
  -H "Operation: append" \
  -H "Target-Type: heading" \
  -H "Target: Heading 1::Subheading" \
  -d "New content" "$URL/vault/my-note.md"

# Replace a block reference
curl -k -X PATCH -H "Authorization: Bearer $KEY" \
  -H "Content-Type: text/markdown" \
  -H "Operation: replace" \
  -H "Target-Type: block" \
  -H "Target: blockref1" \
  -d "New block content" "$URL/vault/my-note.md"
```

**PATCH Headers:**
| Header | Required | Values |
|--------|----------|--------|
| `Operation` | Yes | `append`, `prepend`, `replace` |
| `Target-Type` | Yes | `heading`, `block`, `frontmatter` |
| `Target` | Yes | Heading path (use `::` for nested), block ID, or frontmatter field |

---

### Vault Directories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vault/` | List files in vault root |
| GET | `/vault/{pathToDirectory}/` | List files in directory |

**Example:**
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/vault/"
curl -k -H "Authorization: Bearer $KEY" "$URL/vault/daily/"
```

---

### Active File

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/active/` | Get currently open file content |
| POST | `/active/` | Append to active file |
| PUT | `/active/` | Update active file content |
| PATCH | `/active/` | Partially update active file |
| DELETE | `/active/` | Delete active file |

**Example - Get active file:**
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/active/"
```

---

### Periodic Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/periodic/{period}/` | Get current periodic note |
| GET | `/periodic/{period}/{year}/{month}/{day}/` | Get periodic note for date |
| POST | `/periodic/{period}/` | Append to current periodic note |
| POST | `/periodic/{period}/{year}/{month}/{day}/` | Append to dated periodic note |
| PUT | `/periodic/{period}/` | Update current periodic note |
| PUT | `/periodic/{period}/{year}/{month}/{day}/` | Update dated periodic note |
| PATCH | `/periodic/{period}/` | Partial update current periodic note |
| PATCH | `/periodic/{period}/{year}/{month}/{day}/` | Partial update dated periodic note |
| DELETE | `/periodic/{period}/` | Delete current periodic note |
| DELETE | `/periodic/{period}/{year}/{month}/{day}/` | Delete dated periodic note |

**Period types:** `daily`, `weekly`, `monthly`, `yearly`

**Example - Get today's daily note:**
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/periodic/daily/"
```

**Example - Get specific date:**
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/periodic/daily/2026/05/11/"
```

---

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/` | Advanced search (Dataview-style query) |
| POST | `/search/simple/` | Simple text search |

**Simple search example:**
```bash
curl -k -X POST -H "Authorization: Bearer $KEY" \
  "$URL/search/simple/?query=meeting"
```

**Advanced search (JsonLogic):**
```bash
# Content-Type must be: application/vnd.olrapi.jsonlogic+json

# Find files by tag
curl -k -X POST -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/vnd.olrapi.jsonlogic+json" \
  -d '{"in": ["myTag", {"var": "tags"}]}' "$URL/search/"

# Find files by path glob
curl -k -X POST -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/vnd.olrapi.jsonlogic+json" \
  -d '{"glob": ["*daily*", {"var": "path"}]}' "$URL/search/"

# Find files larger than 500 bytes
curl -k -X POST -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/vnd.olrapi.jsonlogic+json" \
  -d '{">": [{"var": "stat.size"}, 500]}' "$URL/search/"

# AND query (tag + path)
curl -k -X POST -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/vnd.olrapi.jsonlogic+json" \
  -d '{"and": [{"in": ["work", {"var": "tags"}]}, {"glob": ["*project*", {"var": "path"}]}]}' "$URL/search/"
```

---

### Commands

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/commands/` | List available commands |
| POST | `/commands/{commandId}/` | Execute a command |

**Example - List commands:**
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/commands/"
```

**Example - Execute command:**
```bash
curl -k -X POST -H "Authorization: Bearer $KEY" "$URL/commands/app:open-vault"
```

**Common command IDs:**
- `app:open-vault` - Open vault picker
- `command-palette:open` - Open command palette
- `daily-notes` - Create/open daily note
- `editor:save-file` - Save current file

---

### Open

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/open/{filename}` | Open file in Obsidian UI |

**Example:**
```bash
curl -k -X POST -H "Authorization: Bearer $KEY" "$URL/open/my-note.md"
```

---

### Tags

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tags/` | Get all tags with metadata |

**Example:**
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/tags/"
```

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created (new file) |
| 204 | Success (no content returned) |
| 404 | File not found |
| 403 | Authentication failed |
| 500 | Server error |

---

## Notes

- All paths relative to vault root
- File extensions `.md` required for markdown files
- Content-Type `text/markdown` for note content
- Use `-k` flag for self-signed SSL certificate
- API operates on currently active vault in Obsidian
- Periodic notes require Periodic Notes plugin enabled