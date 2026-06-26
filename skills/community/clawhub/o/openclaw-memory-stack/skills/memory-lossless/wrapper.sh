#!/usr/bin/env bash
# Lossless-Claw Memory Backend — SQLite DAG adapter + Health Check
set -euo pipefail

WRAPPER_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

BACKEND="lossless"
LCM_DB="${OPENCLAW_LCM_DB:-$HOME/.openclaw/lcm/lcm.sqlite}"

# ============================================================
# Layer A: Native API (direct SQLite access)
# ============================================================

cmd_search() {
  local query="${1:?Usage: wrapper.sh search <query>}"
  if [ ! -f "$LCM_DB" ]; then
    echo "error: LCM database not found at $LCM_DB" >&2
    return 1
  fi
  python3 -c "
import sqlite3, json, sys

conn = sqlite3.connect('$LCM_DB')
cursor = conn.execute(
    'SELECT rowid, content, created_at FROM nodes WHERE content LIKE ? ORDER BY created_at DESC LIMIT 20',
    (f'%{sys.argv[1]}%',)
)
for rowid, content, ts in cursor:
    print(f'[{rowid}] ({ts or \"no-ts\"}) {content[:200]}')
conn.close()
" "$query"
}

cmd_describe() {
  local node_id="${1:?Usage: wrapper.sh describe <node_id>}"
  if [ ! -f "$LCM_DB" ]; then
    echo "error: LCM database not found at $LCM_DB" >&2
    return 1
  fi
  python3 -c "
import sqlite3, json, sys

conn = sqlite3.connect('$LCM_DB')
cursor = conn.execute(
    'SELECT content, created_at FROM nodes WHERE rowid = ?',
    (int(sys.argv[1]),)
)
row = cursor.fetchone()
if row:
    print(row[0])
    print(f'--- timestamp: {row[1] or \"unknown\"}')
else:
    print(f'Node {sys.argv[1]} not found', file=sys.stderr)
    sys.exit(1)
conn.close()
" "$node_id"
}

