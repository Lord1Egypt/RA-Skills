---
name: google-drive-skill
description: |
  Use when the user wants to interact with a public Google Drive — listing, reading, creating, updating, or deleting files and folders.
  Handles both read-only access (API key only) and write access (service account or OAuth2).
  Covers folder navigation, file upload/download, permissions, MIME types, and error handling.
  USE FOR: integrating Google Drive into scripts or applications; reading publicly shared files; CRUD on service-account-owned drives; automating Drive folder structures.
  DO NOT USE FOR: Google Workspace Admin tasks; Google Docs/Sheets API-specific operations beyond Drive metadata.
---

# Google Drive Skill

## Resolve `SKILL_SCRIPTS`

**IMPORTANT:** All commands below use `SKILL_SCRIPTS` as shorthand for the absolute path to the `scripts/` directory of this skill. Resolve it before running any script:

```bash
SKILL_SCRIPTS="$(
  _ws_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  _ws_path="$_ws_root/.github/skills/google-drive-skill/scripts"
  _global_path="$HOME/.openclaw/workspace/skills/google-drive-skill/scripts"
  _global_path2="$HOME/.openclaw/skills/google-drive-skill/scripts"

  if [ -d "$_ws_path" ]; then
    echo "$_ws_path"
  elif [ -d "$_global_path" ]; then
    echo "$_global_path"
  elif [ -d "$_global_path2" ]; then
    echo "$_global_path2"
  else
    find "$HOME" /opt -type d -name google-drive-skill -path '*/skills/*' 2>/dev/null \
      | head -1 | sed 's|$|/scripts|'
  fi
)"
echo "SKILL_SCRIPTS=$SKILL_SCRIPTS"
```

---

## Overview

This skill provides patterns and **ready-to-run scripts** for CRUD operations on Google Drive using the **Drive API v3**.

| Script | Operation | Auth Required |
|--------|-----------|---------------|
| `list_files.py` | List files/folders in a folder | API key (public) or service account |
| `download_file.py` | Download a file to disk | API key (public) or service account |
| `create_folder.py` | Create a new folder | Service account |
| `upload_file.py` | Upload a local file | Service account |
| `update_file.py` | Rename, move, or replace content | Service account |
| `delete_file.py` | Trash or permanently delete | Service account |
| `set_permissions.py` | Make public / share / revoke | Service account |

**Supporting files:**
- `scripts/drive_client.py` — shared auth factory (imported by all scripts)
- `assets/service_account_template.json` — template for your service account JSON
- `references/mime_types.md` — MIME type quick reference
- `references/error_codes.md` — HTTP error codes + retry patterns

---

## Quick Start

### 1. Install dependencies

```bash
pip install google-api-python-client google-auth google-auth-httplib2
```

### 2. Set credentials

```bash
# Read-only (public files):
export GOOGLE_API_KEY="your_api_key_here"

# Read + write (service account):
export GOOGLE_SERVICE_ACCOUNT_JSON="/path/to/service_account.json"
```

See `assets/service_account_template.json` for the expected JSON structure.

### 3. Resolve `SKILL_SCRIPTS` (see top of this file), then run scripts

---

## Script Commands

### List files in a folder

```bash
# Table output (default):
python "$SKILL_SCRIPTS/list_files.py" --folder-id FOLDER_ID

# JSON output:
python "$SKILL_SCRIPTS/list_files.py" --folder-id FOLDER_ID --json
```

### Download a file

```bash
# Save to specific path:
python "$SKILL_SCRIPTS/download_file.py" --file-id FILE_ID --dest ./downloads/report.pdf

# Save to directory (auto filename from Drive):
python "$SKILL_SCRIPTS/download_file.py" --file-id FILE_ID --dest ./downloads/
```

### Create a folder

```bash
# In Drive root:
python "$SKILL_SCRIPTS/create_folder.py" --name "My New Folder"

# Inside a specific parent folder:
python "$SKILL_SCRIPTS/create_folder.py" --name "Subfolder" --parent-id PARENT_FOLDER_ID
```

### Upload a file

