#!/usr/bin/env bash
# OpenClaw Memory Stack — L0/L1/L2 Tiered Context Loading
# OpenViking-style progressive loading: abstract → overview → full content.
# Sourced by wrappers and router; not run standalone.

TIERED_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$TIERED_LIB_DIR/platform.sh"

# Tier token budgets — must stay aligned with landing claim "3 tiers: ~100 / ~800 / full"
TIER_L0_TOKENS="${TIER_L0_TOKENS:-100}"
TIER_L1_TOKENS="${TIER_L1_TOKENS:-800}"

# Thresholds for auto-expansion
TIER_AUTO_EXPAND_THRESHOLD="${TIER_AUTO_EXPAND_THRESHOLD:-0.6}"

# Tier summarization is performed by the OpenClaw agent (which IS an LLM) and
# stored via `openclaw-memory tier set` — no separate Ollama/MLX install required.
# `generate_tiers` (heuristic) remains as an offline fallback.

# ── L0: Abstract (~100 tokens) ──────────────────────────────
# One-sentence summary for relevance checking.
# Heuristic: first non-empty, non-heading, non-frontmatter line.

_extract_l0_heuristic() {
  local file_path="$1"
  python3 -c "
import sys
from pathlib import Path

content = Path('$file_path').read_text(errors='replace')
lines = content.split('\n')

in_frontmatter = False
for line in lines:
    stripped = line.strip()
    if stripped == '---':
        in_frontmatter = not in_frontmatter
        continue
    if in_frontmatter:
        continue
    if not stripped:
        continue
    # Skip markdown headings
    if stripped.startswith('#'):
        # Use heading text as L0 if it's descriptive
        text = stripped.lstrip('#').strip()
        if len(text) > 10:
            print(text[:400])
            sys.exit(0)
        continue
    # Skip code fences
    if stripped.startswith('\`\`\`'):
        continue
    # First meaningful line
    print(stripped[:400])
    sys.exit(0)

# Fallback: filename
print(Path('$file_path').stem.replace('-', ' ').replace('_', ' '))
" 2>/dev/null
}

# ── L1: Overview (~800 tokens) ───────────────────────────────
# Core info + usage scenarios.
# Heuristic: first ~TIER_L1_TOKENS tokens (approx chars / 0.75).

_extract_l1_heuristic() {
  local file_path="$1"
  local char_limit=$(( TIER_L1_TOKENS * 4 ))  # ~4 chars per token

  python3 -c "
from pathlib import Path

content = Path('$file_path').read_text(errors='replace')
limit = $char_limit

# Strip frontmatter
lines = content.split('\n')
result = []
in_fm = False
for line in lines:
    if line.strip() == '---':
        in_fm = not in_fm
        continue
    if not in_fm:
        result.append(line)

text = '\n'.join(result)[:limit]

# Try to end at a sentence or paragraph boundary
last_para = text.rfind('\n\n')
if last_para > limit * 0.7:
    text = text[:last_para]
else:
    last_period = text.rfind('.')
    if last_period > limit * 0.7:
        text = text[:last_period + 1]

print(text)
" 2>/dev/null
}

# ── Generate tier files for a directory ──────────────────────
# Creates .abstract and .overview sidecar files.
# Usage: generate_tiers <file_path>

generate_tiers() {
  local file_path="$1"

  if [ ! -f "$file_path" ]; then
    echo "Error: file not found: $file_path" >&2
    return 1
  fi

  local dir
  dir="$(dirname "$file_path")"
  local basename
  basename="$(basename "$file_path")"

  # L0: Write abstract
  local l0_content
  l0_content=$(_extract_l0_heuristic "$file_path")
  if [ -n "$l0_content" ]; then
    local abstract_file="$dir/.abstract"
    # Append or update entry for this file
    _update_tier_file "$abstract_file" "$basename" "$l0_content"
  fi

  # L1: Write overview
  local l1_content
  l1_content=$(_extract_l1_heuristic "$file_path")
  if [ -n "$l1_content" ]; then
    local overview_file="$dir/.overview"
    _update_tier_file "$overview_file" "$basename" "$l1_content"
  fi

  # L2: Original file — no action needed
}

