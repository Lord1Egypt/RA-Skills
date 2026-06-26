#!/usr/bin/env bash
set -euo pipefail

echo "Checking OmniFocus MCP skill prerequisites..."

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "FAIL: this skill requires macOS" >&2
  exit 1
fi

if ! command -v osascript >/dev/null 2>&1; then
  echo "FAIL: osascript is not available" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "FAIL: npm is not available" >&2
  exit 1
fi

if ! command -v openclaw >/dev/null 2>&1; then
  echo "WARN: openclaw is not available on PATH"
else
  echo "PASS: openclaw found"
fi

if command -v node >/dev/null 2>&1; then
  echo "PASS: node found"
else
  echo "WARN: node is not available on PATH"
fi

if command -v omnifocus-mcp >/dev/null 2>&1; then
  echo "PASS: omnifocus-mcp found"
else
  echo "WARN: omnifocus-mcp is not on PATH"
  echo "INFO: install it with npm install -g omnifocus-mcp"
fi

if [[ -d "/Applications/OmniFocus.app" || -d "$HOME/Applications/OmniFocus.app" ]]; then
  echo "PASS: OmniFocus.app found"
else
  echo "WARN: OmniFocus.app not found in /Applications or ~/Applications"
fi

echo "PASS: base prerequisites look reasonable"
