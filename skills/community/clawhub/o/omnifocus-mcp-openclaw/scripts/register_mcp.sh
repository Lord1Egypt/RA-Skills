#!/usr/bin/env bash
set -euo pipefail

if ! command -v openclaw >/dev/null 2>&1; then
  echo "openclaw is not installed or not on PATH" >&2
  exit 1
fi

if ! command -v omnifocus-mcp >/dev/null 2>&1; then
  echo "omnifocus-mcp is not installed or not on PATH" >&2
  echo "Install it with: npm install -g omnifocus-mcp" >&2
  exit 1
fi

openclaw mcp set omnifocus '{"command":"omnifocus-mcp","args":[]}'
echo "Registered OpenClaw MCP server: omnifocus"
echo "Inspect it with: openclaw mcp show omnifocus --json"
