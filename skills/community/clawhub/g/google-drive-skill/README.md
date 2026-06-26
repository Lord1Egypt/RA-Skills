# Google Drive Skill

A comprehensive skill providing patterns and ready-to-run scripts for CRUD operations on Google Drive using the **Google Drive API v3**.

## Overview

This skill enables seamless interaction with Google Drive through Python scripts. It supports:
- **Read-only access** (API key for public files)
- **Full read/write access** (service account authentication)
- Folder navigation, file management, permissions, and error handling

### Use Cases
- Integrate Google Drive into scripts and applications
- Read publicly shared files
- Automate CRUD operations on service-account-owned drives
- Manage Drive folder structures programmatically

## Project Structure

```
google-drive-skill/
├── README.md                           # This file
├── SKILL.md                            # Detailed skill documentation
├── assets/
│   └── service_account_template.json   # Service account credentials template
├── references/
│   ├── error_codes.md                  # HTTP error codes & retry patterns
│   └── mime_types.md                   # MIME type quick reference
└── scripts/
    ├── drive_client.py                 # Shared auth factory (imported by all)
    ├── list_files.py                   # List files/folders in a directory
    ├── download_file.py                # Download files from Drive
    ├── upload_file.py                  # Upload files to Drive
    ├── create_folder.py                # Create new folders
    ├── update_file.py                  # Rename, move, or update files
    ├── delete_file.py                  # Delete or trash files
    └── set_permissions.py              # Manage file permissions & sharing
```

## Quick Start

### 1. Install Dependencies

```bash
pip install google-api-python-client google-auth google-auth-httplib2
```

### 2. Set Up Credentials

**For read-only access (public files):**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

**For read/write access (service account):**
```bash
export GOOGLE_SERVICE_ACCOUNT_JSON="/path/to/service_account.json"
```

See `assets/service_account_template.json` for the expected JSON structure.

### 3. Run Scripts

```bash
# List files in a folder
python scripts/list_files.py --folder-id FOLDER_ID

# Download a file
python scripts/download_file.py --file-id FILE_ID --dest ./downloads/

# Upload a file
python scripts/upload_file.py --src ./report.pdf --parent-id FOLDER_ID

# Create a folder
python scripts/create_folder.py --name "New Folder"

# Update/rename a file
python scripts/update_file.py --file-id FILE_ID --name "Updated Name.pdf"

# Delete a file
python scripts/delete_file.py --file-id FILE_ID

# Manage permissions
python scripts/set_permissions.py --file-id FILE_ID --public
```

## Available Scripts

| Script | Operation | Auth Required |
|--------|-----------|---------------|
| `list_files.py` | List files/folders in a directory | API key or service account |
| `download_file.py` | Download a file to disk | API key or service account |
| `create_folder.py` | Create a new folder | Service account |
| `upload_file.py` | Upload a local file | Service account |
| `update_file.py` | Rename, move, or update content | Service account |
| `delete_file.py` | Trash or permanently delete | Service account |
| `set_permissions.py` | Make public / share / revoke access | Service account |

## Authentication Methods

### API Key (Read-Only)
Use for public, shared files when you only need read access.

```python
from googleapiclient.discovery import build
import os

API_KEY = os.environ["GOOGLE_API_KEY"]
drive = build("drive", "v3", developerKey=API_KEY)
```

### Service Account (Read/Write)
Use when you need to create, modify, or delete files.

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

## Finding File & Folder IDs

Every Drive resource has a unique `fileId`. Extract it from the share URL:

```
Folder: https://drive.google.com/drive/folders/FOLDER_ID_HERE
File:   https://drive.google.com/file/d/FILE_ID_HERE/view
```

## Common Operations

### List Files
```bash
python scripts/list_files.py --folder-id FOLDER_ID
python scripts/list_files.py --folder-id FOLDER_ID --json  # JSON output
```

### Download Files
```bash
# Save to specific path
python scripts/download_file.py --file-id FILE_ID --dest ./report.pdf

# Save to directory (auto filename)
python scripts/download_file.py --file-id FILE_ID --dest ./downloads/
```

### Create Folders
```bash
# In Drive root
python scripts/create_folder.py --name "My New Folder"

# In a specific parent folder
python scripts/create_folder.py --name "Subfolder" --parent-id PARENT_FOLDER_ID
```

### Upload Files
```bash
# Basic upload
python scripts/upload_file.py --src ./report.pdf --parent-id FOLDER_ID

# Custom name and make public
python scripts/upload_file.py --src ./photo.png --name "Photo.png" --parent-id FOLDER_ID --make-public
```

### Update Files
```bash
# Rename
python scripts/update_file.py --file-id FILE_ID --name "New Name.pdf"

# Move to different folder
python scripts/update_file.py --file-id FILE_ID --move-to NEW_PARENT_ID --old-parent OLD_PARENT_ID

# Replace content
python scripts/update_file.py --file-id FILE_ID --src ./updated.pdf
```

### Delete Files
```bash
# Move to trash
python scripts/delete_file.py --file-id FILE_ID

# Permanently delete (with confirmation)
python scripts/delete_file.py --file-id FILE_ID --permanent

# Permanently delete (non-interactive)
python scripts/delete_file.py --file-id FILE_ID --permanent --yes
```

### Manage Permissions
```bash
# Make file publicly readable
python scripts/set_permissions.py --file-id FILE_ID --public

# Share with a user as writer
python scripts/set_permissions.py --file-id FILE_ID --email user@example.com --role writer

# Share as reader
python scripts/set_permissions.py --file-id FILE_ID --email user@example.com --role reader

# List current permissions
python scripts/set_permissions.py --file-id FILE_ID --list

# Remove a permission
python scripts/set_permissions.py --file-id FILE_ID --remove PERMISSION_ID
```

## References

- **[error_codes.md](references/error_codes.md)** — HTTP error codes and retry patterns
- **[mime_types.md](references/mime_types.md)** — MIME type quick reference
- **[SKILL.md](SKILL.md)** — Complete skill documentation and code patterns

## Security Best Practices

1. **Never commit credentials** — Always store `service_account.json` outside the repository
2. **Use `.gitignore`** — Add service account files to `.gitignore`
3. **Rotate service accounts** — Follow Google Cloud security policies
4. **Limit permissions** — Grant only necessary Drive API scopes to service accounts

## Troubleshooting

- **Authentication errors**: Verify environment variables are set correctly
- **Permission denied**: Check that your service account has access to the target files/folders
- **Not found errors**: Confirm file/folder IDs are correct
- See [error_codes.md](references/error_codes.md) for detailed error handling

## For More Information

See [SKILL.md](SKILL.md) for comprehensive documentation including:
- Detailed CRUD operation patterns
- Advanced usage examples
- Error handling strategies
- Full script documentation
