---
name: integration-google-drive
description: Google Drive + Sheets nodes. OAuth scopes, folder-vs-file IDs.
user-invocable: false
---

# Google Drive (and Sheets)

## Node types

- `n8n-nodes-base.googleDrive` — file ops on Drive.
- `n8n-nodes-base.googleSheets` — Sheets read/write.

## Credential type

`googleApi` (single credential covers Drive + Sheets if scopes include both).

For setup, see [`skills/manage-credentials.md`](../../manage-credentials.md). OAuth scopes minimum:

- Drive: `https://www.googleapis.com/auth/drive`
- Sheets: `https://www.googleapis.com/auth/spreadsheets`

## File / folder IDs

A Drive URL `https://drive.google.com/drive/folders/<ID>` gives the folder ID. A Sheets URL `https://docs.google.com/spreadsheets/d/<ID>/edit` gives the spreadsheet ID.

Store IDs in env YAML:

```yaml
gdrive:
  reportsFolder: "1abc..."
  weeklyReport: "1xyz..."  # spreadsheet
```

## App verification

Using sensitive scopes (full Drive access, etc.) requires Google's app verification for production-tier apps. For internal-team-only projects, configure the OAuth client as "internal" within a Workspace org to bypass verification.
