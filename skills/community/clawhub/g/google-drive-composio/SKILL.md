---
name: google-drive
description: Browse Google Drive folders and read the files inside them. Use when the user points at a Drive folder or file, asks for data stored in Drive (CSV/Excel/PDF exports, shared reports), or wants files organised, uploaded, or shared in Drive. Uses Composio for OAuth so no client-side Google credentials are needed.
metadata:
  {
    "openclaw":
      {
        "requires": { "python": ["composio"] },
        "env":
          {
            "COMPOSIO_API_KEY": "Your Composio API key (from https://app.composio.dev/).",
            "COMPOSIO_USER_ID": "Any stable identifier for the Google account you connected in Composio (email, user ID, tenant ID — anything, as long as it matches the user_id you used when connecting)."
          }
      }
  }
---

# Google Drive Integration Skill

Composio-powered Google Drive skill. All OAuth is handled by [Composio](https://composio.dev/) — you never see or store Google tokens, and the skill works the same whether the connected account is a personal Gmail or a Workspace account.

## Setup (one-time)

1. **Get a Composio API key** — sign up at https://app.composio.dev/ and copy your API key.
2. **Connect Google Drive in Composio** — from the Composio dashboard, connect the Google Drive integration for a `user_id` of your choice (any string; e.g. your email or an internal tenant ID). Complete the Google OAuth flow.
3. **Install the Python client** — `pip install composio` (or let the platform install it via the `requires.python` metadata above).
4. **Export env vars** before running the skill:

   ```bash
   export COMPOSIO_API_KEY="ak_..."
   export COMPOSIO_USER_ID="the-user-id-you-used-in-step-2"
   ```

   If the skill runs on a platform that auto-injects Composio credentials, these are set for you — no manual export needed.

`TENANT_ID` is also accepted as a fallback for `COMPOSIO_USER_ID` (for platforms that already set that name).

## Usage

Run the `google_drive_api.py` script via Bash for all Google Drive operations:

```bash
python skills/google-drive/google_drive_api.py <command> [options]
```

## Commands

### Discovery

```bash
# List files in a folder (defaults to My Drive root)
python skills/google-drive/google_drive_api.py list --folder-id FOLDER_ID --page-size 50 --order-by "modifiedTime desc"

# Search by name substring, MIME type, or a raw Drive query
python skills/google-drive/google_drive_api.py search --name-contains "weekly sales"
python skills/google-drive/google_drive_api.py search --mime-type "text/csv" --folder-id FOLDER_ID
python skills/google-drive/google_drive_api.py search --query "name contains 'depletions' and modifiedTime > '2026-01-01T00:00:00'"

# Find folders by name or parent
python skills/google-drive/google_drive_api.py find-folder --name "Retail Reports"
python skills/google-drive/google_drive_api.py find-folder --name-contains "2026" --parent-id FOLDER_ID

# List shared drives the account can see
python skills/google-drive/google_drive_api.py shared-drives
```

Add `--all-drives` to `list` and `search` when the files live in a shared (team) drive rather than My Drive.

### Metadata

```bash
# File or folder metadata (name, mimeType, size, modifiedTime, parents)
python skills/google-drive/google_drive_api.py info --file-id FILE_ID

# Who has access to a file
python skills/google-drive/google_drive_api.py permissions --file-id FILE_ID
```

### Reading File Content

```bash
# Download a binary/uploaded file (CSV, XLSX, PDF, ...) into the workspace
python skills/google-drive/google_drive_api.py download --file-id FILE_ID --save-to data/report.csv

# Export a Google-native file to a concrete format
python skills/google-drive/google_drive_api.py export --file-id FILE_ID --mime-type text/csv --save-to data/sheet.csv
```

`--save-to` writes the bytes to a local path in the workspace so you can parse them with Python (`pandas.read_csv`, `openpyxl`, ...). Without it, the command only prints the Composio file reference.

**Export MIME types for Google-native files:**

| Source | Format | `--mime-type` |
|--------|--------|---------------|
| Google Sheet | CSV (first tab) | `text/csv` |
| Google Sheet | Excel | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Google Doc | Plain text | `text/plain` |
| Google Doc | PDF | `application/pdf` |
| Google Slides | PDF | `application/pdf` |

### Writing & Organising

```bash
# Create a folder
python skills/google-drive/google_drive_api.py create-folder --name "Q3 Reports" --parent-id PARENT_ID

# Create a text file (CSV, TXT, MD) from a string or a local file
python skills/google-drive/google_drive_api.py create-file --name "summary.csv" --from-file out/summary.csv --parent-id FOLDER_ID --mime-type text/csv

# Rename / re-describe
python skills/google-drive/google_drive_api.py update-file --file-id FILE_ID --name "2026-07 depletions.csv"

# Move, copy, trash
python skills/google-drive/google_drive_api.py move --file-id FILE_ID --to-folder-id FOLDER_ID
python skills/google-drive/google_drive_api.py copy --file-id FILE_ID --name "backup.csv" --to-folder-id FOLDER_ID
python skills/google-drive/google_drive_api.py trash --file-id FILE_ID

# Share with a person or a domain
python skills/google-drive/google_drive_api.py share --file-id FILE_ID --type user --role reader --email person@example.com
```

## Workflow Tips

- **Folder first, then files**: `find-folder` to resolve a folder name to an ID, then `list --folder-id` to see what is inside, then `download`/`export` the file you need.
- **Extract IDs from URLs**: folder IDs come after `/folders/`, file IDs sit between `/d/` and `/edit` or in the `?id=` param.
- **Check `mimeType` before reading**: Google-native files (`application/vnd.google-apps.*`) must be exported, not downloaded. Uploaded files (CSV, XLSX, PDF) use `download`.
- **Spreadsheets**: for a Google Sheet you need to read cell-by-cell or write back to, use a dedicated Google Sheets skill with the same file ID — `export --mime-type text/csv` only gives you a flat snapshot of the first tab.
- **Bound your listings**: pass `--page-size` on big folders and page through with `--page-token` instead of pulling everything at once.
- **Shared drives**: if a file the user can see is missing from results, retry with `--all-drives`.

## Cross-Integration Workflows

- **Drive → analysis**: `download --save-to` a CSV/XLSX, then parse it with pandas and load it wherever it belongs.
- **Any integration → Drive**: pull data with the source CLI, write a CSV locally, then `create-file --from-file` into a Drive folder to share.
- **Drive → Sheets**: `info` a Google Sheet found in Drive, then hand its ID to a Google Sheets skill for structured reads and writes.

## Important Notes

- **Composio-powered**: This integration uses [Composio](https://composio.dev/) for OAuth and API execution. Tokens are managed automatically — you never see a Google refresh token in your env.
- **Output**: JSON to stdout. Commands return `{"success": true, "data": {...}}` (plus `saved_to` when `--save-to` is used) or `{"success": false, "error": "...", "slug": "..."}` with a non-zero exit code.
- **Access scope**: the agent only sees what the connected Google account can see. "Not found" usually means the file was never shared with that account, not that it doesn't exist.
- **Large files**: downloads land in the workspace filesystem — prefer exporting a CSV slice over pulling multi-hundred-MB originals.
- **Safety**: always confirm with the user before trashing, moving, overwriting, or sharing files — sharing changes who outside the org can read the data.
