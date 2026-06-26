#!/usr/bin/env bash
set -euo pipefail

INDEX_URL="${OPENCLAW_DOCS_INDEX_URL:-https://docs.openclaw.ai/llms.txt}"
CACHE_ROOT="${OPENCLAW_DOCS_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/openclaw-admin/openclaw-docs}"
VERSION="${OPENCLAW_VERSION:-}"

if [[ -z "$VERSION" ]] && command -v openclaw >/dev/null 2>&1; then
  VERSION="$(openclaw --version 2>/dev/null | awk '{print $NF}' | tr -cd '[:alnum:]._-')" || true
fi

if [[ -z "$VERSION" ]]; then
  VERSION="unknown-$(date -u +%Y%m%dT%H%M%SZ)"
fi

DEST="$CACHE_ROOT/$VERSION"
PAGES="$DEST/pages"

mkdir -p "$PAGES"

curl -fsSL "$INDEX_URL" -o "$DEST/llms.txt"

grep -Eo 'https://docs\.openclaw\.ai/[^)]+' "$DEST/llms.txt" \
  | sed 's/[[:space:]>),.]*$//' \
  | sort -u > "$DEST/urls.txt"

failures=0
while IFS= read -r url; do
  [[ -z "$url" ]] && continue
  rel="${url#https://docs.openclaw.ai/}"
  rel="${rel%%\?*}"
  # llms.txt promises ".md appended to any docs page URL" yields clean Markdown.
  # Without this, an extensionless URL like /automation lands as a file, then
  # /automation/cron-jobs fails to mkdir because `automation` is a file.
  case "$rel" in
    *.md|*.xml|*.txt|*.json|*.yaml|*.yml|*.html)
      fetch_url="$url"
      target="$PAGES/$rel"
      ;;
    *)
      fetch_url="${url}.md"
      target="$PAGES/${rel}.md"
      ;;
  esac
  mkdir -p "$(dirname "$target")"
  if ! curl -fsSL "$fetch_url" -o "$target"; then
    printf 'failed: %s\n' "$fetch_url" >&2
    failures=$((failures + 1))
  fi
done < "$DEST/urls.txt"

{
  printf 'version=%s\n' "$VERSION"
  printf 'index_url=%s\n' "$INDEX_URL"
  printf 'cache_path=%s\n' "$DEST"
  printf 'fetched_at_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'url_count=%s\n' "$(wc -l < "$DEST/urls.txt" | tr -d ' ')"
  printf 'failures=%s\n' "$failures"
} > "$DEST/manifest.env"

if [[ -e "$CACHE_ROOT/current" && ! -L "$CACHE_ROOT/current" ]]; then
  printf 'refusing to replace non-symlink path: %s\n' "$CACHE_ROOT/current" >&2
  printf 'move it aside or set OPENCLAW_DOCS_CACHE to another directory.\n' >&2
  exit 3
fi

ln -sfn "$DEST" "$CACHE_ROOT/current"

printf 'OpenClaw docs cache refreshed: %s\n' "$DEST"
printf 'Manifest: %s\n' "$DEST/manifest.env"

if [[ "$failures" -gt 0 ]]; then
  exit 2
fi
