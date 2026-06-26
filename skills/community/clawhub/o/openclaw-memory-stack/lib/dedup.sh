#!/usr/bin/env bash
# OpenClaw Memory Stack — Memory Deduplication
# Prevents duplicate memories from accumulating.
# Sourced by wrappers (especially Total Recall); not run standalone.

DEDUP_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$DEDUP_LIB_DIR/platform.sh"

# Config defaults
DEDUP_ENABLED="${DEDUP_ENABLED:-true}"
DEDUP_THRESHOLD="${DEDUP_THRESHOLD:-0.9}"
DEDUP_MERGE_MODEL="${DEDUP_MERGE_MODEL:-qwen2.5:7b}"
DEDUP_MERGE_ENDPOINT="${DEDUP_MERGE_ENDPOINT:-http://localhost:11434}"

# Load config from JSON file if available
# Usage: dedup_load_config <config_json_path>
dedup_load_config() {
  local config_file="$1"
  [ ! -f "$config_file" ] && return 0

  if has_command python3; then
    local _val
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('dedup',{}); v=cfg.get('enabled',''); print(str(v).lower()) if v!='' else exit(1)" 2>/dev/null) && DEDUP_ENABLED="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('dedup',{}); v=cfg.get('threshold',''); print(v) if v else exit(1)" 2>/dev/null) && DEDUP_THRESHOLD="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('dedup',{}); v=cfg.get('merge_model',''); print(v) if v else exit(1)" 2>/dev/null) && DEDUP_MERGE_MODEL="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('dedup',{}); v=cfg.get('merge_endpoint',''); print(v) if v else exit(1)" 2>/dev/null) && DEDUP_MERGE_ENDPOINT="$_val"
  fi
}

# Check if dedup is enabled
dedup_is_enabled() {
  [ "$DEDUP_ENABLED" = "true" ] || [ "$DEDUP_ENABLED" = "1" ]
}

# ── Duplicate detection ──────────────────────────────────────
# Usage: check_duplicate <new_content> [collection]
# Output: "duplicate:<key>" | "merge:<key>" | "unique"
#   - duplicate: content is near-identical (score > threshold), skip
#   - merge: content is related but different (score > threshold * 0.8), merge
#   - unique: no significant match, proceed with store

check_duplicate() {
  local new_content="$1"
  local collection="${2:-}"

  if ! dedup_is_enabled; then
    echo "unique"
    return 0
  fi

  # Need qmd for vector similarity check
  if ! has_command qmd; then
    # No qmd — fall back to exact string matching
    _check_duplicate_grep "$new_content"
    return 0
  fi

  # Use qmd vsearch to find similar content
  local collection_flag=""
  [ -n "$collection" ] && collection_flag="-c $collection"

  # Truncate content for search query (qmd has query length limits)
  local search_query
  search_query=$(echo "$new_content" | head -c 500)

  local raw_output
  raw_output=$(qmd vsearch "$search_query" $collection_flag --json 2>/dev/null) || true

  if [ -z "$raw_output" ] || [ "$raw_output" = "null" ] || [ "$raw_output" = "[]" ]; then
    echo "unique"
    return 0
  fi

  # Check top result score
  python3 -c "
import json

data = json.loads('''$raw_output''')
if isinstance(data, list):
    items = data
elif isinstance(data, dict) and 'results' in data:
    items = data['results']
else:
    items = [data]

if not items:
    print('unique')
    exit(0)

top = items[0]
score = float(top.get('score', top.get('relevance', 0)))
path = top.get('path', top.get('source', ''))

threshold = float('$DEDUP_THRESHOLD')
merge_threshold = threshold * 0.8

if score >= threshold:
    print(f'duplicate:{path}')
elif score >= merge_threshold:
    print(f'merge:{path}')
else:
    print('unique')
" 2>/dev/null || echo "unique"
}

