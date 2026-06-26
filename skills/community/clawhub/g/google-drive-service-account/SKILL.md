---
name: google-drive-service-account
description: Access Google Drive from OpenClaw using either GOOGLE_SERVICE_ACCOUNT_KEY service-account JSON or a GOOGLE_OAUTH_REFRESH_TOKEN from the Google Drive OAuth connector.
metadata:
  {
    "openclaw":
      {
        "emoji": "🗂️",
        "requires":
          {
            "bins": ["python3", "openssl"],
            "env":
              [
                "GOOGLE_SERVICE_ACCOUNT_KEY",
                "GOOGLE_OAUTH_REFRESH_TOKEN",
                "GOOGLE_CLIENT_ID",
                "GOOGLE_CLIENT_SECRET",
              ],
          },
        "primaryEnv": "GOOGLE_OAUTH_REFRESH_TOKEN",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Google Drive

Use this skill when Google Drive access is available through either:

- `GOOGLE_SERVICE_ACCOUNT_KEY` for service-account auth
- `GOOGLE_OAUTH_REFRESH_TOKEN` for the dashboard Google Drive OAuth connector

OAuth mode also needs `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` so the refresh token can be exchanged for an access token.

This skill is for:

- Searching Drive files and folders
- Listing folder contents
- Inspecting file metadata
- Downloading binary files
- Exporting Google Docs, Sheets, and Slides to standard formats
- Uploading files or creating folders

Important behavior:

- The script prefers `GOOGLE_OAUTH_REFRESH_TOKEN` when present, then falls back to `GOOGLE_SERVICE_ACCOUNT_KEY`.
- A service account only sees files it owns, files explicitly shared with the service account email, or a delegated user's Drive when domain-wide delegation is configured.
- If your workspace uses domain-wide delegation, set `GOOGLE_DRIVE_SUBJECT=user@company.com` or pass `--subject user@company.com`.
- For automation and tool use, prefer `--json`.

## Quick Start

Check access:

```bash
python3 {baseDir}/scripts/gdrive_sa.py whoami
```

Search files:

```bash
python3 {baseDir}/scripts/gdrive_sa.py search "name contains 'Q1'" --limit 10
python3 {baseDir}/scripts/gdrive_sa.py search "'root' in parents" --limit 25 --json
```

List a folder:

```bash
python3 {baseDir}/scripts/gdrive_sa.py ls root --limit 50
python3 {baseDir}/scripts/gdrive_sa.py ls <folderId> --json
```

Inspect metadata:

```bash
python3 {baseDir}/scripts/gdrive_sa.py info <fileId>
```

Download or export:

```bash
python3 {baseDir}/scripts/gdrive_sa.py download <fileId> --out /tmp/file.bin
python3 {baseDir}/scripts/gdrive_sa.py export <fileId> --mime text/plain --out /tmp/doc.txt
python3 {baseDir}/scripts/gdrive_sa.py cat <fileId> --mime text/plain
```

Create folders and upload files:

```bash
python3 {baseDir}/scripts/gdrive_sa.py mkdir "Reports" --parent root
python3 {baseDir}/scripts/gdrive_sa.py upload ./report.pdf --parent <folderId>
python3 {baseDir}/scripts/gdrive_sa.py upload ./notes.txt --name "meeting-notes.txt" --parent root
```

## Query Tips

Drive search uses the standard Drive query syntax in the `q` parameter. Useful examples:

- `name contains 'invoice'`
- `mimeType = 'application/vnd.google-apps.folder'`
- `'root' in parents`
- `trashed = false`
- `modifiedTime > '2026-01-01T00:00:00Z'`

Combined example:

```bash
python3 {baseDir}/scripts/gdrive_sa.py search "trashed = false and name contains 'roadmap'" --limit 20 --json
```

## Google Workspace Export MIME Types

Common export choices for Google-native files:

- Docs to plain text: `text/plain`
- Docs to PDF: `application/pdf`
- Docs to Word: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- Sheets to CSV: `text/csv`
- Sheets to XLSX: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Slides to PDF: `application/pdf`

Example:

```bash
python3 {baseDir}/scripts/gdrive_sa.py export <sheetId> --mime text/csv --out /tmp/sheet.csv
```

## Notes

- The script automatically enables `supportsAllDrives=true` and `includeItemsFromAllDrives=true`.
- OAuth-connected agents act as the connected end user, not as a service account.
- `root` refers to the visible root for the authenticated principal.
- Use `cat` only for text-friendly outputs. Use `download` or `export --out` for binary files.
- Confirm before uploading or creating folders in shared team drives.
