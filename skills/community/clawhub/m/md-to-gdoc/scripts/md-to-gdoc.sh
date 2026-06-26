#!/usr/bin/env bash
# md-to-gdoc.sh — Convert a markdown file to a Google Doc with proper formatting.
#
# Usage:
#   md-to-gdoc.sh <markdown-file> [--title "Doc Title"] [--parent <folder-id>] [--account <email>]
#
# Defaults:
#   --title:   derived from filename (e.g. my-research.md → "my research")
#   --account: uses gog's default account (first authenticated)
#
# Outputs the Google Doc URL on success.

set -euo pipefail

# --- Parse args ---
MD_FILE=""
TITLE=""
PARENT=""
ACCOUNT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title)   TITLE="$2"; shift 2 ;;
    --parent)  PARENT="$2"; shift 2 ;;
    --account) ACCOUNT="$2"; shift 2 ;;
    -*)        echo "Unknown flag: $1" >&2; exit 1 ;;
    *)         MD_FILE="$1"; shift ;;
  esac
done

if [[ -z "$MD_FILE" ]]; then
  echo "Usage: md-to-gdoc.sh <markdown-file> [--title \"Doc Title\"] [--parent <folder-id>] [--account <email>]" >&2
  exit 1
fi

if [[ ! -f "$MD_FILE" ]]; then
  echo "Error: File not found: $MD_FILE" >&2
  exit 1
fi

# --- Validate markdown has proper headings ---
if ! grep -qE '^#{1,6} ' "$MD_FILE"; then
  echo "WARNING: No markdown headings (# Title) found in $MD_FILE" >&2
  echo "  The file should use # for H1, ## for H2, etc." >&2
  echo "  Without headings, everything will render as body text." >&2
  # Don't exit — still proceed, just warn
fi

# --- Derive title from filename if not provided ---
if [[ -z "$TITLE" ]]; then
  # Strip path + extension, replace hyphens/underscores with spaces
  basename_no_ext="$(basename "$MD_FILE" .md)"
  TITLE="$(echo "$basename_no_ext" | sed 's/[-_]/ /g')"
fi

# --- Step 1: Create empty Google Doc ---
CREATE_ARGS=(docs create "$TITLE" --json --force)
if [[ -n "$ACCOUNT" ]]; then
  CREATE_ARGS+=(--account "$ACCOUNT")
fi
if [[ -n "$PARENT" ]]; then
  CREATE_ARGS+=(--parent "$PARENT")
fi

echo "Creating Google Doc: \"$TITLE\"..." >&2
CREATE_OUTPUT=$(gog "${CREATE_ARGS[@]}" 2>&1)

DOC_ID=$(echo "$CREATE_OUTPUT" | python3 -c "import sys,json; print(json.load(sys.stdin)['file']['id'])" 2>/dev/null)
if [[ -z "$DOC_ID" ]]; then
  echo "Error: Failed to create Google Doc. Output:" >&2
  echo "$CREATE_OUTPUT" >&2
  exit 1
fi

DOC_URL=$(echo "$CREATE_OUTPUT" | python3 -c "import sys,json; print(json.load(sys.stdin)['file']['webViewLink'])" 2>/dev/null)
echo "Created doc: $DOC_ID" >&2

# --- Step 2: Populate with formatted markdown using `gog docs update` ---
# CRITICAL: Use `update --format=markdown`, NOT `write --markdown`.
# The `write --markdown` path has bugs with heading styles.
# The `update --format=markdown` path uses MarkdownToDocsRequests() which
# properly applies UpdateParagraphStyle with namedStyleType for headings.
echo "Writing formatted content..." >&2
UPDATE_ARGS=(docs update "$DOC_ID" --content-file "$MD_FILE" --format=markdown --force)
if [[ -n "$ACCOUNT" ]]; then
  UPDATE_ARGS+=(--account "$ACCOUNT")
fi
UPDATE_OUTPUT=$(gog "${UPDATE_ARGS[@]}" 2>&1)

UPDATE_EXIT=$?
if [[ $UPDATE_EXIT -ne 0 ]]; then
  echo "Error: Failed to write content. Output:" >&2
  echo "$UPDATE_OUTPUT" >&2
  echo "Doc was created but is empty: $DOC_URL" >&2
  exit 1
fi

echo "Done! $DOC_URL" >&2
echo "$DOC_URL"
