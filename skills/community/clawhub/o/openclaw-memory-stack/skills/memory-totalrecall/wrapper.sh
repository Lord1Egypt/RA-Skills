#!/usr/bin/env bash
# Total Recall Memory Backend — Markdown 4-tier system
# Tiers: Counter (CLAUDE.local.md), Pantry (registers/), Daily (daily/), Archive (archive/)
set -euo pipefail

WRAPPER_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

# Source A-MEM self-organize library if available
if [ -f "$INSTALL_ROOT/lib/self-organize.sh" ]; then
  source "$INSTALL_ROOT/lib/self-organize.sh"
fi

# Source deduplication library
source "$INSTALL_ROOT/lib/dedup.sh"
TR_CONFIG="$WRAPPER_DIR/config.json"
[ -f "$TR_CONFIG" ] && dedup_load_config "$TR_CONFIG"

BACKEND="totalrecall"

# ============================================================
# Discover MEMORY_ROOT
# ============================================================
discover_memory_root() {
  # 1. Explicit env var takes priority
  if [ -n "${OPENCLAW_REPO_ROOT:-}" ]; then
    echo "$OPENCLAW_REPO_ROOT"
    return 0
  fi
  # 2. Try git repo root
  local git_root
  git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
  if [ -n "$git_root" ]; then
    echo "$git_root"
    return 0
  fi
  echo ""
  return 1
}

MEMORY_ROOT="$(discover_memory_root)" || true

# ============================================================
# Layer A: Native API
# ============================================================
cmd_store() {
  # Usage: wrapper.sh store <tier> <slug> [--event-time <ISO8601>] [--tags <comma,separated>] <content...>
  local tier="$1" slug="$2"; shift 2

  # Parse optional flags
  local event_time="" tags=""
  local content_parts=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --event-time) event_time="$2"; shift 2 ;;
      --tags)       tags="$2"; shift 2 ;;
      *)            content_parts+=("$1"); shift ;;
    esac
  done
  local content="${content_parts[*]}"

  # Auto-generate record_time (when it was recorded)
  local record_time
  record_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # If no event_time provided, default to record_time
  [ -z "$event_time" ] && event_time="$record_time"

  # Build frontmatter block
  local frontmatter=""
  frontmatter="---
key: ${slug}
event_time: ${event_time}
record_time: ${record_time}"
  [ -n "$tags" ] && frontmatter="${frontmatter}
tags: ${tags}"
  frontmatter="${frontmatter}
---"

  # Dedup check: skip or merge if duplicate content exists
  if dedup_is_enabled && [ "$tier" != "counter" ]; then
    local dedup_action
    dedup_action=$(dedup_pre_store "$content" "$tier" "$slug")
    case "$dedup_action" in
      skip)
        echo "dedup: skipped duplicate for $slug" >&2
        return 0
        ;;
      merge:*)
        local merge_path="${dedup_action#merge:}"
        if [ -f "$merge_path" ]; then
          local merged_content
          merged_content=$(merge_memories "$merge_path" "$content")
          if [ -n "$merged_content" ]; then
            content="$merged_content"
            echo "dedup: merged into $merge_path" >&2
          fi
        fi
        ;;
      store|*)
        ;; # proceed normally
    esac
  fi

  case "$tier" in
    counter)
      # Counter tier: append without frontmatter (single file, line-based)
      printf '%s\n' "$content" >> "$MEMORY_ROOT/CLAUDE.local.md"
      echo "$MEMORY_ROOT/CLAUDE.local.md"
      ;;
    pantry)
      mkdir -p "$MEMORY_ROOT/memory/registers"
      local fp="$MEMORY_ROOT/memory/registers/${slug}.md"
      printf '%s\n%s\n' "$frontmatter" "$content" > "$fp"
      echo "$fp"
      ;;
    daily)
      mkdir -p "$MEMORY_ROOT/memory/daily"
      local fp="$MEMORY_ROOT/memory/daily/$(date -u +%Y-%m-%d)_${slug}.md"
      printf '%s\n%s\n' "$frontmatter" "$content" > "$fp"
      echo "$fp"
      ;;
    archive)
      mkdir -p "$MEMORY_ROOT/memory/archive"
      local fp="$MEMORY_ROOT/memory/archive/${slug}.md"
      printf '%s\n%s\n' "$frontmatter" "$content" > "$fp"
      echo "$fp"
      ;;
    *)
      echo "Unknown tier: $tier (use: counter, pantry, daily, archive)" >&2
      return 1
      ;;
  esac

  # A-MEM hook: auto-organize new memory if enabled
  if [ "${AMEM_ENABLED:-false}" = "true" ] && type organize_new_memory &>/dev/null; then
    # Run in background to avoid blocking the store operation
    (organize_new_memory "$content" > "$HOME/.openclaw/state/amem-last-organize.json" 2>/dev/null) &
  fi
}

