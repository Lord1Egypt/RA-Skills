#!/bin/bash
# Market News Brief - Summarize broad market headlines from Yahoo Finance

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
uv run "$SCRIPT_DIR/src/main.py" "$@"
