#!/bin/zsh
# MemPalace MCP wrapper for OpenClaw

MEMPALACE_VENV="$HOME/mempalace/.venv"
MEMPALACE_BIN="$MEMPALACE_VENV/bin/mempalace"

# Activate venv and run mempalace with all args
source "$MEMPALACE_VENV/bin/activate"
exec "$MEMPALACE_BIN" "$@"
