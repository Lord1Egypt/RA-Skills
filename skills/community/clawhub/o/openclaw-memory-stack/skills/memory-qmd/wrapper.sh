#!/usr/bin/env bash
# QMD Memory Backend — Full native API + Router Adapter
set -euo pipefail

WRAPPER_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

BACKEND="qmd"
QMD_CONFIG="$WRAPPER_DIR/config.json"

# Load HyDE support
source "$INSTALL_ROOT/lib/hyde.sh"
[ -f "$QMD_CONFIG" ] && hyde_load_config "$QMD_CONFIG"

# ============================================================
# Layer A: Native API
# ============================================================
cmd_search()          { qmd search "$@"; }
cmd_vsearch()         { qmd vsearch "$@"; }
cmd_query()           { qmd query "$@"; }
cmd_get()             { qmd get "$@"; }
cmd_multi_get()       { qmd multi_get "$@"; }
cmd_collection_add()  { qmd collection add "$@"; }
cmd_collection_remove() { qmd collection remove "$@"; }
cmd_collection_list() { qmd collection list "$@"; }
cmd_context_add()     { qmd context add "$@"; }
cmd_context_remove()  { qmd context remove "$@"; }
cmd_context_list()    { qmd context list "$@"; }
cmd_embed()           { qmd embed "$@"; }
cmd_update()          { qmd update "$@"; }
cmd_status()          { qmd status "$@"; }

# ============================================================
# Layer B: Router Adapter
# ============================================================
adapter() {
  local query="" hint="" use_hyde=false
  while [ $# -gt 0 ]; do
    case "$1" in
      --hint)  hint="$2"; shift 2 ;;
      --hyde)  use_hyde=true; shift ;;
      *)       query="$1"; shift ;;
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

  # Check qmd is available
  if ! has_command qmd; then
    contract_unavailable "$query" "$BACKEND" "qmd CLI not found"
    return 1
  fi

  local start_ms
  start_ms=$(now_ms)

  # Select mode based on hint
  local mode="query"
  case "$hint" in
    exact)        mode="search" ;;
    semantic)     mode="vsearch" ;;
    relationship) mode="vsearch" ;;
    timeline)     mode="search" ;;
    decision)     mode="vsearch" ;;
    grep)         mode="search" ;;
    *)            mode="search" ;;
  esac

  # HyDE expansion: for vsearch, generate hypothetical document first
  local search_query="$query"
  if [ "$mode" = "vsearch" ]; then
    if $use_hyde || hyde_is_enabled; then
      local hyde_text
      hyde_text=$(hyde_expand "$query")
      if [ -n "$hyde_text" ] && [ "$hyde_text" != "$query" ]; then
        search_query="$hyde_text"
      fi
    fi
  fi

  # Execute search
  local raw_output=""
  raw_output=$(qmd "$mode" "$search_query" --json 2>/dev/null) || true

  local end_ms duration_ms
  end_ms=$(now_ms)
  duration_ms=$(( end_ms - start_ms ))

  # Parse results
  if [ -z "$raw_output" ] || [ "$raw_output" = "null" ] || [ "$raw_output" = "[]" ]; then
    contract_empty "$query" "$BACKEND" "$duration_ms"
    return 0
  fi

  # Build results array from qmd JSON output
  local results count normalized
  if has_command python3; then
    read -r results count normalized < <(python3 -c "
import json, sys
try:
    data = json.loads('''$raw_output''')
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and 'results' in data:
        items = data['results']
    else:
        items = [data]

    results = []
    for item in items[:20]:
        content = item.get('content', item.get('text', item.get('path', str(item))))
        score = float(item.get('score', item.get('relevance', 0)))
        # Normalize: BM25 scores are 0.1-0.3, multiply by 3
        norm = min(score * 3, 1.0) if '$mode' == 'search' else score
        source_path = item.get('path', item.get('source', '$BACKEND'))
        results.append({
            'content': str(content)[:500],
            'relevance': round(norm, 4),
            'source': '$BACKEND',
            'timestamp': item.get('timestamp', '$(now_iso)')
        })

    best = max((r['relevance'] for r in results), default=0.0)
    print(json.dumps(results), len(results), round(best, 4))
except Exception as e:
    print('[]', 0, 0.0)
" 2>/dev/null)
  else
    results="[]"
    count=0
    normalized="0.0"
  fi

  [ -z "$count" ] && count=0
  [ -z "$normalized" ] && normalized="0.0"

  if [ "$count" -eq 0 ]; then
    contract_empty "$query" "$BACKEND" "$duration_ms"
  else
    contract_success "$query" "$BACKEND" "$results" "$count" "$duration_ms" "$normalized"
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
  --mock)    shift; cat "$INSTALL_ROOT/tests/fixtures/qmd-mock-response.json" 2>/dev/null || contract_empty "${2:-test}" "$BACKEND" 0 ;;
  health)    shift; cmd_health "$@" ;;
  "")        echo "Usage: wrapper.sh [--adapter \"query\" [--hint X] | <native-command> [args...]]"; exit 1 ;;
  *)         cmd_name="${1//-/_}"; shift; "cmd_$cmd_name" "$@" ;;
esac
