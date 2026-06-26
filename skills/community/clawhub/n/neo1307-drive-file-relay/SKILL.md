---
name: drive-file-relay
description: Copy (relay) a local file from this machine into Google Drive for desktop (GoogleDriveFS) so it can be downloaded from a phone when the phone is not on the same LAN. Use when the user says they are on the phone, cannot access the PC, and needs an APK/ZIP/PDF/any file moved into Drive; also use when you must verify size+SHA256 after copy.
---

# Drive File Relay (Google Drive for desktop)

## Workflow

1) **Preflight**
- Confirm source path exists.
- Detect Drive mount:
  - Prefer `G:\Drive'ım\` (TR) and `G:\My Drive\` (EN).
  - If not found, list filesystem drives and look for a drive containing `.shortcut-targets-by-id`.

2) **Copy + verify** (no partial success)
- Create destination folder if missing.
- Copy file.
- Compute SHA256 of source and destination and ensure they match.
- Report:
  - src path
  - dst path
  - size bytes + MB
  - sha256

3) **User instruction**
- Tell the user where to find it on the phone: Google Drive → My Drive/Drive'ım → `<folder>`.

## Script
Run (PowerShell):
- `powershell -ExecutionPolicy Bypass -File scripts/drive_relay.ps1 -Src "<path>" -DstFolder "ArgusShare" -DstName "<optional>"`

### Notes
- Do **not** attempt provider messaging via curl/Telegram Bot API.
- This skill does **not** create share links; it only ensures the file is present in the user’s Drive.
