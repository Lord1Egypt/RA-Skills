#!/usr/bin/env bash
# Vertex AI Memory Bank Backend — Full native API + Router Adapter
set -euo pipefail

WRAPPER_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

BACKEND="vertex"
PLUGIN="openclaw-vertexai-memorybank"

# ============================================================
# Layer A: Native API
# ============================================================
cmd_search()    { openclaw plugins run "$PLUGIN" memorybank-search "$@"; }
cmd_remember()  { openclaw plugins run "$PLUGIN" memorybank-remember "$@"; }
cmd_forget()    { openclaw plugins run "$PLUGIN" memorybank-forget "$@"; }
cmd_sync()      { openclaw plugins run "$PLUGIN" memorybank-sync "$@"; }
cmd_stats()     { openclaw plugins run "$PLUGIN" memorybank-stats "$@"; }
cmd_status()    { openclaw plugins run "$PLUGIN" memorybank-stats "$@"; }

# ============================================================
# Layer B: Router Adapter
# ============================================================
adapter() {
  local query="" hint=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --hint) hint="$2"; shift 2 ;;
      *)      query="$1"; shift ;;
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

  # Check plugin is available
  if ! has_command openclaw; then
    contract_unavailable "$query" "$BACKEND" "openclaw CLI not found"
    return 1
  fi

  if ! openclaw plugins list 2>/dev/null | grep -q vertexai-memorybank; then
    contract_unavailable "$query" "$BACKEND" "Plugin $PLUGIN not installed. Run: openclaw plugins install $PLUGIN"
    return 1
  fi

  local start_ms
  start_ms=$(now_ms)

  # Execute search via plugin
  local raw_output=""
  raw_output=$(openclaw plugins run "$PLUGIN" memorybank-search "$query" 2>/dev/null) || true

  local end_ms duration_ms
  end_ms=$(now_ms)
  duration_ms=$(( end_ms - start_ms ))

  # Parse results
  if [ -z "$raw_output" ] || [ "$raw_output" = "null" ] || [ "$raw_output" = "[]" ]; then
    contract_empty "$query" "$BACKEND" "$duration_ms"
    return 0
  fi

  # Build results array from Vertex JSON output
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
    elif isinstance(data, dict) and 'memories' in data:
        items = data['memories']
    else:
        items = [data]

    results = []
    for item in items[:20]:
        content = item.get('content', item.get('text', item.get('memory', str(item))))
        score = float(item.get('score', item.get('relevance', item.get('similarity', 0))))
        source_path = item.get('source', item.get('scope', '$BACKEND'))
        results.append({
            'content': str(content)[:500],
            'relevance': round(min(score, 1.0), 4),
            'source': '$BACKEND',
            'timestamp': item.get('timestamp', item.get('created_at', '$(now_iso)'))
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

  # L3: functional probe (with timeout)
  local timeout_sec="${OPENCLAW_PROBE_TIMEOUT:-5}"
  if ! timeout "$timeout_sec" bash -c "$probe_l3" 2>/dev/null; then
    if [[ $? -eq 124 ]]; then
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
  --mock)    shift; cat "$INSTALL_ROOT/tests/fixtures/vertex-mock-response.json" 2>/dev/null || contract_empty "${2:-test}" "$BACKEND" 0 ;;
  health)    shift; cmd_health "$@" ;;
  "")        echo "Usage: wrapper.sh [--adapter \"query\" [--hint X] | <native-command> [args...]]"; exit 1 ;;
  *)         cmd_name="${1//-/_}"; shift; "cmd_$cmd_name" "$@" ;;
esac
