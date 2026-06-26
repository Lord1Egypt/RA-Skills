#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE_DIR="${OPENCLAW_DOCS_CACHE_DIR:-$SKILL_DIR/.cache}"
INDEX_URL="${OPENCLAW_DOCS_INDEX_URL:-https://docs.openclaw.ai/llms.txt}"
BASE_URL="${OPENCLAW_DOCS_BASE_URL:-https://docs.openclaw.ai}"
CACHE_TTL_SECONDS="${OPENCLAW_DOCS_CACHE_TTL_SECONDS:-3600}"

ensure_cache_dirs() {
  mkdir -p "$CACHE_DIR" "$CACHE_DIR/docs" "$CACHE_DIR/snapshots"
}

index_file() {
  printf '%s\n' "$CACHE_DIR/llms.txt"
}

file_age_seconds() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    printf '999999999\n'
    return
  fi
  local now mtime
  now=$(date +%s)
  mtime=$(stat -c %Y "$path")
  printf '%s\n' "$((now - mtime))"
}

refresh_index() {
  ensure_cache_dirs
  local dest tmp
  dest=$(index_file)
  tmp="${dest}.tmp"
  curl -fsSL "$INDEX_URL" -o "$tmp"
  mv "$tmp" "$dest"
  printf '%s\n' "$dest"
}

ensure_index() {
  ensure_cache_dirs
  local dest age
  dest=$(index_file)
  age=$(file_age_seconds "$dest")
  if [[ ! -s "$dest" || "$age" -gt "$CACHE_TTL_SECONDS" ]]; then
    refresh_index >/dev/null
  fi
  printf '%s\n' "$dest"
}

extract_doc_tsv() {
  local idx
  idx=$(ensure_index)
  perl -ne 'print "$1\t$2\n" if /^- \[(.*)\]\((https:\/\/docs\.openclaw\.ai\/[^)]+\.md)\)$/' "$idx"
}

extract_doc_urls() {
  extract_doc_tsv | cut -f2
}

normalize_doc_url() {
  local input="${1:-}"
  if [[ -z "$input" ]]; then
    echo "Usage: provide a docs path like gateway/configuration or a full docs.openclaw.ai URL" >&2
    return 1
  fi

  if [[ "$input" =~ ^https?:// ]]; then
    local base_no_query query
    base_no_query="${input%%\?*}"
    query=""
    if [[ "$input" == *\?* ]]; then
      query="?${input#*\?}"
    fi
    if [[ "$base_no_query" != *.md ]]; then
      base_no_query="${base_no_query%/}.md"
    fi
    printf '%s%s\n' "$base_no_query" "$query"
    return
  fi

  local path="$input"
  path="${path#/}"
  path="${path%.html}"
  if [[ "$path" != *.md ]]; then
    path="${path}.md"
  fi
  printf '%s/%s\n' "$BASE_URL" "$path"
}

doc_cache_path() {
  local url="$1"
  local without_query rel
  without_query="${url%%\?*}"
  rel="${without_query#${BASE_URL}/}"
  printf '%s\n' "$CACHE_DIR/docs/$rel"
}

download_doc() {
  local url="$1"
  local dest tmp force_fetch
  ensure_cache_dirs
  dest=$(doc_cache_path "$url")
  mkdir -p "$(dirname "$dest")"
  force_fetch="${OPENCLAW_DOCS_FORCE_FETCH:-0}"
  if [[ -s "$dest" && "$force_fetch" != "1" ]]; then
    printf '%s\n' "$dest"
    return
  fi
  tmp="${dest}.tmp"
  curl -fsSL "$url" -o "$tmp"
  mv "$tmp" "$dest"
  printf '%s\n' "$dest"
}

snapshot_path() {
  local stamp="${1:-}"
  printf '%s\n' "$CACHE_DIR/snapshots/${stamp}.tsv"
}

snapshot_now() {
  local stamp dest
  stamp=$(date -u +%Y%m%dT%H%M%SZ)
  dest=$(snapshot_path "$stamp")
  extract_doc_tsv | sort > "$dest"
  printf '%s\n' "$dest"
}

list_snapshots() {
  ensure_cache_dirs
  find "$CACHE_DIR/snapshots" -maxdepth 1 -type f -name '*.tsv' -printf '%f\n' | sort
}

resolve_snapshot() {
  local ref="${1:-}"
  ensure_cache_dirs
  if [[ -z "$ref" ]]; then
    return 1
  fi
  if [[ -f "$ref" ]]; then
    printf '%s\n' "$ref"
    return
  fi
  if [[ -f "$(snapshot_path "$ref")" ]]; then
    snapshot_path "$ref"
    return
  fi
  local match
  match=$(find "$CACHE_DIR/snapshots" -maxdepth 1 -type f -name "${ref}*.tsv" | sort | head -n1 || true)
  if [[ -n "$match" ]]; then
    printf '%s\n' "$match"
    return
  fi
  return 1
}

compare_snapshots() {
  local older="$1"
  local newer="$2"
  local a b added removed
  a=$(mktemp)
  b=$(mktemp)
  trap 'rm -f "$a" "$b" "$added" "$removed"' RETURN
  sort "$older" > "$a"
  sort "$newer" > "$b"
  added=$(mktemp)
  removed=$(mktemp)
  comm -13 "$a" "$b" > "$added"
  comm -23 "$a" "$b" > "$removed"

  echo "Comparing $(basename "$older") -> $(basename "$newer")"
  echo
  echo "Added pages: $(wc -l < "$added" | tr -d ' ')"
  if [[ -s "$added" ]]; then
    cut -f1,2 "$added"
  else
    echo "(none)"
  fi
  echo
  echo "Removed pages: $(wc -l < "$removed" | tr -d ' ')"
  if [[ -s "$removed" ]]; then
    cut -f1,2 "$removed"
  else
    echo "(none)"
  fi
}

fetch_all_docs() {
  ensure_cache_dirs
  local count=0 limit
  limit="${OPENCLAW_DOCS_FETCH_LIMIT:-0}"
  while IFS=$'\t' read -r _title url; do
    [[ -n "$url" ]] || continue
    if [[ "$limit" -gt 0 && "$count" -ge "$limit" ]]; then
      break
    fi
    download_doc "$url" >/dev/null
    count=$((count + 1))
  done < <(extract_doc_tsv)
  printf '%s\n' "$count"
}

search_cached_docs() {
  local query="$1"
  local docs_dir="$CACHE_DIR/docs"
  if [[ ! -d "$docs_dir" ]] || ! { find "$docs_dir" -type f -print -quit | grep -q .; }; then
    echo "No cached docs yet. Run: bash ./scripts/build-index.sh fetch" >&2
    return 1
  fi
  if command -v rg >/dev/null 2>&1; then
    rg -n -i --glob '*.md' "$query" "$docs_dir"
  else
    grep -Rni --include='*.md' "$query" "$docs_dir"
  fi
}
