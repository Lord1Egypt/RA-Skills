---
name: forensics-automation
description: Automated Linux forensic collection and archival. Generate comprehensive system forensic reports (users, network, logs, processes, packages, disk usage, etc.) and automatically upload to Google Drive or email results. Use when you need to: (1) Quickly collect forensic data from a Linux system, (2) Archive forensic reports to Google Drive, (3) Automate forensic collection + sharing in one command, or (4) Build forensic automation into security workflows.
---

# Forensics Automation Skill

Automated collection and archival of Linux system forensic data.

## Quick Start

### Prerequisites

Google Drive API setup required once:

```bash
# 1. Create GCP project and enable Google Drive API
# 2. Create OAuth 2.0 Desktop App credentials (JSON)
# 3. Run one-time setup
python3 setup_gmail.py

# Follow OAuth flow, authorize, paste code back
# Tokens saved to ~/.gmail_tokens.json
```

### Basic Usage

**Generate forensic report:**
```bash
bash linux_forensics.sh /tmp
# Creates: /tmp/forensics_YYYYMMDD_HHMMSS.txt
```

**Upload to Google Drive:**
```bash
python3 upload_to_drive.py /tmp/forensics_20260324_180000.txt
# Returns: File ID and shareable Drive link
```

**One-command: Generate + Upload:**
```bash
bash forensics_and_upload.sh
# Generates report and uploads in one go
```

**Send forensic data via email:**
```bash
python3 send_email.py recipient@example.com "Forensic Report" "Report attached"
```

## What Gets Collected

Each forensic report includes:

- **System Info**: Kernel version, hostname, OS details
- **Users & Groups**: All user accounts, sudoers configuration
- **Network**: IP addresses, routes, listening ports, connections
- **Packages**: Installed software (apt/rpm)
- **Processes**: Full process listing with arguments
- **System Logs**: dmesg, auth logs, system events
- **Cron Jobs**: Scheduled tasks across all users
- **File Integrity**: Recently modified files (last 7 days)
- **Disk Usage**: Storage breakdown

## Script Details

### `linux_forensics.sh`

Core forensic collection script.

```bash
bash linux_forensics.sh [output_directory]

# Example
bash linux_forensics.sh /tmp
# Creates /tmp/forensics_YYYYMMDD_HHMMSS.txt (~300KB typical)
```

**What it does:**
- Gathers comprehensive system information
- Runs read-only commands (safe to execute)
- Outputs to timestamped file for easy tracking
- Minimal dependencies (bash, standard Unix tools)

### `forensics_and_upload.sh`

Orchestration script: Generate report + Upload to Drive in one command.

```bash
bash forensics_and_upload.sh

# One-step forensic collection and archival
# Includes 2-second rate limit delay to avoid Google API throttling
```

**What it does:**
- Runs `linux_forensics.sh` automatically
- Gets most recent report
- Waits 2 seconds (rate limiting)
- Uploads to Google Drive
- Returns Drive link

### `upload_to_drive.py`

Upload any file to Google Drive using authenticated session.

```bash
python3 upload_to_drive.py <file_path> [folder_id]

# Examples
python3 upload_to_drive.py /tmp/report.txt
python3 upload_to_drive.py /tmp/report.txt "1a2b3c4d5e6f7890"  # Optional: upload to specific folder
```

**Returns:**
- File name on Drive
- File ID (for API access)
- Shareable link

### `send_email.py`

Send emails via Gmail API.

```bash
python3 send_email.py <recipient> <subject> <body>

# Example
python3 send_email.py analyst@company.com "Forensic Report Ready" "New forensics collected and uploaded to Drive"
```

## Integration Examples

### Security Operations Center (SOC)

Automate daily forensic snapshots:

```bash
#!/bin/bash
# Daily forensic collection cron job

cd /opt/forensics
bash forensics_and_upload.sh

# Email security team
python3 send_email.py security@company.com \
  "Daily Forensic Snapshot" \
  "Today's forensic report has been collected and uploaded to Google Drive"
```

### Incident Response

Rapid forensic collection during incident:

```bash
#!/bin/bash
# Incident response script

INCIDENT_ID="INC-2026-003"
bash linux_forensics.sh /tmp

# Upload and tag with incident ID
REPORT=$(ls -t /tmp/forensics_*.txt | head -1)
python3 upload_to_drive.py "$REPORT"

# Notify incident commander
python3 send_email.py "commander@company.com" \
  "Forensics Collected: $INCIDENT_ID" \
  "Forensic data from $REPORT ready for analysis"
```

### Compliance & Auditing

Monthly forensic audits:

```bash
#!/bin/bash
# Monthly audit job

MONTH=$(date +%Y-%m)
bash linux_forensics.sh "/var/forensics/$MONTH"

# Archive to Drive
REPORT=$(ls -t "/var/forensics/$MONTH"/forensics_*.txt | head -1)
python3 upload_to_drive.py "$REPORT" "AUDIT_FOLDER_ID"
```

## Setup & Requirements

### 1. Google Drive API Setup (One-time)

```bash
# Create GCP project and enable APIs:
# - Google Drive API
# - Gmail API (for email integration)

# Create OAuth 2.0 Desktop App credentials
# Download JSON credential file

# Place in script directory or set CREDS_FILE path
```

### 2. First-time Authorization

```bash
python3 setup_gmail.py

# Opens browser for OAuth authorization
# Paste authorization code when prompted
# Tokens saved to ~/.gmail_tokens.json
```

### 3. Verify Setup

```bash
# Test forensic collection
bash linux_forensics.sh /tmp

# Test Drive upload
python3 upload_to_drive.py /tmp/forensics_*.txt

# Test email
python3 send_email.py your-email@example.com "Test" "Forensics setup working!"
```

## Error Handling

### Common Issues

**"No tokens found"**
```
Run setup_gmail.py first to authorize
```

**"HTTP Error 400: Bad Request"**
```
Refresh token may be invalid (expires ~24hrs)
Run setup_gmail.py again to re-authorize
```

**"Permission denied" on /var/log**
```
Some logs require elevated privileges
Script gracefully skips unavailable files
```

**Rate limiting from Google APIs**
```
`forensics_and_upload.sh` includes 2-second delay
For batch operations, add `sleep 5` between uploads
```

## Performance Notes

- **Forensic collection**: ~1-5 seconds (depends on system load)
- **Report size**: ~250-400KB typical
- **Drive upload**: ~2-5 seconds (depends on network)
- **Email send**: ~1-2 seconds
- **Total one-command**: ~10-15 seconds

## Security Considerations

1. **OAuth tokens** stored in `~/.gmail_tokens.json` — keep secure (600 permissions)
2. **Refresh tokens** enable long-term automation without re-auth
3. **Scripts run read-only** — no system modification
4. **Drive links** are shareable — consider folder permissions

## Customization

### Extend forensic data collection

Edit `linux_forensics.sh` to add custom commands:

```bash
echo "=== CUSTOM DATA ===" | tee -a "$REPORT"
your-command-here >> "$REPORT"
```

### Change upload destination

Specify Google Drive folder:

```bash
python3 upload_to_drive.py report.txt "FOLDER_ID"
```

### Batch operations

Upload multiple reports:

```bash
for file in /tmp/forensics_*.txt; do
  python3 upload_to_drive.py "$file"
  sleep 5  # Rate limiting
done
```

## References

- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [Linux forensics best practices](https://www.man7.org/linux/man-pages/)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