cmd_status() {
  if [ ! -f "$LCM_DB" ]; then
    echo "LCM database: not found ($LCM_DB)"
    return 0
  fi
  local db_size
  db_size=$(python3 -c "import os; print(f'{os.path.getsize(\"$LCM_DB\") / 1024:.1f} KB')" 2>/dev/null || echo "unknown")
  python3 -c "
import sqlite3
conn = sqlite3.connect('$LCM_DB')
try:
    count = conn.execute('SELECT count(*) FROM nodes').fetchone()[0]
    print(f'LCM database: $LCM_DB')
    print(f'Total nodes: {count}')
    print(f'DB size: $db_size')
except Exception as e:
    print(f'LCM database: error reading ({e})')
conn.close()
"
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

  # Check DB exists
  if [ ! -f "$LCM_DB" ]; then
    contract_unavailable "$query" "$BACKEND" "LCM database not found at $LCM_DB"
    return 1
  fi

  local start_ms end_ms duration_ms
  start_ms=$(now_ms)

  local tmp_results="/tmp/openclaw-lcm-$$.json"
  trap "rm -f '$tmp_results'" RETURN

  # hint=expand: drill down into compacted nodes, returning full uncompacted content
  if [ "$hint" = "expand" ]; then
    local count normalized
    read -r count normalized < <(python3 -c "
import sqlite3, json, sys

db_path = '$LCM_DB'
query = sys.stdin.read().strip()

try:
    conn = sqlite3.connect(db_path)
    # Find the compacted node matching the query
    cursor = conn.execute(
        'SELECT rowid, content, created_at FROM nodes WHERE content LIKE ? ORDER BY created_at DESC LIMIT 5',
        (f'%{query}%',)
    )
    parent_rows = list(cursor)

    results = []
    max_score = 0.0

    for rowid, parent_content, parent_ts in parent_rows:
        # Expand: find child nodes linked to this parent via edges table
        try:
            children = conn.execute(
                'SELECT n.content, n.created_at FROM edges e JOIN nodes n ON e.target_id = n.rowid WHERE e.source_id = ? ORDER BY n.created_at ASC',
                (rowid,)
            ).fetchall()
        except:
            children = []

        if children:
            # Return expanded child nodes
            for i, (child_content, child_ts) in enumerate(children[:20]):
                score = round(max(0.3, 1.0 - i * 0.04), 3)
                results.append({
                    'content': str(child_content)[:500],
                    'relevance': score,
                    'source': 'lossless',
                    'timestamp': child_ts or '',
                    'expanded_from': str(parent_content)[:100]
                })
                if score > max_score:
                    max_score = score
        else:
            # No children — return the node itself with full content
            score = round(max(0.5, 1.0 - len(results) * 0.05), 3)
            results.append({
                'content': str(parent_content),
                'relevance': score,
                'source': 'lossless',
                'timestamp': parent_ts or '',
                'expanded_from': None
            })
            if score > max_score:
                max_score = score

    conn.close()
    with open('$tmp_results', 'w') as f:
        json.dump(results, f)
    print(len(results), round(max_score, 3))
except Exception as e:
    print(0, 0.0, file=sys.stderr)
    print(0, 0.0)
" <<< "$query" 2>/dev/null) || true

    end_ms=$(now_ms)
    duration_ms=$(( end_ms - start_ms ))

    [ -z "$count" ] && count=0
    [ -z "$normalized" ] && normalized="0.0"

    if [ "$count" -eq 0 ]; then
      contract_empty "$query" "$BACKEND" "$duration_ms"
    else
      local results
      results=$(cat "$tmp_results" 2>/dev/null || echo "[]")
      contract_success "$query" "$BACKEND" "$results" "$count" "$duration_ms" "$normalized"
    fi
    return 0
  fi

  # Standard search: LIKE query across all nodes
  local count normalized
  read -r count normalized < <(python3 -c "
import sqlite3, json, sys

db_path = '$LCM_DB'
query = sys.stdin.read().strip()

try:
    conn = sqlite3.connect(db_path)
    # Search in node content
    cursor = conn.execute(
        'SELECT content, created_at FROM nodes WHERE content LIKE ? ORDER BY created_at DESC LIMIT 20',
        (f'%{query}%',)
    )
    results = []
    max_score = 0.0
    for i, (content, ts) in enumerate(cursor):
        score = round(max(0.2, 1.0 - i * 0.05), 3)
        results.append({
            'content': str(content)[:500],
            'relevance': score,
            'source': 'lossless',
            'timestamp': ts or ''
        })
        if score > max_score:
            max_score = score
    conn.close()
    with open('$tmp_results', 'w') as f:
        json.dump(results, f)
    print(len(results), round(max_score, 3))
except Exception as e:
    print(0, 0.0, file=sys.stderr)
    print(0, 0.0)
" <<< "$query" 2>/dev/null) || true

  end_ms=$(now_ms)
  duration_ms=$(( end_ms - start_ms ))

  [ -z "$count" ] && count=0
  [ -z "$normalized" ] && normalized="0.0"

  if [ "$count" -eq 0 ]; then
    contract_empty "$query" "$BACKEND" "$duration_ms"
  else
    local results
    results=$(cat "$tmp_results" 2>/dev/null || echo "[]")
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
  --mock)    shift; cat "$INSTALL_ROOT/tests/fixtures/lossless-mock-response.json" 2>/dev/null || contract_empty "${2:-test}" "$BACKEND" 0 ;;
  health)    shift; cmd_health "$@" ;;
  "")        echo "Usage: wrapper.sh [--adapter \"query\" [--hint X] | search <query> | describe <node_id> | status | health]"; exit 1 ;;
  *)         cmd_name="${1//-/_}"; shift; "cmd_$cmd_name" "$@" ;;
esac