cmd_search() {
  # Usage: wrapper.sh search <query>
  local query="$1"
  # Search across all tiers
  grep -rl "$query" \
    "$MEMORY_ROOT/CLAUDE.local.md" \
    "$MEMORY_ROOT/memory/registers/" \
    "$MEMORY_ROOT/memory/daily/" \
    "$MEMORY_ROOT/memory/archive/" \
    2>/dev/null || true
}

cmd_retrieve() {
  # Usage: wrapper.sh retrieve <query>
  local query="$1"
  local matches
  matches=$(grep -rl "$query" \
    "$MEMORY_ROOT/CLAUDE.local.md" \
    "$MEMORY_ROOT/memory/registers/" \
    "$MEMORY_ROOT/memory/daily/" \
    "$MEMORY_ROOT/memory/archive/" \
    2>/dev/null || true)
  if [ -z "$matches" ]; then
    echo "No matches found."
    return 0
  fi
  while IFS= read -r f; do
    echo "=== $f ==="
    head -c 500 "$f" 2>/dev/null || true
    echo ""
  done <<< "$matches"
}

cmd_list() {
  # Usage: wrapper.sh list [tier]
  local tier="${1:-all}"
  case "$tier" in
    counter)
      [ -f "$MEMORY_ROOT/CLAUDE.local.md" ] && echo "$MEMORY_ROOT/CLAUDE.local.md"
      ;;
    pantry)
      find "$MEMORY_ROOT/memory/registers" -name '*.md' 2>/dev/null | sort || true
      ;;
    daily)
      find "$MEMORY_ROOT/memory/daily" -name '*.md' 2>/dev/null | sort || true
      ;;
    archive)
      find "$MEMORY_ROOT/memory/archive" -name '*.md' 2>/dev/null | sort || true
      ;;
    all)
      [ -f "$MEMORY_ROOT/CLAUDE.local.md" ] && echo "$MEMORY_ROOT/CLAUDE.local.md"
      find "$MEMORY_ROOT/memory" -name '*.md' 2>/dev/null | sort || true
      ;;
    *)
      echo "Unknown tier: $tier" >&2; return 1
      ;;
  esac
}

cmd_forget() {
  # Usage: wrapper.sh forget <tier> <slug>
  local tier="$1" slug="$2"
  case "$tier" in
    counter)
      rm -f "$MEMORY_ROOT/CLAUDE.local.md"
      echo "Removed counter"
      ;;
    pantry)
      rm -f "$MEMORY_ROOT/memory/registers/${slug}.md"
      echo "Removed pantry/$slug"
      ;;
    daily)
      # slug may be partial; find matching files
      local found
      found=$(find "$MEMORY_ROOT/memory/daily" -name "*${slug}*" 2>/dev/null)
      if [ -n "$found" ]; then
        echo "$found" | xargs rm -f
        echo "Removed daily matching '$slug'"
      else
        echo "No daily entry matching '$slug'" >&2; return 1
      fi
      ;;
    archive)
      rm -f "$MEMORY_ROOT/memory/archive/${slug}.md"
      echo "Removed archive/$slug"
      ;;
    *)
      echo "Unknown tier: $tier" >&2; return 1
      ;;
  esac
}

