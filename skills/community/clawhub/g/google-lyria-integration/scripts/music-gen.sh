#!/bin/bash
# music-gen.sh - Wrapper to call music-gen.py
# Usage: ./music-gen.sh <prompt> [name] [sample_count]
#
# Reads config from workspace/lyria/config.json:
#   - project_id, location, bearer_token, output_dir
#
# Name is optional custom filename base (defaults to timestamp)
# Sample count generates multiple variations in one call

set -e

# Find workspace root (handles both direct run and skill usage)
if [ -n "$OPENCLAW_WORKSPACE" ]; then
    WORKSPACE_ROOT="$OPENCLAW_WORKSPACE"
else
    # Try to find .openclaw/workspace in home
    if [ -d "$HOME/.openclaw/workspace" ]; then
        WORKSPACE_ROOT="$HOME/.openclaw/workspace"
    else
        echo "Error: Cannot find OpenClaw workspace. Set OPENCLAW_WORKSPACE or ensure ~/.openclaw/workspace exists." >&2
        exit 1
    fi
fi

# Config file location
CONFIG_FILE="$WORKSPACE_ROOT/lyria/config.json"

# Arguments
PROMPT="$1"
NAME="$2"
SAMPLE_COUNT="${3:-1}"

# Validate required arguments
if [ -z "$PROMPT" ]; then
    echo "Usage: ./music-gen.sh <prompt> [name] [sample_count]" >&2
    echo "" >&2
    echo "Arguments:" >&2
    echo "  prompt       - Text description of desired music" >&2
    echo "  name         - Optional: custom filename base (no extension)" >&2
    echo "  sample_count - Optional: number of samples to generate (default: 1)" >&2
    echo "" >&2
    echo "Config file read from: $CONFIG_FILE" >&2
    echo "Ensure config.json has: project_id, location, bearer_token, output_dir" >&2
    echo "" >&2
    echo "Examples:" >&2
    echo "  ./music-gen.sh 'chill lo-fi piano' 'my_song'" >&2
    echo "  ./music-gen.sh 'k-pop dance track' 'kpop_track' 3" >&2
    exit 1
fi

# Validate config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE" >&2
    echo "" >&2
    echo "First time setup:" >&2
    echo "  1. Create directory: mkdir -p $WORKSPACE_ROOT/lyria/generated_music" >&2
    echo "  2. Create config file: $CONFIG_FILE" >&2
    echo "  3. Add your project_id, location, bearer_token, and output_dir" >&2
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run Python script
exec python3 "${SCRIPT_DIR}/music-gen.py" "$CONFIG_FILE" "$PROMPT" "$NAME" "$SAMPLE_COUNT"
