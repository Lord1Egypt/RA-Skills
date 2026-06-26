---
name: nextcloud
description: File management, document understanding, and workflow intelligence for Nextcloud via WebDAV and OCS APIs. Use for uploading, downloading, listing, searching, extracting text, summarizing files, Q&A over files, extracting workflow actions, creating Exchange tasks from files, sharing, moving, and copying files and folders on Nextcloud. Triggers on phrases like "upload to nextcloud", "download from nextcloud", "list files on nextcloud", "search nextcloud", "summarize nextcloud file", "ask nextcloud file", "extract actions from file", "create tasks from file", "create nextcloud share link", "nextcloud file operations".
---

# Nextcloud Module

File management on Nextcloud server using WebDAV protocol and OCS sharing APIs.

## Requirements

- Nextcloud instance with WebDAV enabled
- App password (generate from Nextcloud security settings)

## Configuration

Set environment variables:

```bash
export NEXTCLOUD_URL="https://cloud.example.com"
export NEXTCLOUD_USERNAME="your-username"
export NEXTCLOUD_APP_PASSWORD="your-app-password"
```

## Commands

### shared
List folders shared with the current user.

```bash
python3 -m modules.nextcloud shared
```

Returns: Name, owner, permissions, and path for each shared folder.

### list
List files and folders in a directory.

```bash
python3 -m modules.nextcloud list /path/to/directory/
python3 -m modules.nextcloud list /path/to/directory/ --recursive
```

Returns: File name, type (file/folder), size, and last modified date.

### search
Search files and folders by name, recursively.

```bash
python3 -m modules.nextcloud search contract /Clients/
```

Returns: Matching files/folders with path, type, size, and last modified date.

### extract-text
Extract readable text from one supported file.

```bash
python3 -m modules.nextcloud extract-text /Clients/contract.docx
```

### summarize
Create a grounded summary for one file.

```bash
python3 -m modules.nextcloud summarize /Clients/contract.docx
```

### ask-file
Answer a question using one file as the source.

```bash
python3 -m modules.nextcloud ask-file /Clients/contract.docx "When is the renewal due?"
```

### extract-actions
Extract grounded workflow actions from one file.

```bash
python3 -m modules.nextcloud extract-actions /Clients/contract.txt
```

Returns: action items, due-date hints, owner hints, and source excerpts.

### create-tasks-from-file
Preview or create Exchange tasks from extracted file actions.

```bash
python3 -m modules.nextcloud create-tasks-from-file /Clients/contract.txt
python3 -m modules.nextcloud create-tasks-from-file /Clients/contract.txt --select 1,2 --execute
python3 -m modules.nextcloud create-tasks-from-file /Clients/contract.txt --mailbox user@example.com --execute
```

### upload
Upload a local file to Nextcloud.

```bash
python3 -m modules.nextcloud upload /local/file.txt /remote/directory/
```

### download
Download a file from Nextcloud to local filesystem.

```bash
python3 -m modules.nextcloud download /remote/file.txt /local/directory/
```

### mkdir
Create a new directory on Nextcloud.

```bash
python3 -m modules.nextcloud mkdir /new/folder/path/
```

### delete
Delete a file or directory on Nextcloud.

```bash
python3 -m modules.nextcloud delete /path/to/delete
```

### move
Move or rename a file or directory.

```bash
python3 -m modules.nextcloud move /old/path /new/path
```

### copy
Copy a file or directory.

```bash
python3 -m modules.nextcloud copy /source/path /destination/path
```

### info
Get detailed information about a file or directory.

```bash
python3 -m modules.nextcloud info /path/to/item
```

### share-create
Create a public share link for a file or folder.

```bash
python3 -m modules.nextcloud share-create /Contracts/offer.pdf
python3 -m modules.nextcloud share-create /Dropzones/Inbox --public-upload --expire-date 2026-04-30
```

### share-list
List public share links, optionally filtered by path.

```bash
python3 -m modules.nextcloud share-list
python3 -m modules.nextcloud share-list /Contracts/offer.pdf
```

### share-revoke
Revoke a public share link by share ID.

```bash
python3 -m modules.nextcloud share-revoke 42
```

## Error Handling

- Exit code 0: Success
- Exit code 1: Missing configuration or invalid command usage
- Exit code 3: Connection/authentication/operation error
- Exit code 4: File or directory not found (for info-like lookups)

## Notes

- Nextcloud WebDAV uses user ID (not username) in paths - the script resolves this automatically
- Search currently matches file/folder names and paths, not document content
- `extract-text`, `summarize`, `ask-file`, `extract-actions`, and `create-tasks-from-file` operate on one file at a time
- `create-tasks-from-file` is preview-first by default; use `--execute` to actually create Exchange tasks
- `--select 1,2,...` lets you approve only a subset of extracted task proposals
- PDF extraction uses `pdfplumber` (recommended, MIT license, best table/layout handling) with `pypdf` as fallback; install `pdfplumber` for best results
- Task creation uses Exchange delegate access when `--mailbox` is supplied
- Share-link commands use the Nextcloud OCS sharing API
- For large files, ensure sufficient timeout settings
- Self-signed certificates may require additional configuration
