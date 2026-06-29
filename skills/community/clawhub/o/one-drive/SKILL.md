---
name: one-drive
description: |
  OneDrive API integration with managed OAuth via Microsoft Graph. Manage files, folders, and sharing.
  Use this skill when users want to upload, download, organize, or share files in OneDrive.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# OneDrive

Access the OneDrive API with managed OAuth authentication via Microsoft Graph. Manage files, folders, drives, and sharing with full CRUD operations.

## Quick Start

**CLI:**

```bash
maton one-drive item list
```

```bash
maton api '/one-drive/v1.0/me/drive/root/children'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/one-drive/v1.0/me/drive/root/children')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/one-drive/v1.0/{resource}
```

Maton proxies requests to `graph.microsoft.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your OneDrive OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list one-drive --status ACTIVE
```

```bash
maton api -X GET /connections -f app=one-drive -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=one-drive&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create one-drive
```

```bash
maton api /connections -f app=one-drive
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'one-drive'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T08:23:30.317909Z",
    "last_updated_time": "2026-02-07T08:24:04.925298Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "one-drive",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple OneDrive connections, specify which one to use:

**CLI:**

```bash
maton one-drive item list --connection {connection_id}
```

```bash
maton api /one-drive/v1.0/me/drive/root/children --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/one-drive/v1.0/me/drive')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to files, folders, and sharing within the connected OneDrive account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Drives

#### Get Current User's Drive

```bash
GET /one-drive/v1.0/me/drive
```

Example:

```bash
maton one-drive whoami
```

#### List User's Drives

```bash
GET /one-drive/v1.0/me/drives
```

Example:

```bash
maton one-drive drive list
```

#### Get Drive by ID

```bash
GET /one-drive/v1.0/drives/{drive-id}
```

Example:

```bash
maton one-drive drive view {drive-id}
```

### Files and Folders

#### Get Drive Root

```bash
GET /one-drive/v1.0/me/drive/root
```

Example:

```bash
maton one-drive item view root
```

#### List Root Children

```bash
GET /one-drive/v1.0/me/drive/root/children
```

Example:

```bash
maton one-drive item list
```

#### Get Item by ID

```bash
GET /one-drive/v1.0/me/drive/items/{item-id}
```

Example:

```bash
maton one-drive item view {item-id}
```

#### Get Item by Path

Use colon (`:`) syntax to access items by path:

```bash
GET /one-drive/v1.0/me/drive/root:/Documents/report.pdf
```

Example:

```bash
maton one-drive item view-by-path Documents/report.pdf
```

#### List Folder Children by Path

```bash
GET /one-drive/v1.0/me/drive/root:/Documents:/children
```

Example:

```bash
maton one-drive item list Documents
```

#### Get Item Children

```bash
GET /one-drive/v1.0/me/drive/items/{item-id}/children
```

Example:

```bash
maton one-drive item view {item-id} --expand children
```

### Special Folders

Access known folders by name:

```bash
GET /one-drive/v1.0/me/drive/special/documents
GET /one-drive/v1.0/me/drive/special/photos
GET /one-drive/v1.0/me/drive/special/music
GET /one-drive/v1.0/me/drive/special/approot
```

Example:

```bash
maton one-drive item view --special documents
```

### Recent and Shared

#### Get Recent Files

```bash
GET /one-drive/v1.0/me/drive/recent
```

Example:

```bash
maton one-drive drive recent
```

#### Get Files Shared With Me

```bash
GET /one-drive/v1.0/me/drive/sharedWithMe
```

Example:

```bash
maton one-drive drive shared
```

### Search

```bash
GET /one-drive/v1.0/me/drive/root/search(q='budget')
```

Example:

```bash
maton one-drive drive search 'budget'
```

### Create Folder

```bash
POST /one-drive/v1.0/me/drive/root:/Documents:/children
Content-Type: application/json

{
  "name": "Reports",
  "folder": {},
  "@microsoft.graph.conflictBehavior": "rename"
}
```

Example:

```bash
maton one-drive item create-folder Reports --path Documents
```

Create folder inside another folder by parent ID:
```bash
POST /one-drive/v1.0/me/drive/items/{parent-id}/children
Content-Type: application/json

{
  "name": "Reports",
  "folder": {}
}
```

Example:

```bash
maton one-drive item create-folder Reports --parent-id {parent-id}
```

### Upload File (Simple - up to 4MB)

```bash
PUT /one-drive/v1.0/me/drive/root:/Documents/report.pdf:/content
Content-Type: application/pdf

{report.pdf binary content}
```

Example:

```bash
maton one-drive item upload ./report.pdf --path Documents/report.pdf
```

### Upload File (Large - resumable)

For files over 4MB, use resumable upload:

**Step 1: Create upload session**
```bash
POST /one-drive/v1.0/me/drive/root:/large-report.pdf:/createUploadSession
Content-Type: application/json

{
  "item": {
    "@microsoft.graph.conflictBehavior": "rename"
  }
}
```

Example:

```bash
maton one-drive item upload ./large-report.pdf --path large-report.pdf --conflict rename
```

Files larger than 4 MiB automatically use a resumable upload session.

**Response:**
```json
{
  "uploadUrl": "https://sn3302.up.1drv.com/up/...",
  "expirationDateTime": "2024-02-08T10:00:00Z"
}
```

**Step 2: Upload bytes to the uploadUrl**

### Download File

Get the file metadata to retrieve the download URL:

```bash
GET /one-drive/v1.0/me/drive/items/{item-id}
```

Example:

```bash
maton one-drive item view {item-id}
```

The response includes `@microsoft.graph.downloadUrl` - a pre-authenticated URL valid for a short time:

```json
{
  "id": "...",
  "name": "document.pdf",
  "@microsoft.graph.downloadUrl": "https://public-sn3302.files.1drv.com/..."
}
```

