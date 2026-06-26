#!/usr/bin/env bash
# wiki-index.sh — Regenerate wiki/index.md from frontmatter
# Usage: bash wiki-index.sh <vault-path> [--help]
set -eo pipefail
export LC_ALL=C
. "$(dirname "$0")/lib.sh"

for arg in "$@"; do
  case "$arg" in --help|-h) echo "Usage: bash wiki-index.sh <vault-path>"; echo "Regenerate wiki/index.md from frontmatter of all wiki pages."; exit 0 ;; --*) echo "Error: unknown option '$arg'" >&2; exit 2 ;; esac
done

VAULT="${1:?Usage: wiki-index.sh <vault-path>}"
WIKI="$VAULT/wiki"
INDEX="$WIKI/index.md"

[ -d "$WIKI" ] || { echo "Error: $WIKI not found" >&2; exit 1; }

get_title() {
  local _t
  _t=$(get_field "$1" title)
  if [ -z "$_t" ]; then
    echo "Warning: no title in ${1#"$VAULT"/}" >&2
    basename "$1" .md | tr '-' ' '
  else
    printf '%s\n' "$_t"
  fi
}

get_summary() {
  local _s
  _s=$(awk '
    /^---\r?$/ && !d { f=!f; if(!f) d=1; next }
    f || /^#/ || /^$/ { next }
    /^%%/ { c=!c; next }
    c { next }
    { gsub(/%%([^%]|%[^%])*%%/, ""); gsub(/\r$/, ""); gsub(/\[\[[^|\]]*\\\|/, ""); gsub(/\[\[[^|\]]*\|/, ""); gsub(/\[\[/, ""); gsub(/\]\]/, ""); sub(/[[:space:]]+$/, ""); if(length>120) $0=substr($0,1,117)"..."; print; exit }
  ' "$1" 2>/dev/null) || true
  if [ -z "$_s" ]; then
    echo "Warning: no summary extracted from ${1#"$VAULT"/}" >&2
  fi
  printf '%s\n' "$_s"
}

build_section() {
  local _cat="$1" _hdr="$2"
  local _dir="$WIKI/$_cat"
  local _file="" _title="" _filename="" _summary="" _found=0
  [ -d "$_dir" ] || return 0
  echo "$_hdr"
  echo ""
  while IFS= read -r _file; do
    [ -n "$_file" ] || continue
    _found=1
    _title=$(get_title "$_file")
    _filename=$(basename "$_file" .md)
    _summary=$(get_summary "$_file")
    printf '%s\n' "- [[${_filename}|${_title}]] — ${_summary}"
  done < <(find "$_dir" -maxdepth 1 -type f -name '*.md' -print 2>/dev/null | sort)
  [ "$_found" -eq 1 ] || echo "_No pages yet._"
  echo ""
}

total=$(find "$WIKI" -type f -name '*.md' ! -path "$WIKI/index.md" ! -path "$WIKI/log.md" -print 2>/dev/null | wc -l | tr -d ' ')

_tmp_index=$(mktemp "$WIKI/index.md.XXXXXX")
trap 'rm -f "$_tmp_index" 2>/dev/null' EXIT
{
  echo "---"
  echo "title: Wiki Index"
  echo "type: index"
  echo "updated: $(date +%Y-%m-%d)"
  echo "---"
  echo ""
  echo "# Wiki Index"
  echo ""
  echo "*Auto-generated. Do not edit manually.*"
  echo ""
  build_section entities  "## 👤 Entities"
  build_section concepts  "## 💡 Concepts"
  build_section syntheses "## 📊 Syntheses"
  build_section sources   "## 📄 Sources"
  build_section reports   "## 📋 Reports"
  echo "---"
  echo ""
  echo "**Total pages:** ${total}"
  echo ""
  echo "Last compiled: $(date '+%Y-%m-%d %H:%M')"
} > "$_tmp_index"
mv "$_tmp_index" "$INDEX"

echo "Index written: $INDEX ($total pages)"