```bash
# Basic upload (MIME type auto-detected):
python "$SKILL_SCRIPTS/upload_file.py" --src ./report.pdf --parent-id FOLDER_ID

# Custom name on Drive:
python "$SKILL_SCRIPTS/upload_file.py" --src ./report.pdf --name "Q1-Report.pdf" --parent-id FOLDER_ID

# Upload and make publicly readable immediately:
python "$SKILL_SCRIPTS/upload_file.py" --src ./photo.png --parent-id FOLDER_ID --make-public
```

### Update a file

```bash
# Rename:
python "$SKILL_SCRIPTS/update_file.py" --file-id FILE_ID --name "New Name.pdf"

# Move to a different folder:
python "$SKILL_SCRIPTS/update_file.py" --file-id FILE_ID --move-to NEW_PARENT_ID --old-parent OLD_PARENT_ID

# Replace file content:
python "$SKILL_SCRIPTS/update_file.py" --file-id FILE_ID --src ./updated_report.pdf

# Rename + replace content:
python "$SKILL_SCRIPTS/update_file.py" --file-id FILE_ID --name "v2.pdf" --src ./v2.pdf
```

### Delete or trash a file

```bash
# Move to trash (safe, recoverable):
python "$SKILL_SCRIPTS/delete_file.py" --file-id FILE_ID

# Permanently delete (prompts for confirmation):
python "$SKILL_SCRIPTS/delete_file.py" --file-id FILE_ID --permanent

# Permanently delete (non-interactive):
python "$SKILL_SCRIPTS/delete_file.py" --file-id FILE_ID --permanent --yes
```

### Manage permissions

```bash
# Make file publicly readable (anyone with link):
python "$SKILL_SCRIPTS/set_permissions.py" --file-id FILE_ID --public

# Share with a user as writer:
python "$SKILL_SCRIPTS/set_permissions.py" --file-id FILE_ID --email user@example.com --role writer

# Share with a user as reader:
python "$SKILL_SCRIPTS/set_permissions.py" --file-id FILE_ID --email user@example.com --role reader

# List current permissions (returns JSON):
python "$SKILL_SCRIPTS/set_permissions.py" --file-id FILE_ID --list

# Remove a specific permission:
python "$SKILL_SCRIPTS/set_permissions.py" --file-id FILE_ID --remove PERMISSION_ID
```

---

## Auth Setup

### Option A — API Key (read-only public files)

Use when the file/folder is shared as **"Anyone with the link"** and you only need to **read**.

```python
from googleapiclient.discovery import build

API_KEY = os.environ["GOOGLE_API_KEY"]
drive = build("drive", "v3", developerKey=API_KEY)
```

### Option B — Service Account (read + write on shared/public drives)

Use when you need to **create, modify, or delete** files.

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"], scopes=SCOPES
)
drive = build("drive", "v3", credentials=creds)
```

> Copy `assets/service_account_template.json` to see the expected structure.  
> Store the real file outside the repo and never commit it.  
> Add `service_account.json` to `.gitignore`.

---

## File & Folder ID

Every Drive resource has a unique `fileId`. Extract it from the share URL:

```
https://drive.google.com/drive/folders/FOLDER_ID_HERE
https://drive.google.com/file/d/FILE_ID_HERE/view
```

---

## CRUD Operations

### List Files in a Public Folder

```python
def list_files(drive, folder_id: str) -> list[dict]:
    results = []
    page_token = None
    while True:
        resp = drive.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        results.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return results
```

### Download a Public File

```python
import io
from googleapiclient.http import MediaIoBaseDownload

