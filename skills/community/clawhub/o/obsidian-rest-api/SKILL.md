---
name: obsidian-rest-api
description: "Operate Obsidian via Local REST API plugin from remote/WSL environments. Use when: (1) user asks to operate Obsidian, read/write notes, or manage vault remotely; (2) working with Obsidian vault files from WSL/remote where direct filesystem access is blocked; (3) creating, editing, or searching notes through API instead of file edits."
---

# Obsidian REST API

Operate Obsidian via Local REST API plugin from WSL or remote environments.

## First-Time Setup

**On first use, automatically detect and save configuration:**

1. Check TOOLS.md for existing `OBSIDIAN_API_URL` and `OBSIDIAN_API_KEY`
2. If not found:
   - Get Windows host IP: `cat /etc/resolv.conf | grep nameserver | awk '{print $2}'`
   - Ask user for API Key
   - Save to TOOLS.md:
     ```markdown
     ### Obsidian REST API (WSL → Windows)
     **API 端点**: https://<detected-ip>:27124
     **API Key**: <user-provided-key>
     ```
3. Test connection with saved config

## Configuration Format

Saved in TOOLS.md:
```markdown
### Obsidian REST API (WSL → Windows)
**API 端点**: https://<windows-host-ip>:27124
**API Key**: <your-api-key>
```

## Quick Start

```bash
# Get URL and KEY from TOOLS.md
URL=$(grep 'API 端点' ~/.openclaw/workspace/TOOLS.md | awk -F': ' '{print $2}')
KEY=$(grep 'API Key' ~/.openclaw/workspace/TOOLS.md | awk -F': ' '{print $2}')

# Test connection
curl -k -H "Authorization: Bearer $KEY" "$URL/"

# List vault files
curl -k -H "Authorization: Bearer $KEY" "$URL/vault/"

# Create note
curl -k -X PUT -H "Authorization: Bearer $KEY" -H "Content-Type: text/markdown" \
  -d "# Title\nContent" "$URL/vault/note.md"
```

## Common Tasks

### Create/Update Note
```bash
curl -k -X PUT -H "Authorization: Bearer $KEY" -H "Content-Type: text/markdown" \
  --data "<content>" "$URL/vault/<filename>.md"
```

### Append to Note
```bash
curl -k -X POST -H "Authorization: Bearer $KEY" -H "Content-Type: text/markdown" \
  --data "<content-to-append>" "$URL/vault/<filename>.md"
```

### Get Daily Note
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/periodic/daily/"
# Or specific date:
curl -k -H "Authorization: Bearer $KEY" "$URL/periodic/daily/2026/05/11/"
```

### Search Notes
```bash
# Simple text search
curl -k -X POST -H "Authorization: Bearer $KEY" \
  "$URL/search/simple/?query=keyword"

# Advanced search (Dataview-style)
curl -k -X POST -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"query":"tag:#work"}' "$URL/search/"
```

### Get Active File
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/active/"
```

### Open File in UI
```bash
curl -k -X POST -H "Authorization: Bearer $KEY" "$URL/open/note.md"
```

### Execute Command
```bash
# List available commands
curl -k -H "Authorization: Bearer $KEY" "$URL/commands/"

# Execute command
curl -k -X POST -H "Authorization: Bearer $KEY" "$URL/commands/daily-notes"
```

### Get All Tags
```bash
curl -k -H "Authorization: Bearer $KEY" "$URL/tags/"
```

## API Reference

See [references/api.md](references/api.md) for complete endpoint documentation.

## Troubleshooting

**Connection refused**: Windows firewall blocking port.
```powershell
# PowerShell (admin)
New-NetFirewallRule -DisplayName "Obsidian REST API" -Direction Inbound -LocalPort 27124 -Protocol TCP -Action Allow
```

**SSL error**: Use `-k` flag (self-signed cert).

**Vault not found**: Ensure vault is open in Obsidian.

## Windows Setup

1. Install `Local REST API` plugin in Obsidian
2. Enable "Bind to all interfaces" in plugin settings
3. Allow port in Windows firewall
4. Generate API key