# owncloud-sync

## Purpose
This skill tracks files created or imported into Google Drive over a specified period (e.g., last 30 days), verifies their presence on the OwnCloud server, and generates a daily report emailed to the user. The report lists new Google Drive files and flags any missing or outdated files on OwnCloud, helping the user decide which files to copy.

## Rationale
Google Drive serves as a convenient workspace to drop and edit files. This skill helps decide whether to push files to OwnCloud or to delete/retain them on Google Drive.

## Prerequisites on OwnCloud Server
- OwnCloud lacks a satisfactory built-in file search service, so an indexing service is required.
- A Go program (`allfiles-service.go`) is provided at https://github.com/MikoBoulot/openclaw-skills.
- Compile the Go program with:
  ```
  go build -ldflags=-s -w -o /usr/local/bin/allfiles-service allfiles-service.go
  ```
- Configure credentials (`BASIC_USER`, `BASIC_PASS`) in the service definition to match the `ALLFILES_USER` and `ALLFILES_PASS` in the skill.
- Install and enable the provided systemd service `allfiles.service`.
- Place valid certificates (default location: `/etc/allfiles/certs/`).

## Operating Mode
- The script `owncloud-sync.sh` is located in `.openclaw/workspace/skills/owncloud-sync/`.
- Run the script manually or on demand; it requires Zsh.

## Configuration
- The variables `ALLFILES_URL`, `ALLFILES_USER`, and `ALLFILES_PASS` in `owncloud.json` specify the OwnCloud indexing service credentials.
- `GOG_ACCOUNT` (Google Drive account) and `EMAIL_RECIPIENT` (report recipient) are set within the script.
- `PERIOD_DAYS` defines the date range for querying Google Drive, also set in the script.

## Report
- All files created or imported during the specified period are checked on OwnCloud.
- The report indicates each files status: OK, MISSING, or NEED UPDATE (if OwnClouds version is older than Google Drives).
