#!/usr/bin/env bash
# Nowledge Mem Memory Backend — REST API + Router Adapter
set -euo pipefail

WRAPPER_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

BACKEND="nowledge"
NOWLEDGE_URL="${OPENCLAW_NOWLEDGE_URL:-http://127.0.0.1:14242}"

# ============================================================
# Layer A: Native API
# ============================================================
cmd_search() {
  local query="$1"; shift
  local encoded
  encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))" 2>/dev/null)
  curl -sf "$NOWLEDGE_URL/api/memories/search?q=$encoded" "$@"
}

cmd_store() {
  python3 -c "
import json, sys, urllib.request
content = sys.stdin.read().strip()
data = json.dumps({'content': content}).encode()
req = urllib.request.Request('$NOWLEDGE_URL/api/memories', data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
print(resp.read().decode())
" <<< "$*"
}

cmd_list() {
  local limit="${1:-50}"
  curl -sf "$NOWLEDGE_URL/api/memories?limit=$limit"
}

cmd_threads() {
  curl -sf "$NOWLEDGE_URL/api/threads"
}

cmd_status() {
  local response
  response=$(curl -sf "$NOWLEDGE_URL/api/memories?limit=1" 2>/dev/null) || {
    echo "Nowledge Mem not reachable at $NOWLEDGE_URL"
    return 1
  }
  python3 -c "
import json, sys
try:
    data = json.loads('''$response''')
    if isinstance(data, list):
        count = len(data)
    elif isinstance(data, dict):
        count = data.get('total', data.get('count', len(data.get('results', []))))
    else:
        count = 0
    print(f'Nowledge Mem: reachable, memories found: {count}')
except Exception as e:
    print(f'Nowledge Mem: reachable, response parse error: {e}')
" 2>/dev/null
}

# ============================================================
# Layer B: Router Adapter
# ============================================================
adapter() {
  local query="" hint="" depth="${OPENCLAW_NOWLEDGE_DEPTH:-1}"
  while [ $# -gt 0 ]; do
    case "$1" in
      --hint)  hint="$2"; shift 2 ;;
      --depth) depth="$2"; shift 2 ;;
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

  # Check curl is available
  if ! has_command curl; then
    contract_unavailable "$query" "$BACKEND" "curl not found"
    return 1
  fi

  local start_ms
  start_ms=$(now_ms)

  # URL-encode the query
  local encoded_query
  encoded_query=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$query" 2>/dev/null) || encoded_query="$query"

  # Multi-hop Cypher query for relationship hints with depth > 1
  if [ "$hint" = "relationship" ] && [ "$depth" -gt 1 ] 2>/dev/null; then
    local cypher_result
    cypher_result=$(python3 -c "
import json, sys, urllib.request

query = sys.argv[1]
depth = int(sys.argv[2])
url = '$NOWLEDGE_URL'

# Build Cypher query for multi-hop traversal
cypher = f'MATCH path = (a)-[*1..{depth}]-(b) WHERE a.name = \"{query}\" RETURN path'

# POST Cypher query to Nowledge API
payload = json.dumps({'cypher': cypher, 'query': query, 'depth': depth}).encode()
req = urllib.request.Request(
    f'{url}/api/memories/graph',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read().decode())
    paths = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get('paths', data.get('results', [data]))
    else:
        items = []
    for i, item in enumerate(items[:20]):
        nodes = item.get('nodes', [])
        edges = item.get('edges', item.get('relationships', []))
        path_str = ' -> '.join([n.get('name', str(n)) for n in nodes]) if nodes else str(item)
        score = round(max(0.2, 1.0 - i * 0.05), 3)
        paths.append({
            'content': path_str[:500],
            'relevance': score,
            'source': 'nowledge',
            'timestamp': item.get('timestamp', ''),
            'traversal': {'depth': depth, 'nodes': len(nodes), 'edges': len(edges)}
        })
    best = max((p['relevance'] for p in paths), default=0.0)
    print(json.dumps(paths), len(paths), round(best, 4))
except Exception as e:
    print('[]', 0, 0.0)
" "$query" "$depth" 2>/dev/null) || cypher_result=""

    if [ -n "$cypher_result" ]; then
      local c_results c_count c_normalized
      read -r c_results c_count c_normalized <<< "$cypher_result"
      if [ "${c_count:-0}" -gt 0 ]; then
        local end_ms duration_ms
        end_ms=$(now_ms)
        duration_ms=$(( end_ms - start_ms ))
        contract_success "$query" "$BACKEND" "$c_results" "$c_count" "$duration_ms" "$c_normalized"
        return 0
      fi
    fi
    # Fall through to standard search if Cypher returned nothing
  fi

  # Execute search via REST API
  local raw_output="" tmpfile
  tmpfile=$(mktemp)
  local http_code
  http_code=$(curl -sf -w '%{http_code}' -o "$tmpfile" \
    "$NOWLEDGE_URL/api/memories/search?q=$encoded_query" 2>/dev/null) || http_code="000"
  raw_output=$(cat "$tmpfile" 2>/dev/null)
  rm -f "$tmpfile"

  local end_ms duration_ms
  end_ms=$(now_ms)
  duration_ms=$(( end_ms - start_ms ))

  # Handle connection failure
  if [ "$http_code" = "000" ]; then
    contract_unavailable "$query" "$BACKEND" "Nowledge Mem not reachable at $NOWLEDGE_URL"
    return 1
  fi

  # Handle HTTP errors
  if [ "${http_code:0:1}" != "2" ]; then
    contract_error "$query" "$BACKEND" "HTTP_$http_code" "Nowledge API returned $http_code"
    return 1
  fi

  # Parse results
  if [ -z "$raw_output" ] || [ "$raw_output" = "null" ] || [ "$raw_output" = "[]" ]; then
    contract_empty "$query" "$BACKEND" "$duration_ms"
    return 0
  fi

  # Build results array from Nowledge JSON output
  local results count normalized
  if has_command python3; then
    # Use temp file to avoid shell quoting issues with raw JSON
    local pytmp
    pytmp=$(mktemp)
    printf '%s' "$raw_output" > "$pytmp"
    read -r results count normalized < <(python3 -c "
import json, sys

with open('$pytmp') as f:
    data = json.load(f)

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
    content = item.get('content', item.get('text', item.get('summary', str(item))))
    score = float(item.get('score', item.get('relevance', item.get('similarity', 0))))
    source_path = item.get('source', item.get('thread', '$BACKEND'))
    results.append({
        'content': str(content)[:500],
        'relevance': round(score, 4),
        'source': '$BACKEND',
        'timestamp': item.get('timestamp', item.get('created_at', '$(now_iso)'))
    })

best = max((r['relevance'] for r in results), default=0.0)
print(json.dumps(results), len(results), round(best, 4))
" 2>/dev/null)
    rm -f "$pytmp"
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
    contract_health "$BACKEND" "installed" "Nowledge Mem not running at $NOWLEDGE_URL"
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
# Layer D: Evolution Chains (EVOLVES relationship in graph)
# ============================================================
store_evolution() {
  local from_key="$1"      # e.g., "chose-postgres-2026-03-15"
  local to_key="$2"        # e.g., "switched-cockroachdb-2026-03-18"
  local reason="$3"        # Why the evolution happened

  if [ -z "$from_key" ] || [ -z "$to_key" ]; then
    echo '{"error": "from_key and to_key are required"}' >&2
    return 1
  fi

  local timestamp
  timestamp=$(now_iso)

  # Create an EVOLVES edge in the graph via Nowledge API
  # Store as a memory with structured evolution metadata
  python3 -c "
import json, sys, urllib.request

payload = {
    'content': json.dumps({
        'type': 'evolution',
        'from': '$from_key',
        'to': '$to_key',
        'reason': '''$(json_escape "$reason")''',
        'timestamp': '$timestamp',
        'edge': 'EVOLVES'
    }),
    'metadata': {
        'type': 'evolution_edge',
        'from_key': '$from_key',
        'to_key': '$to_key'
    }
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    '$NOWLEDGE_URL/api/memories',
    data=data,
    headers={'Content-Type': 'application/json'}
)
try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    print(json.dumps({
        'status': 'success',
        'edge': {'from': '$from_key', 'to': '$to_key', 'type': 'EVOLVES'},
        'timestamp': '$timestamp'
    }))
except Exception as e:
    print(json.dumps({'status': 'error', 'message': str(e)}))
" 2>/dev/null
}

query_evolution_timeline() {
  local entity="$1"

  if [ -z "$entity" ]; then
    echo '{"error": "entity is required"}' >&2
    return 1
  fi

  # Search for all evolution edges involving this entity
  local encoded_entity
  encoded_entity=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$entity" 2>/dev/null) || encoded_entity="$entity"

  local raw_output="" tmpfile
  tmpfile=$(mktemp)
  curl -sf -o "$tmpfile" "$NOWLEDGE_URL/api/memories/search?q=$encoded_entity" 2>/dev/null || true
  raw_output=$(cat "$tmpfile" 2>/dev/null)
  rm -f "$tmpfile"

  # Parse evolution edges and build chronological timeline
  python3 -c "
import json, sys

entity = '''$entity'''
raw = '''$(json_escape "$raw_output")'''

try:
    data = json.loads(raw) if raw else []
except:
    data = []

if isinstance(data, dict):
    data = data.get('results', data.get('memories', []))

# Filter for evolution-type entries
timeline = []
for item in data:
    content_str = item.get('content', '')
    try:
        content = json.loads(content_str)
        if content.get('type') == 'evolution':
            if entity.lower() in content.get('from', '').lower() or \
               entity.lower() in content.get('to', '').lower():
                timeline.append({
                    'from': content['from'],
                    'to': content['to'],
                    'reason': content.get('reason', ''),
                    'timestamp': content.get('timestamp', ''),
                    'edge': 'EVOLVES'
                })
    except (json.JSONDecodeError, TypeError):
        # Not an evolution entry — check if content mentions the entity
        if entity.lower() in content_str.lower() and 'evolv' in content_str.lower():
            timeline.append({
                'from': '?',
                'to': '?',
                'reason': content_str[:200],
                'timestamp': item.get('timestamp', ''),
                'edge': 'EVOLVES'
            })

# Sort chronologically
timeline.sort(key=lambda x: x.get('timestamp', ''))

result = {
    'entity': entity,
    'timeline': timeline,
    'chain_length': len(timeline),
    'status': 'success' if timeline else 'empty'
}
print(json.dumps(result, indent=2))
" 2>/dev/null
}

cmd_evolution() {
  local subcmd="${1:-}"; shift || true
  case "$subcmd" in
    store)    store_evolution "${1:-}" "${2:-}" "${3:-}" ;;
    timeline) query_evolution_timeline "${1:-}" ;;
    *)        echo "Usage: wrapper.sh evolution [store <from> <to> <reason> | timeline <entity>]"; return 1 ;;
  esac
}

# ============================================================
# Dispatch
# ============================================================
case "${1:-}" in
  --adapter) shift; adapter "$@" ;;
  --mock)    shift; cat "$INSTALL_ROOT/tests/fixtures/nowledge-mock-response.json" 2>/dev/null || contract_empty "${2:-test}" "$BACKEND" 0 ;;
  health)    shift; cmd_health "$@" ;;
  "")        echo "Usage: wrapper.sh [--adapter \"query\" [--hint X] | health | evolution [store|timeline] | search|store|list|threads|status [args...]]"; exit 1 ;;
  *)         cmd_name="${1//-/_}"; shift; "cmd_$cmd_name" "$@" ;;
esac