Use this URL directly to download the file content (no auth header needed).

### Update Item (Rename/Move)

```bash
PATCH /one-drive/v1.0/me/drive/items/{item-id}
Content-Type: application/json

{
  "name": "new-name.txt"
}
```

Example:

```bash
maton one-drive item update {item-id} --name new-name.txt
```

Move to different folder:
```bash
PATCH /one-drive/v1.0/me/drive/items/{item-id}
Content-Type: application/json

{
  "parentReference": {
    "id": "{new-parent-id}"
  }
}
```

Example:

```bash
maton one-drive item move {item-id} --dest-id {new-parent-id}
```

### Copy Item

```bash
POST /one-drive/v1.0/me/drive/items/{item-id}/copy
Content-Type: application/json

{
  "parentReference": {
    "id": "{destination-folder-id}"
  },
  "name": "copied-file.txt"
}
```

Example:

```bash
maton one-drive item copy {item-id} --dest-id {destination-folder-id} --name copied-file.txt
```

Returns `202 Accepted` with a `Location` header to monitor the copy operation.

### Delete Item

```bash
DELETE /one-drive/v1.0/me/drive/items/{item-id}
```

Example:

```bash
maton one-drive item delete {item-id}
```

Returns `204 No Content` on success.

### Sharing

#### Create Sharing Link

```bash
POST /one-drive/v1.0/me/drive/items/01ABCDEF/createLink
Content-Type: application/json

{
  "type": "view",
  "scope": "anonymous"
}
```

Link types:
- `view` - Read-only access
- `edit` - Read-write access
- `embed` - Embeddable link

Scopes:
- `anonymous` - Anyone with the link
- `organization` - Anyone in your organization

Example:

```bash
maton one-drive item share 01ABCDEF --type view --scope anonymous
```

#### Invite Users (Share with specific people)

```bash
POST /one-drive/v1.0/me/drive/items/{item-id}/invite
Content-Type: application/json

{
  "recipients": [
    {"email": "user@example.com"}
  ],
  "roles": ["read"],
  "sendInvitation": true,
  "message": "Check out this file!"
}
```

Example:

```bash
maton one-drive item invite {item-id} --emails user@example.com --roles read --message 'Check out this file!'
```

## Query Parameters

Customize responses with OData query parameters:

- `$select` - Choose specific properties: `?$select=id,name,size`
- `$expand` - Include related resources: `?$expand=children`
- `$filter` - Filter results: `?$filter=file ne null` (files only)
- `$orderby` - Sort results: `?$orderby=name asc`
- `$top` - Limit results: `?$top=10`

Example:
```bash
GET /one-drive/v1.0/me/drive/root/children?$select=id,name,size&$top=20&$orderby=name%20asc
```

```bash
maton one-drive item list --select id,name,size --top 20 --orderby 'name asc'
```

## Pagination

OneDrive uses cursor-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton one-drive item list --paginate
```

## Code Examples

### CLI

```bash
# Search for files
maton one-drive drive search 'budget'

# Share a file
maton one-drive item share 01ABCDEF --type view --scope anonymous

# Extract specific fields with --jq (requires --json)
maton one-drive item view root --json --jq '.name'
```

### JavaScript

```javascript
// List files in root
const response = await fetch(
  'https://api.maton.ai/one-drive/v1.0/me/drive/root/children',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();

// Upload a file
const uploadResponse = await fetch(
  'https://api.maton.ai/one-drive/v1.0/me/drive/root:/myfile.txt:/content',
  {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'text/plain'
    },
    body: 'Hello, OneDrive!'
  }
);
```

### Python

```python
import os
import requests

# List files in root
response = requests.get(
    'https://api.maton.ai/one-drive/v1.0/me/drive/root/children',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
files = response.json()

# Upload a file
upload_response = requests.put(
    'https://api.maton.ai/one-drive/v1.0/me/drive/root:/myfile.txt:/content',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'text/plain'
    },
    data='Hello, OneDrive!'
)
```

## Notes

- OneDrive uses Microsoft Graph API (`graph.microsoft.com`)
- Item IDs are unique within a drive
- Use colon (`:`) syntax for path-based addressing: `/root:/path/to/file`
- Files ≤4MB upload via a single PUT; larger files automatically use a resumable upload session
- Download URLs from `@microsoft.graph.downloadUrl` are pre-authenticated and temporary
- Conflict behavior options: `fail`, `replace`, `rename`
- On personal OneDrive accounts, only the user's own drive ID (returned by `whoami`) is directly addressable. The additional `b!...`-prefixed IDs that appear in `drive list` return HTTP 400 from Microsoft Graph when fetched this way. Use `me/drive` instead.
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing OneDrive connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions |
| 404 | Item not found |
| 409 | Conflict (e.g., item already exists) |
| 429 | Rate limited (check `Retry-After` header) |
| 4xx/5xx | Passthrough error from Microsoft Graph API |

### Error Response Format

```json
{
  "error": {
    "code": "itemNotFound",
    "message": "The resource could not be found."
  }
}
```

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `one-drive`. For example:

- Correct: `https://api.maton.ai/one-drive/v1.0/me/drive/root/children`
- Incorrect: `https://api.maton.ai/v1.0/me/drive/root/children`

## Resources

- [OneDrive Developer Documentation](https://learn.microsoft.com/en-us/onedrive/developer/)
- [Microsoft Graph API Reference](https://learn.microsoft.com/en-us/graph/api/overview)
- [DriveItem Resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [Drive Resource](https://learn.microsoft.com/en-us/graph/api/resources/drive)
- [Sharing and Permissions](https://learn.microsoft.com/en-us/onedrive/developer/rest-api/concepts/sharing)
- [Large File Upload](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
