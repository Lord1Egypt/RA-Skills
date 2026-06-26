---
name: owncloudsync
description: Check that new files on Google Drive are present on OwnCloud + send email report
version: 1.0.0
author: SydneyPhoenix26
tags: [sync, google-drive, owncloud, backup, report]
license: MIT
metadata:
  { "openclaw": { 
      "requires": { 
        "bins": ["zsh", "curl", "jq", "gog"],
        "env" : [],
        "files" : ["owncloud.json"]
      }, 
      "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "steipete/tap/gogcli",
              "bins": ["gog"],
              "label": "Install gog (brew)",
            }
          ],
    }
  }
---
# owncloud-sync
## Purpose
This skill tracks files created or imported into Google Drive over a specified period (e.g., last 30 days), verifies their presence on the OwnCloud server, and generates a daily report emailed to the user. The report lists new Google Drive files and flags any missing or outdated files on OwnCloud, helping the user decide which files to copy.

## Rationale
Google Drive serves as a convenient workspace to drop and edit files. This skill helps decide whether to push files to OwnCloud or to delete/retain them on Google Drive.

## Operating Mode
- The script `owncloud-sync.sh` is located in `.openclaw/skills/owncloud-sync/`.
- Run the script manually or on demand; it requires Zsh.

## Configuration
- The script require a local config file owncloud.json.
- The variables `ALLFILES_URL`, `ALLFILES_USER`, and `ALLFILES_PASS` in `owncloud.json` specify the OwnCloud indexing service URL and credentials.
- `GOG_ACCOUNT` (Google Drive account) and `EMAIL_RECIPIENT` (report recipient) are also defined in `owncloud.json`.
- `PERIOD_DAYS` defines the date range for querying Google Drive, also in `owncloud.json`.

## Report
- All files created or imported during the specified period are checked on OwnCloud.
- The report indicates each file's status: OK, MISSING, or NEED UPDATE (if OwnCloud's version is older than Google Drive's).