def download_file(drive, file_id: str, dest_path: str) -> None:
    request = drive.files().get_media(fileId=file_id, supportsAllDrives=True)
    with open(dest_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
```

### Create a Folder

```python
def create_folder(drive, name: str, parent_id: str | None = None) -> str:
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = drive.files().create(
        body=metadata,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return folder["id"]
```

### Upload / Create a File

```python
from googleapiclient.http import MediaFileUpload

def upload_file(
    drive,
    local_path: str,
    name: str,
    parent_id: str | None = None,
    mime_type: str = "application/octet-stream",
) -> str:
    metadata = {"name": name}
    if parent_id:
        metadata["parents"] = [parent_id]
    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
    file = drive.files().create(
        body=metadata,
        media_body=media,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return file["id"]
```

### Upload from In-Memory Bytes

```python
from googleapiclient.http import MediaIoBaseUpload

def upload_bytes(
    drive,
    data: bytes,
    name: str,
    parent_id: str | None = None,
    mime_type: str = "application/octet-stream",
) -> str:
    metadata = {"name": name}
    if parent_id:
        metadata["parents"] = [parent_id]
    media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mime_type, resumable=True)
    file = drive.files().create(
        body=metadata,
        media_body=media,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return file["id"]
```

### Update File Metadata (rename, move)

```python
def rename_file(drive, file_id: str, new_name: str) -> None:
    drive.files().update(
        fileId=file_id,
        body={"name": new_name},
        supportsAllDrives=True,
    ).execute()

def move_file(drive, file_id: str, new_parent_id: str, old_parent_id: str) -> None:
    drive.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=old_parent_id,
        fields="id, parents",
        supportsAllDrives=True,
    ).execute()
```

### Update File Content

```python
def update_file_content(
    drive,
    file_id: str,
    local_path: str,
    mime_type: str = "application/octet-stream",
) -> None:
    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
    drive.files().update(
        fileId=file_id,
        media_body=media,
        supportsAllDrives=True,
    ).execute()
```

### Delete a File or Folder

```python
def delete_file(drive, file_id: str) -> None:
    drive.files().delete(fileId=file_id, supportsAllDrives=True).execute()
```

> Deleting a folder also deletes all its children permanently. Prefer trashing:
> ```python
> drive.files().update(fileId=file_id, body={"trashed": True}).execute()
> ```

---

## Set Permissions (Make Public)

To make a file publicly readable (anyone with the link):

```python
def make_public(drive, file_id: str) -> None:
    drive.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
        supportsAllDrives=True,
    ).execute()
```

To grant write access to a specific user:

```python
def share_with_user(drive, file_id: str, email: str, role: str = "writer") -> None:
    # role: "reader", "commenter", "writer", "fileOrganizer", "organizer", "owner"
    drive.permissions().create(
        fileId=file_id,
        body={"role": role, "type": "user", "emailAddress": email},
        sendNotificationEmail=False,
        supportsAllDrives=True,
    ).execute()
```

---

## Common MIME Types

| Content | MIME Type |
|---------|-----------|
| Folder | `application/vnd.google-apps.folder` |
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| PDF | `application/pdf` |
| Plain text | `text/plain` |
| JSON | `application/json` |
| PNG | `image/png` |
| ZIP | `application/zip` |

---

## Error Handling

```python
from googleapiclient.errors import HttpError

def safe_delete(drive, file_id: str) -> bool:
    try:
        drive.files().delete(fileId=file_id, supportsAllDrives=True).execute()
        return True
    except HttpError as e:
        if e.resp.status == 404:
            return False  # already gone
        raise
```

Common HTTP status codes:
- `400` — bad request (check field names, MIME types)
- `403` — permission denied (check auth scope or file sharing settings)
- `404` — file not found (check `fileId`, `supportsAllDrives`)
- `429` — rate limited (back off and retry)

---

## Required Python Packages

```
google-api-python-client>=2.100.0
google-auth>=2.23.0
google-auth-httplib2>=0.1.1
```

Install:
```bash
pip install google-api-python-client google-auth google-auth-httplib2
```

---

## Security Notes

- Never hardcode API keys or service account credentials in source code. Use environment variables or secret managers.
- Restrict API key to the Drive API scope in the Google Cloud Console.
- Service account credentials (`service_account.json`) must be in `.gitignore`.
- When sharing files, prefer time-limited access tokens over permanent public links where possible.
- `"type": "anyone"` with `"role": "writer"` on a production folder is dangerous — audit permissions regularly.

---

## Reference

**Local references (this skill):**
- [references/mime_types.md](references/mime_types.md) — full MIME type table
- [references/error_codes.md](references/error_codes.md) — HTTP errors, Drive reasons, retry pattern
- [assets/service_account_template.json](assets/service_account_template.json) — service account JSON structure

**Official docs:**
- [Drive API v3 documentation](https://developers.google.com/drive/api/v3/reference)
- [Python client library](https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html)
- [Service accounts guide](https://developers.google.com/identity/protocols/oauth2/service-account)
- [Drive MIME types](https://developers.google.com/drive/api/guides/mime-types)
