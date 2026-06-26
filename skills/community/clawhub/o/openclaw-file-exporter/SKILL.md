---
name: openclaw-file-exporter
description: Export OpenClaw configuration files, skills, or other files and upload them to tmpfile.link for easy download. Use when the user wants to export/backup/download OpenClaw files including skills, configs, or any other files. Compresses files automatically and provides formatted download links with file details.
---

# OpenClaw File Exporter

Export OpenClaw files and upload to tmpfile.link temporary file hosting service.

## When to Use

Use this skill when the user wants to:
- Export/backup an OpenClaw skill
- Download configuration files
- Share OpenClaw files externally
- Create backups of any OpenClaw-related files

## Features

- Automatic compression (tar.gz)
- Uploads to tmpfile.link (7-day retention)
- Supports both anonymous and authenticated uploads
- Formatted output with download links

## Usage

### Basic Export

Export a skill or file:

```bash
~/.openclaw/skills/openclaw-file-exporter/scripts/export-and-upload.sh <source_path> [custom_name]
```

Examples:
```bash
# Export a skill
~/.openclaw/skills/openclaw-file-exporter/scripts/export-and-upload.sh ~/.openclaw/skills/skill-security-auditor

# Export with custom name
~/.openclaw/skills/openclaw-file-exporter/scripts/export-and-upload.sh ~/.openclaw/skills/skill-security-auditor my-backup.tar.gz

# Export a config file
~/.openclaw/skills/openclaw-file-exporter/scripts/export-and-upload.sh ~/.openclaw/config.yaml
```

### Authentication (Optional)

For authenticated uploads (longer retention), set environment variables:

```bash
export tfLink-X-User-Id="your-user-id"
export tfLink-X-Auth-Token="your-auth-token"
```

If not set, the script uses anonymous upload.

## Output Format

The script outputs formatted file information:

```
========================================
Upload successful!
========================================
File Name: skill-security-auditor.tar.gz
Size: 7890 bytes
Type: application/gzip
Uploaded To: public

Download Link:
https://d.tmpfile.link/public/2026-03-12/uuid/skill-security-auditor.tar.gz

Download Link (Encoded):
https://d.tmpfile.link/public/2026-03-12/uuid/skill-security-auditor.tar.gz
========================================

Note: File will be automatically deleted after 7 days
```

## Limitations

- Maximum file size: 100MB
- Files auto-delete after 7 days (anonymous) or longer (authenticated)
- Requires `curl` and `jq` to be installed
