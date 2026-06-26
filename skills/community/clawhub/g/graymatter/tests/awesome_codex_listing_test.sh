#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_JSON="$ROOT_DIR/.codex-plugin/plugin.json"
LISTING_DOC="$ROOT_DIR/docs/awesome-codex-plugins.md"

[[ -f "$PLUGIN_JSON" ]]
[[ -f "$LISTING_DOC" ]]

name="$(jq -r '.name' "$PLUGIN_JSON")"
repo="$(jq -r '.repository' "$PLUGIN_JSON")"
description="$(jq -r '.description' "$PLUGIN_JSON")"

[[ "$name" == "graymatter" ]]
[[ "$repo" == "https://github.com/ValkyrLabs/GrayMatter" ]]

expected_line="- [GrayMatter](https://github.com/ValkyrLabs/GrayMatter) — $description"
grep -Fx -- "$expected_line" "$LISTING_DOC" >/dev/null

echo "awesome_codex_listing_test: ok"