cmd_status() {
  echo "memory_root: $MEMORY_ROOT"
  local counter_lines=0 pantry_count=0 daily_count=0 archive_count=0
  [ -f "$MEMORY_ROOT/CLAUDE.local.md" ] && counter_lines=$(wc -l < "$MEMORY_ROOT/CLAUDE.local.md" | tr -d ' ')
  [ -d "$MEMORY_ROOT/memory/registers" ] && pantry_count=$(find "$MEMORY_ROOT/memory/registers" -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
  [ -d "$MEMORY_ROOT/memory/daily" ] && daily_count=$(find "$MEMORY_ROOT/memory/daily" -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
  [ -d "$MEMORY_ROOT/memory/archive" ] && archive_count=$(find "$MEMORY_ROOT/memory/archive" -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
  echo "counter: ${counter_lines} lines"
  echo "pantry: ${pantry_count} files"
  echo "daily: ${daily_count} files"
  echo "archive: ${archive_count} files"
}

# ============================================================
# Layer B: Router Adapter
# ============================================================
adapter() {
  local query="" hint="" event_after="" event_before=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --hint)         hint="$2"; shift 2 ;;
      --event-after)  event_after="$2"; shift 2 ;;
      --event-before) event_before="$2"; shift 2 ;;
      *)              query="$1"; shift ;;
    esac
  done

  if [ -z "$query" ]; then
    contract_error "" "$BACKEND" "BACKEND_ERROR" "No query provided"
    return 1
  fi

  # Mock mode for simulation testing
  if [ "${OPENCLAW_MOCK:-}" = "1" ]; then
    cat "$INSTALL_ROOT/tests/fixtures/${BACKEND}-mock-response.json"
    return 0
  fi

  if [ -z "$MEMORY_ROOT" ]; then
    contract_unavailable "$query" "$BACKEND" "No memory root found. Run setup.sh first."
    return 1
  fi

  if [ ! -d "$MEMORY_ROOT/memory" ] && [ ! -f "$MEMORY_ROOT/CLAUDE.local.md" ]; then
    contract_unavailable "$query" "$BACKEND" "Memory directory not found at $MEMORY_ROOT. Run setup.sh first."
    return 1
  fi

  local start_ms
  start_ms=$(now_ms)

  # Search across all 4 tiers, score by tier and recency
  # Supports bi-temporal filtering via --event-after / --event-before
  local results="[]" count=0 best_score="0.0"

  if has_command python3; then
    IFS=$'\t' read -r results count best_score < <(python3 -c "
import json, os, sys, re
from datetime import datetime, timezone
from pathlib import Path

query = '''$query'''
root = '''$MEMORY_ROOT'''
event_after_str = '''$event_after'''
event_before_str = '''$event_before'''
now = datetime.now(timezone.utc)
results = []

def parse_date(s):
    \"\"\"Parse a date/datetime string into a timezone-aware datetime.\"\"\"
    if not s:
        return None
    for fmt in ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None

event_after = parse_date(event_after_str)
event_before = parse_date(event_before_str)

def extract_frontmatter(content):
    \"\"\"Extract frontmatter fields from markdown content.\"\"\"
    fm = {}
    if not content.startswith('---'):
        return fm
    parts = content.split('---', 2)
    if len(parts) < 3:
        return fm
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    return fm

def get_temporal_date(path, content):
    \"\"\"Get the best temporal date: event_time from frontmatter, fallback to file mtime.\"\"\"
    fm = extract_frontmatter(content)
    # Prefer event_time, then record_time, then file mtime
    for field in ('event_time', 'record_time'):
        dt = parse_date(fm.get(field, ''))
        if dt:
            return dt
    try:
        mt = os.path.getmtime(path)
        return datetime.fromtimestamp(mt, tz=timezone.utc)
    except:
        return now

def passes_temporal_filter(temporal_dt):
    \"\"\"Check if a date passes the event_after/event_before filters.\"\"\"
    if event_after and temporal_dt < event_after:
        return False
    if event_before and temporal_dt > event_before:
        return False
    return True

def file_mod_days(path):
    try:
        mt = os.path.getmtime(path)
        dt = datetime.fromtimestamp(mt, tz=timezone.utc)
        return (now - dt).days
    except:
        return 999

def recency_bonus(days):
    return max(0.0, 0.1 * (1.0 - days / 30.0))

def search_file(path, tier_score):
    try:
        content = Path(path).read_text(errors='replace')
    except:
        return
    lines = content.split('\n')
    matching_lines = [l.strip() for l in lines if query.lower() in l.lower()]
    if not matching_lines:
        return

    # Bi-temporal filtering
    temporal_dt = get_temporal_date(path, content)
    if not passes_temporal_filter(temporal_dt):
        return

    days = file_mod_days(path)
    score = round(tier_score + recency_bonus(days), 4)
    snippet = matching_lines[0][:200]

    fm = extract_frontmatter(content)
    results.append({
        'content': f'{os.path.relpath(path, root)}: {snippet}',
        'relevance': score,
        'source': 'totalrecall',
        'timestamp': temporal_dt.isoformat(),
        'event_time': fm.get('event_time', ''),
        'record_time': fm.get('record_time', temporal_dt.isoformat())
    })

# Counter tier (score 0.9)
counter = os.path.join(root, 'CLAUDE.local.md')
if os.path.isfile(counter):
    search_file(counter, 0.9)

# Pantry tier (score 0.8)
pantry = os.path.join(root, 'memory', 'registers')
if os.path.isdir(pantry):
    for f in os.listdir(pantry):
        if f.endswith('.md'):
            search_file(os.path.join(pantry, f), 0.8)

# Daily tier (score 0.6)
daily = os.path.join(root, 'memory', 'daily')
if os.path.isdir(daily):
    for f in os.listdir(daily):
        if f.endswith('.md'):
            search_file(os.path.join(daily, f), 0.6)

# Archive tier (score 0.4)
archive = os.path.join(root, 'memory', 'archive')
if os.path.isdir(archive):
    for f in os.listdir(archive):
        if f.endswith('.md'):
            search_file(os.path.join(archive, f), 0.4)

results.sort(key=lambda r: r['relevance'], reverse=True)
results = results[:20]
best = max((r['relevance'] for r in results), default=0.0)
print(json.dumps(results) + '\t' + str(len(results)) + '\t' + str(round(best, 4)))
" 2>/dev/null) || true
  else
    # Fallback: simple grep without scoring
    local matches
    matches=$(grep -rl "$query" \
      "$MEMORY_ROOT/CLAUDE.local.md" \
      "$MEMORY_ROOT/memory/registers/" \
      "$MEMORY_ROOT/memory/daily/" \
      "$MEMORY_ROOT/memory/archive/" \
      2>/dev/null | head -20 || true)
    if [ -n "$matches" ]; then
      count=$(echo "$matches" | wc -l | tr -d ' ')
      best_score="0.5"
      results="["
      local first=true
      while IFS= read -r f; do
        [ "$first" = true ] && first=false || results+=","
        local snippet
        snippet=$(grep -m1 "$query" "$f" 2>/dev/null | head -c 200 || echo "")
        results+="$(result_entry "$f: $snippet" "0.5" "totalrecall")"
      done <<< "$matches"
      results+="]"
    fi
  fi

  local end_ms duration_ms
  end_ms=$(now_ms)
  duration_ms=$(( end_ms - start_ms ))

  [ -z "$count" ] && count=0
  [ -z "$best_score" ] && best_score="0.0"

  if [ "$count" -eq 0 ]; then
    contract_empty "$query" "$BACKEND" "$duration_ms"
  else
    contract_success "$query" "$BACKEND" "$results" "$count" "$duration_ms" "$best_score"
  fi
}

