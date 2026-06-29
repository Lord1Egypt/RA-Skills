#!/usr/bin/env bash
# Launch note-sync MCP server: $NOTE_SYNC_REPO/mcp-server/note-sync-mcp.exe
set -euo pipefail

if [[ -z "${NOTE_SYNC_REPO:-}" ]]; then
  echo "NOTE_SYNC_REPO is not set." >&2
  echo "Add to ~/.openclaw/openclaw.json:" >&2
  echo '  skills.entries.note-sync.env.NOTE_SYNC_REPO = "/mnt/e/github/go-note-sync-mcp"' >&2
  exit 1
fi

EXE="${NOTE_SYNC_REPO}/mcp-server/note-sync-mcp.exe"

if [[ ! -f "${EXE}" ]]; then
  echo "MCP binary not found: ${EXE}" >&2
  echo "Build on Windows:" >&2
  echo "  cd ${NOTE_SYNC_REPO}/mcp-server && go build -o note-sync-mcp.exe" >&2
  exit 1
fi

exec "${EXE}"