# ── Update a tier sidecar file ───────────────────────────────
# Format: each entry is "## <filename>\n<content>\n"
_update_tier_file() {
  local tier_file="$1" filename="$2" content="$3"

  python3 -c "
import sys
from pathlib import Path

tier_file = '$tier_file'
filename = '$filename'
content = '''$content'''

path = Path(tier_file)
existing = path.read_text(errors='replace') if path.exists() else ''

# Parse existing entries
entries = {}
current_key = None
current_lines = []
for line in existing.split('\n'):
    if line.startswith('## '):
        if current_key:
            entries[current_key] = '\n'.join(current_lines).strip()
        current_key = line[3:].strip()
        current_lines = []
    else:
        current_lines.append(line)
if current_key:
    entries[current_key] = '\n'.join(current_lines).strip()

# Update entry
entries[filename] = content.strip()

# Write back
lines = []
for key in sorted(entries.keys()):
    lines.append(f'## {key}')
    lines.append(entries[key])
    lines.append('')

path.write_text('\n'.join(lines))
" 2>/dev/null
}

# ── Generate tiers for all files in a directory ──────────────
# Usage: generate_tiers_dir <directory> [glob_pattern]
generate_tiers_dir() {
  local directory="$1"
  local pattern="${2:-*.md}"

  if [ ! -d "$directory" ]; then
    echo "Error: directory not found: $directory" >&2
    return 1
  fi

  local count=0
  while IFS= read -r -d '' file; do
    generate_tiers "$file"
    count=$((count + 1))
  done < <(find "$directory" -name "$pattern" -type f -print0 2>/dev/null)

  echo "Generated tiers for $count files in $directory"
}

# ── Agent-provided tier summaries ────────────────────────────
# Usage: set_tiers_explicit <file_path> <l0_text> <l1_text>
# The OpenClaw agent (an LLM) generates summaries from its own context and
# stores them via this helper. No separate Ollama/MLX service required.
# Either l0_text or l1_text may be empty to leave that tier unchanged.
set_tiers_explicit() {
  local file_path="$1" l0_text="$2" l1_text="$3"

  if [ ! -f "$file_path" ]; then
    echo "Error: file not found: $file_path" >&2
    return 1
  fi

  local dir basename
  dir="$(dirname "$file_path")"
  basename="$(basename "$file_path")"

  if [ -n "$l0_text" ]; then
    _update_tier_file "$dir/.abstract" "$basename" "$l0_text"
  fi
  if [ -n "$l1_text" ]; then
    _update_tier_file "$dir/.overview" "$basename" "$l1_text"
  fi
}

# ── Retrieve content at specified tier ───────────────────────
# Usage: retrieve_tiered <query> [L0|L1|L2] [directory]
# Returns content at the specified tier level.

retrieve_tiered() {
  local query="$1"
  local tier="${2:-L0}"
  local search_dir="${3:-${MEMORY_ROOT:-.}}"

  case "$tier" in
    L0)
      # Return .abstract files matching query
      _search_tier_files "$query" "$search_dir" ".abstract"
      ;;
    L1)
      # Return .overview files for matched directories
      _search_tier_files "$query" "$search_dir" ".overview"
      ;;
    L2)
      # Return full content — delegate to grep
      grep -rl "$query" "$search_dir" 2>/dev/null | head -20 | while IFS= read -r f; do
        echo "=== $f ==="
        cat "$f" 2>/dev/null
        echo ""
      done
      ;;
    *)
      echo "Unknown tier: $tier (use: L0, L1, L2)" >&2
      return 1
      ;;
  esac
}

# ── Search tier sidecar files ────────────────────────────────
_search_tier_files() {
  local query="$1" search_dir="$2" filename="$3"

  find "$search_dir" -name "$filename" -type f 2>/dev/null | while IFS= read -r tf; do
    local matches
    matches=$(grep -l "$query" "$tf" 2>/dev/null || true)
    if [ -n "$matches" ]; then
      echo "=== $tf ==="
      cat "$tf" 2>/dev/null
      echo ""
    fi
  done
}

# ── Auto-expand: L0 → L1 if score exceeds threshold ─────────
# Usage: auto_expand_tier <query> <l0_score> [directory]
# Returns "L0", "L1", or "L2" based on score thresholds.

auto_expand_tier() {
  local query="$1" score="$2"
  local threshold="${TIER_AUTO_EXPAND_THRESHOLD}"

  python3 -c "
score = float('$score')
threshold = float('$threshold')
if score >= threshold * 1.5:
    print('L2')
elif score >= threshold:
    print('L1')
else:
    print('L0')
" 2>/dev/null || echo "L0"
}
