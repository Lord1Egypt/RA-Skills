#!/usr/bin/env bash
# OpenViking Memory Backend — Virtual Filesystem Context DB + Router Adapter
set -euo pipefail

WRAPPER_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

BACKEND="openviking"
VENV="$HOME/.openclaw/venv"

_activate_venv() {
  if [[ -d "$VENV" && -f "$VENV/bin/activate" ]]; then
    source "$VENV/bin/activate"
  fi
}

# ============================================================
# Layer A: Native API
# ============================================================
cmd_search() {
  _activate_venv
  local query="${1:?query required}"
  local limit="${2:-5}"
  python3 -c "
import openviking as ov, json
client = ov.SyncOpenViking()
client.initialize()
results = client.find('$query', limit=$limit)
out = []
for r in results:
    out.append({'uri': r.uri, 'score': getattr(r, 'score', 0.5)})
client.close()
print(json.dumps(out, indent=2))
"
}

cmd_index() {
  _activate_venv
  local path="${1:?path required}"
  python3 -c "
import openviking as ov
client = ov.SyncOpenViking()
client.initialize()
client.add_resource(path='$path')
client.close()
print('Indexed: $path')
"
}

cmd_status() {
  _activate_venv
  python3 -c "
import openviking as ov
client = ov.SyncOpenViking()
client.initialize()
print('OpenViking: connected')
client.close()
" 2>/dev/null && echo "Status: ready" || echo "Status: unavailable"
}

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

  _activate_venv

  # Check openviking is available
  if ! python3 -c "import openviking" 2>/dev/null; then
    contract_unavailable "$query" "$BACKEND" "openviking not installed. pip install openviking"
    return 1
  fi

  local start_ms
  start_ms=$(now_ms)

  # Execute search via temp file pattern
  local tmp_results="/tmp/openclaw-ov-$$.json"
  trap "rm -f '$tmp_results'" RETURN

  local py_output
  py_output=$(python3 -c "
import json, sys
sys.path.insert(0, '$VENV/lib/python3.12/site-packages') if '$VENV' else None
import openviking as ov
client = ov.SyncOpenViking()
client.initialize()
results = client.find(sys.stdin.read().strip(), limit=20)
out = []
max_s = 0.0
for r in results:
    s = float(getattr(r, 'score', 0.5))
    content = str(client.read(r.uri))[:500] if hasattr(r, 'uri') else str(r)[:500]
    out.append({'content': content, 'relevance': round(s, 3), 'source': r.uri if hasattr(r, 'uri') else 'openviking', 'timestamp': ''})
    if s > max_s: max_s = s
client.close()
with open('$tmp_results', 'w') as f:
    json.dump(out, f)
print(len(out), round(max_s, 3))
" <<< "$query" 2>/dev/null || true)

  local end_ms duration_ms
  end_ms=$(now_ms)
  duration_ms=$(( end_ms - start_ms ))

  # Parse count and relevance from python output
  local count=0 normalized="0.0"
  if [ -n "$py_output" ]; then
    count=$(echo "$py_output" | awk '{print $1}')
    normalized=$(echo "$py_output" | awk '{print $2}')
  fi

  [ -z "$count" ] && count=0
  [ -z "$normalized" ] && normalized="0.0"

  if [ "$count" -eq 0 ] 2>/dev/null; then
    contract_empty "$query" "$BACKEND" "$duration_ms"
  else
    local results="[]"
    if [ -f "$tmp_results" ]; then
      results=$(cat "$tmp_results")
    fi
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
  --mock)    shift; cat "$INSTALL_ROOT/tests/fixtures/openviking-mock-response.json" 2>/dev/null || contract_empty "${2:-test}" "$BACKEND" 0 ;;
  health)    shift; cmd_health "$@" ;;
  "")        echo "Usage: wrapper.sh [--adapter \"query\" [--hint X] | <native-command> [args...]]"; exit 1 ;;
  *)         cmd_name="${1//-/_}"; shift; "cmd_$cmd_name" "$@" ;;
esac