# Grep-based duplicate check fallback
_check_duplicate_grep() {
  local new_content="$1"
  local memory_root="${OPENCLAW_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || echo "")}"

  if [ -z "$memory_root" ] || [ ! -d "$memory_root/memory" ]; then
    echo "unique"
    return 0
  fi

  # Extract first significant line for matching
  local first_line
  first_line=$(echo "$new_content" | grep -v '^#' | grep -v '^$' | head -1 | head -c 100)

  if [ -z "$first_line" ]; then
    echo "unique"
    return 0
  fi

  local matches
  matches=$(grep -rl "$first_line" "$memory_root/memory/" 2>/dev/null | head -1 || true)

  if [ -n "$matches" ]; then
    echo "duplicate:$matches"
  else
    echo "unique"
  fi
}

# ── Memory merging ───────────────────────────────────────────
# Usage: merge_memories <existing_file_path> <new_content>
# Output: merged content on stdout

merge_memories() {
  local existing_path="$1"
  local new_content="$2"

  if [ ! -f "$existing_path" ]; then
    # Nothing to merge with — return new content
    echo "$new_content"
    return 0
  fi

  local existing_content
  existing_content=$(cat "$existing_path" 2>/dev/null)

  # Check Ollama for LLM merge
  if curl -sf "${DEDUP_MERGE_ENDPOINT}/api/tags" >/dev/null 2>&1; then
    _merge_llm "$existing_content" "$new_content"
    return $?
  fi

  # Fallback: simple append-based merge
  _merge_heuristic "$existing_content" "$new_content"
}

# LLM-powered merge
_merge_llm() {
  local existing="$1" new="$2"

  local prompt="Merge these two related memory entries into one concise, deduplicated entry. Keep all unique information. Remove redundancy. Output only the merged text, no commentary.\n\nExisting memory:\n${existing}\n\nNew memory:\n${new}"

  local payload
  payload=$(python3 -c "
import json
print(json.dumps({
    'model': '$DEDUP_MERGE_MODEL',
    'prompt': '''$prompt''',
    'stream': False,
    'options': {'num_predict': 1000, 'temperature': 0.2}
}))
" 2>/dev/null) || {
    _merge_heuristic "$existing" "$new"
    return 0
  }

  local response
  response=$(curl -sf --max-time 30 \
    -X POST "${DEDUP_MERGE_ENDPOINT}/api/generate" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || {
    _merge_heuristic "$existing" "$new"
    return 0
  }

  local merged
  merged=$(python3 -c "
import json
data = json.loads('''$response''')
text = data.get('response', '').strip()
print(text if text else '')
" 2>/dev/null) || true

  if [ -n "$merged" ]; then
    echo "$merged"
  else
    _merge_heuristic "$existing" "$new"
  fi
}

# Heuristic merge: append non-duplicate lines
_merge_heuristic() {
  local existing="$1" new="$2"

  python3 -c "
existing_lines = set('''$existing'''.strip().split('\n'))
new_lines = '''$new'''.strip().split('\n')

# Start with existing content
result = '''$existing'''.strip()

# Append truly new lines
additions = []
for line in new_lines:
    stripped = line.strip()
    if stripped and stripped not in existing_lines and len(stripped) > 5:
        additions.append(line)

if additions:
    result += '\n\n--- Updated: $(now_iso) ---\n'
    result += '\n'.join(additions)

print(result)
" 2>/dev/null || {
    # Last resort: just concatenate
    printf '%s\n\n--- Updated: %s ---\n%s' "$existing" "$(now_iso)" "$new"
  }
}

# ── Pre-store hook ───────────────────────────────────────────
# Usage: dedup_pre_store <new_content> <tier> <slug> [collection]
# Returns 0 and prints action to take: "store", "skip", "merge:<path>"
# Callers should check the output and act accordingly.

dedup_pre_store() {
  local new_content="$1"
  local tier="$2"
  local slug="$3"
  local collection="${4:-}"

  if ! dedup_is_enabled; then
    echo "store"
    return 0
  fi

  local result
  result=$(check_duplicate "$new_content" "$collection")

  case "$result" in
    duplicate:*)
      local existing_path="${result#duplicate:}"
      echo "dedup: skipping duplicate (matches $existing_path)" >&2
      echo "skip"
      ;;
    merge:*)
      local existing_path="${result#merge:}"
      echo "dedup: merging with existing ($existing_path)" >&2
      echo "merge:$existing_path"
      ;;
    unique|*)
      echo "store"
      ;;
  esac
}
