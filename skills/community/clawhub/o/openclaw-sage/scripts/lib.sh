#!/bin/bash
# Shared utilities for openclaw-sage scripts

DOC_TTL="${OPENCLAW_SAGE_DOC_TTL:-86400}"           # 24hr default
LANGS="${OPENCLAW_SAGE_LANGS:-en}"                  # comma-separated lang codes, or "all"
FETCH_JOBS="${OPENCLAW_SAGE_FETCH_JOBS:-8}"         # parallel fetch workers for build-index.sh fetch
_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${OPENCLAW_SAGE_CACHE_DIR:-${_LIB_DIR}/../.cache/openclaw-sage}"
DOCS_BASE_URL="${OPENCLAW_SAGE_DOCS_BASE_URL:-https://docs.openclaw.ai}"
SOURCE="${OPENCLAW_SAGE_SOURCE:-github}"   # "github" or "local:/path/to/docs"
GITHUB_REPO="openclaw/openclaw"
GITHUB_RAW="https://raw.githubusercontent.com/${GITHUB_REPO}"

mkdir -p "$CACHE_DIR"

# check_online — returns 0 if source is reachable, 1 if not
check_online() {
  if [[ "$SOURCE" == local:* ]]; then
    local local_path="${SOURCE#local:}"
    [ -d "$local_path" ]
  else
    curl -sf --max-time 2 -o /dev/null -I "https://raw.githubusercontent.com" 2>/dev/null
  fi
}

# parse_version_flag [args...] — extracts --version <tag> from args,
# sets VERSION and VERSION_CACHE_DIR, returns remaining args in REMAINING_ARGS
parse_version_flag() {
  VERSION="latest"
  REMAINING_ARGS=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --version)
        shift
        VERSION="${1:?--version requires a tag argument}"
        shift   # consume the tag value; outer shift would advance past next real arg
        continue
        ;;
      *)
        REMAINING_ARGS+=("$1")
        ;;
    esac
    shift
  done
  # local mode always uses "local" as the version label
  if [[ "$SOURCE" == local:* ]]; then
    VERSION="local"
  fi
  VERSION_CACHE_DIR="${CACHE_DIR}/${VERSION}"
  mkdir -p "$VERSION_CACHE_DIR"
}

# resolve_source <doc_path> <ref> — returns URL or filesystem path for a doc
resolve_source() {
  local doc_path="$1" ref="${2:-main}"
  if [[ "$SOURCE" == local:* ]]; then
    local local_path="${SOURCE#local:}"
    echo "${local_path}/${doc_path}.md"
  else
    echo "${GITHUB_RAW}/${ref}/docs/${doc_path}.md"
  fi
}

# resolve_source_raw <relative_path> <ref> — like resolve_source but without .md suffix
# <relative_path> is relative to the docs/ directory (e.g. "docs.json")
resolve_source_raw() {
  local rel_path="$1" ref="${2:-main}"
  if [[ "$SOURCE" == local:* ]]; then
    echo "${SOURCE#local:}/${rel_path}"
  else
    echo "${GITHUB_RAW}/${ref}/docs/${rel_path}"
  fi
}

# clean_markdown <input.md> <output.txt> — strip frontmatter/MDX, write plain text
clean_markdown() {
  local input="$1" output="$2"
  python3 - "$input" "$output" <<'PYEOF'
import sys, re

input_path, output_path = sys.argv[1], sys.argv[2]
with open(input_path, encoding='utf-8', errors='replace') as f:
    text = f.read()

# Extract frontmatter title/summary before stripping
title, summary = '', ''
fm_match = re.match(r'^---\s*\n(.*?)\n---\s*(?:\n|$)', text, re.S)
if fm_match:
    fm = fm_match.group(1)
    m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm, re.M)
    if m: title = m.group(1).strip()
    m = re.search(r'^summary:\s*["\']?(.*?)["\']?\s*$', fm, re.M)
    if m: summary = m.group(1).strip()
    text = text[fm_match.end():]

# Protect fenced code blocks from tag stripping
fences = {}
def protect(m):
    key = f'\x00FENCE{len(fences)}\x00'
    fences[key] = m.group(0)
    return key
text = re.sub(r'```.*?```', protect, text, flags=re.S)
text = re.sub(r'`[^`]+`', protect, text)

# Strip self-closing MDX tags: <Tag ... />
text = re.sub(r'<[A-Z][A-Za-z]*[^>]*/>', '', text)
# Strip paired MDX tags, keep inner text: <Tag ...>content</Tag>
# Loop until stable to handle nested tags (e.g. <CardGroup><Card>text</Card></CardGroup>)
prev = None
while prev != text:
    prev = text
    text = re.sub(r'<([A-Z][A-Za-z]*)[^>]*>(.*?)</\1>', r'\2', text, flags=re.S)

# Restore fenced code blocks
for key, val in fences.items():
    text = text.replace(key, val)

header = '\n'.join(filter(None, [title, summary]))
if header:
    text = header + '\n\n' + text

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text.strip() + '\n')
PYEOF
}

# fetch_markdown <safe_path> <ref> — fetch .md from source, clean to .txt
# Writes: $VERSION_CACHE_DIR/doc_<safe_path>.md
#         $VERSION_CACHE_DIR/doc_<safe_path>.txt
# Returns 0 on success, 1 on failure.
fetch_markdown() {
  local safe="$1" ref="${2:-main}"
  : "${VERSION_CACHE_DIR:?fetch_markdown requires VERSION_CACHE_DIR — call parse_version_flag first}"
  local doc_path
  doc_path="$(echo "$safe" | tr '_' '/')"
  local source_url
  source_url="$(resolve_source "$doc_path" "$ref")"
  local md_file="${VERSION_CACHE_DIR}/doc_${safe}.md"
  local txt_file="${VERSION_CACHE_DIR}/doc_${safe}.txt"
  local tmp_md
  tmp_md=$(mktemp)
  trap 'rm -f "$tmp_md"' EXIT

  if [[ "$SOURCE" == local:* ]]; then
    if [ ! -f "$source_url" ]; then
      return 1
    fi
    cp "$source_url" "$tmp_md"
  else
    if ! curl -sf --max-time 15 "$source_url" -o "$tmp_md" 2>/dev/null || [ ! -s "$tmp_md" ]; then
      return 1
    fi
  fi

  mv "$tmp_md" "$md_file"
  clean_markdown "$md_file" "$txt_file"

  if [ ! -s "$txt_file" ]; then
    rm -f "$txt_file"
    return 1
  fi
}

# get_mtime <file> — print file mtime as epoch seconds
get_mtime() {
  local file="$1"
  [ -f "$file" ] || return 1
  if [[ "$OSTYPE" == "darwin"* ]]; then
    stat -f %m "$file"
  else
    stat -c %Y "$file"
  fi
}

# is_cache_fresh <file> <ttl_seconds>
is_cache_fresh() {
  local file="$1" ttl="$2"
  [ -f "$file" ] || return 1
  local now mtime
  now=$(date +%s)
  mtime=$(get_mtime "$file") || return 1
  [ $((now - mtime)) -lt "$ttl" ]
}
