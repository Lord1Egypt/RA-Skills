#!/usr/bin/env bash
set -euo pipefail

if ! command -v lark-cli >/dev/null 2>&1; then
  echo "FAIL lark-cli not found on PATH"
  exit 1
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

python3 - <<'PY' >"$tmp_dir/dates.env"
from datetime import datetime, timedelta, timezone

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow_start = today_start + timedelta(days=1)
start_72h = now - timedelta(hours=72)
start_7d = now - timedelta(days=7)

print(f'START_72H="{start_72h.isoformat(timespec="seconds")}"')
print(f'START_7D="{start_7d.isoformat(timespec="seconds")}"')
print(f'TODAY_START="{today_start.isoformat(timespec="seconds")}"')
print(f'TOMORROW_START="{tomorrow_start.isoformat(timespec="seconds")}"')
PY

# shellcheck disable=SC1090
source "$tmp_dir/dates.env"

run_probe() {
  local name="$1"
  shift
  local log="$tmp_dir/$name.log"

  echo "== $name =="
  if "$@" >"$log" 2>&1; then
    echo "PASS $name"
    return 0
  fi

  echo "FAIL $name"
  cat "$log"
  return 1
}

extract_first_value() {
  local log="$1"
  shift
  python3 - "$log" "$@" <<'PY'
import json
import sys

path = sys.argv[2:]
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    data = json.load(fh)

def descend(value, key):
    if isinstance(value, dict):
        return value.get(key)
    if isinstance(value, list) and key.isdigit():
        idx = int(key)
        if 0 <= idx < len(value):
            return value[idx]
    return None

cur = data
for key in path:
    cur = descend(cur, key)
    if cur is None:
        raise SystemExit(1)

if isinstance(cur, str) and cur:
    print(cur)
    raise SystemExit(0)

raise SystemExit(1)
PY
}

failures=0

run_probe docs_search \
  lark-cli docs +search --query "" --page-size 1 --format json --as user || failures=$((failures + 1))

run_probe wiki_spaces_list \
  lark-cli wiki spaces list --params '{"page_size":1}' --format json --as user || failures=$((failures + 1))

run_probe messages_search \
  lark-cli im +messages-search --query "" --start "$START_72H" --end "$TOMORROW_START" --page-size 1 --format json --as user || failures=$((failures + 1))

run_probe minutes_search \
  lark-cli minutes +search --page-size 1 --format json --as user || failures=$((failures + 1))

run_probe calendar_agenda \
  lark-cli calendar +agenda --start "$TODAY_START" --end "$TOMORROW_START" --format pretty --as user || failures=$((failures + 1))

run_probe vc_search \
  lark-cli vc +search --start "$START_7D" --page-size 1 --format pretty --as user || failures=$((failures + 1))

doc_ref=""
if [ -f "$tmp_dir/docs_search.log" ]; then
  doc_ref="$(extract_first_value "$tmp_dir/docs_search.log" items 0 url 2>/dev/null || true)"
  if [ -z "$doc_ref" ]; then
    doc_ref="$(extract_first_value "$tmp_dir/docs_search.log" data items 0 url 2>/dev/null || true)"
  fi
  if [ -z "$doc_ref" ]; then
    doc_ref="$(extract_first_value "$tmp_dir/docs_search.log" items 0 token 2>/dev/null || true)"
  fi
  if [ -z "$doc_ref" ]; then
    doc_ref="$(extract_first_value "$tmp_dir/docs_search.log" data items 0 token 2>/dev/null || true)"
  fi
  if [ -z "$doc_ref" ]; then
    doc_ref="$(extract_first_value "$tmp_dir/docs_search.log" items 0 obj_token 2>/dev/null || true)"
  fi
  if [ -z "$doc_ref" ]; then
    doc_ref="$(extract_first_value "$tmp_dir/docs_search.log" data items 0 obj_token 2>/dev/null || true)"
  fi
fi

if [ -n "$doc_ref" ]; then
  run_probe docs_fetch \
    lark-cli docs +fetch --doc "$doc_ref" --format json --as user || failures=$((failures + 1))
else
  echo "SKIP docs_fetch (no searchable doc result)"
fi

space_id=""
if [ -f "$tmp_dir/wiki_spaces_list.log" ]; then
  space_id="$(extract_first_value "$tmp_dir/wiki_spaces_list.log" items 0 space_id 2>/dev/null || true)"
  if [ -z "$space_id" ]; then
    space_id="$(extract_first_value "$tmp_dir/wiki_spaces_list.log" data items 0 space_id 2>/dev/null || true)"
  fi
fi

if [ -n "$space_id" ]; then
  run_probe wiki_nodes_list \
    lark-cli wiki nodes list --params "{\"space_id\":\"$space_id\",\"page_size\":1}" --format json --as user || failures=$((failures + 1))
else
  echo "SKIP wiki_nodes_list/wiki_get_node (no space_id found)"
fi

node_token=""
if [ -f "$tmp_dir/wiki_nodes_list.log" ]; then
  node_token="$(extract_first_value "$tmp_dir/wiki_nodes_list.log" items 0 node_token 2>/dev/null || true)"
  if [ -z "$node_token" ]; then
    node_token="$(extract_first_value "$tmp_dir/wiki_nodes_list.log" data items 0 node_token 2>/dev/null || true)"
  fi
fi

if [ -n "$node_token" ]; then
  run_probe wiki_get_node \
    lark-cli wiki spaces get_node --params "{\"token\":\"$node_token\"}" --format json --as user || failures=$((failures + 1))
elif [ -n "$space_id" ]; then
  echo "SKIP wiki_get_node (no node_token found)"
fi

minute_token=""
if [ -f "$tmp_dir/minutes_search.log" ]; then
  minute_token="$(extract_first_value "$tmp_dir/minutes_search.log" items 0 token 2>/dev/null || true)"
  if [ -z "$minute_token" ]; then
    minute_token="$(extract_first_value "$tmp_dir/minutes_search.log" data items 0 token 2>/dev/null || true)"
  fi
fi

if [ -n "$minute_token" ]; then
  run_probe minutes_get \
    lark-cli minutes minutes get --params "{\"minute_token\":\"$minute_token\"}" --format json --as user || failures=$((failures + 1))
else
  echo "SKIP minutes_get (no minute_token found)"
fi

if [ "$failures" -ne 0 ]; then
  echo
  echo "Readiness validation failed: $failures probe(s) failed."
  exit 1
fi

echo
echo "Readiness validation passed."
