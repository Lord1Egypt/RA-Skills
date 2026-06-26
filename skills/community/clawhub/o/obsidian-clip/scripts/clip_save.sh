#!/usr/bin/env bash
set -euo pipefail

# Create (or append to) an Obsidian Clip note.
#
# Storage:
#   ${OBSIDIAN_VAULT:-$HOME/Documents/obsidian/obsidian-vault}/Clip/YYYY-MM/

OBSIDIAN_VAULT_DEFAULT="$HOME/Documents/obsidian/obsidian-vault"
VAULT="${OBSIDIAN_VAULT:-$OBSIDIAN_VAULT_DEFAULT}"

url=""
title=""
theme=""
date=""
keywords=""

bullets=()
actions=()
limits=()

tags=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --url) url="$2"; shift 2;;
    --title) title="$2"; shift 2;;
    --theme) theme="$2"; shift 2;;
    --date) date="$2"; shift 2;;
    --keywords) keywords="$2"; shift 2;;
    --bullets) bullets+=("$2"); shift 2;;
    --actions) actions+=("$2"); shift 2;;
    --limits) limits+=("$2"); shift 2;;
    --tags) tags+=("$2"); shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

if [[ -z "$url" ]]; then
  echo "--url is required" >&2
  exit 2
fi

if [[ -z "$date" ]]; then
  date=$(date +%F)
fi

month=${date:0:7}
clip_dir="$VAULT/Clip/$month"
mkdir -p "$clip_dir"

# Basic sanitization for filenames
safe_title="$title"
if [[ -z "$safe_title" ]]; then
  safe_title="Clip"
fi
safe_title=$(echo "$safe_title" | tr '/:\\' '____' | tr -s ' ' ' ')

# Keyword suffix for filename
kw_suffix=""
if [[ -n "$keywords" ]]; then
  kw_suffix="_${keywords}"
fi

file="$clip_dir/${date}_${safe_title}${kw_suffix}.md"

now_modified=$(date +%F)

# Tag helpers (macOS bash 3.2 compatible)
unique_tags=()
contains_tag() {
  local needle="$1"; shift || true
  for x in "$@"; do
    [[ "$x" == "$needle" ]] && return 0
  done
  return 1
}
for t in ${tags[@]+"${tags[@]}"}; do
  [[ -z "$t" ]] && continue
  if (( ${#unique_tags[@]} == 0 )); then
    unique_tags+=("$t")
  else
    if ! contains_tag "$t" "${unique_tags[@]}"; then
      unique_tags+=("$t")
    fi
  fi
done
if (( ${#unique_tags[@]} == 0 )); then
  unique_tags=("clip")
else
  if ! contains_tag "clip" "${unique_tags[@]}"; then
    unique_tags=("clip" "${unique_tags[@]}")
  fi
fi

# YAML tags + end tags
_tags_yaml=""
_end_tags=""
for t in "${unique_tags[@]}"; do
  _tags_yaml+=$'  - '"$t"$'\n'
  _end_tags+="#${t} "
done
_end_tags=$(echo "$_end_tags" | sed 's/[[:space:]]*$//')

# Language: auto-detect zh/en (override with OBSIDIAN_CLIP_LANG=zh|en)
clip_lang="${OBSIDIAN_CLIP_LANG:-auto}"
if [[ "$clip_lang" == "auto" ]]; then
  # Prefer locale hint
  if [[ "${LANG:-}" == zh* ]] || [[ "${LC_ALL:-}" == zh* ]]; then
    clip_lang="zh"
  else
    clip_lang="en"
  fi
  # If content contains CJK, switch to zh
  content_probe="$title $theme"
  for x in ${bullets[@]+"${bullets[@]}"}; do content_probe+=" $x"; done
  for x in ${actions[@]+"${actions[@]}"}; do content_probe+=" $x"; done
  for x in ${limits[@]+"${limits[@]}"}; do content_probe+=" $x"; done
  if [[ "$content_probe" =~ [一-龥] ]]; then
    clip_lang="zh"
  fi
fi

if [[ "$clip_lang" == "zh" ]]; then
  L_LINK="链接"
  L_THEME="主题一句话"
  H_TAKEAWAYS="要点"
  H_ACTIONS="我怎么用"
  H_LIMITS="规则/限制"
else
  L_LINK="Link"
  L_THEME="Theme"
  H_TAKEAWAYS="Takeaways"
  H_ACTIONS="How I'll use it"
  H_LIMITS="Limits"
fi

if [[ "$clip_lang" == "zh" ]]; then
  H_CLIP_AT="剪藏"
  L_CREATED_LINE_PREFIX="> 创建时间："
else
  H_CLIP_AT="Clip"
  L_CREATED_LINE_PREFIX="> Created: "
fi

# Section body
section=$'## '"$H_CLIP_AT"$' '"$date"$'\n\n'
section+="- ${L_LINK}：${url}"$'\n'
if [[ -n "$theme" ]]; then
  section+="- ${L_THEME}：${theme}"$'\n'
fi

if [[ ${#bullets[@]} -gt 0 ]]; then
  section+=$'\n### '"$H_TAKEAWAYS"$'\n'
  for b in "${bullets[@]}"; do
    section+="- ${b}"$'\n'
  done
fi

if [[ ${#actions[@]} -gt 0 ]]; then
  section+=$'\n### '"$H_ACTIONS"$'\n'
  for a in "${actions[@]}"; do
    section+="- ${a}"$'\n'
  done
fi

if [[ ${#limits[@]} -gt 0 ]]; then
  section+=$'\n### '"$H_LIMITS"$'\n'
  for l in "${limits[@]}"; do
    section+="- ${l}"$'\n'
  done
fi

section+=$'\n'

if [[ -f "$file" ]]; then
  tmp=$(mktemp)
  awk -v m="$now_modified" '
    BEGIN{in_fm=0}
    NR==1 && $0=="---" {in_fm=1; print; next}
    in_fm==1 && $0 ~ /^modified:/ {print "modified: " m; next}
    in_fm==1 && $0=="---" {in_fm=0; print; next}
    {print}
  ' "$file" > "$tmp"
  mv "$tmp" "$file"
  printf "%b" "$section" >> "$file"
else
  {
    printf '%s\n' '---'
    printf "created: %s\n" "$date"
    printf "modified: %s\n" "$now_modified"
    printf "tags:\n%b" "$_tags_yaml"
    printf "category: clip\n"
    printf '%s\n\n' '---'

    printf "# %s%s\n\n" "$safe_title" "$kw_suffix"
    printf "%s%s\n\n" "$L_CREATED_LINE_PREFIX" "$date"
    printf "%b" "$section"
    printf "%s\n" "$_end_tags"
  } > "$file"
fi

echo "$file"