# ============================================================
# Layer C: Health Check (three-level probe from capability.json)
# ============================================================
cmd_health() {
  local deep=false
  [[ "${1:-}" == "--deep" ]] && deep=true

  local cap_file="$WRAPPER_DIR/capability.json"
  if [[ ! -f "$cap_file" ]]; then
    contract_health "$BACKEND" "unavailable" "capability.json not found"
    return 0
  fi

  # Read probe commands from capability.json
  local probe_l1 probe_l2 probe_l3
  probe_l1=$(python3 -c "import json; print(json.load(open('$cap_file'))['probe']['l1_install'])" 2>/dev/null) || true
  probe_l2=$(python3 -c "import json; print(json.load(open('$cap_file'))['probe']['l2_runtime'])" 2>/dev/null) || true
  if $deep; then
    probe_l3=$(python3 -c "import json; d=json.load(open('$cap_file')); print(d['probe'].get('l3_deep') or d['probe']['l3_functional'])" 2>/dev/null) || true
  else
    probe_l3=$(python3 -c "import json; print(json.load(open('$cap_file'))['probe']['l3_functional'])" 2>/dev/null) || true
  fi

  # L1: install check
  if ! bash -c "$probe_l1" &>/dev/null; then
    local hint
    hint=$(python3 -c "import json; print(json.load(open('$cap_file'))['install_hint'])" 2>/dev/null || echo "")
    contract_health "$BACKEND" "unavailable" "$BACKEND not found. Install: $hint"
    return 0
  fi

  # L2: runtime check
  if ! bash -c "$probe_l2" &>/dev/null; then
    contract_health "$BACKEND" "installed" "Runtime dependencies missing"
    return 0
  fi

  # L3: functional probe (with timeout — portable across macOS/Linux)
  local timeout_sec="${OPENCLAW_PROBE_TIMEOUT:-5}"
  local l3_exit=0
  if command -v timeout &>/dev/null; then
    timeout "$timeout_sec" bash -c "$probe_l3" 2>/dev/null || l3_exit=$?
  elif command -v gtimeout &>/dev/null; then
    gtimeout "$timeout_sec" bash -c "$probe_l3" 2>/dev/null || l3_exit=$?
  else
    # POSIX fallback: run probe in background, kill after timeout
    bash -c "$probe_l3" 2>/dev/null &
    local probe_pid=$!
    ( sleep "$timeout_sec" && kill "$probe_pid" 2>/dev/null ) &
    local watchdog_pid=$!
    if wait "$probe_pid" 2>/dev/null; then
      l3_exit=0
    else
      l3_exit=$?
    fi
    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true
  fi
  if [ "$l3_exit" -ne 0 ]; then
    if [ "$l3_exit" -eq 124 ] || [ "$l3_exit" -eq 137 ]; then
      contract_health "$BACKEND" "degraded" "Functional probe timed out (${timeout_sec}s)"
    else
      contract_health "$BACKEND" "degraded" "Functional probe failed"
    fi
    return 0
  fi

  contract_health "$BACKEND" "ready" ""
}

# ============================================================
# Dispatch
# ============================================================
case "${1:-}" in
  --adapter) shift; adapter "$@" ;;
  --mock)    shift; cat "$INSTALL_ROOT/tests/fixtures/totalrecall-mock-response.json" 2>/dev/null || contract_empty "${2:-test}" "$BACKEND" 0 ;;
  health)    shift; cmd_health "$@" ;;
  "")        echo "Usage: wrapper.sh [--adapter \"query\" [--hint X] | health | store|search|list|forget|status [args...]]"; exit 1 ;;
  *)         cmd_name="${1//-/_}"; shift; "cmd_$cmd_name" "$@" ;;
esac
