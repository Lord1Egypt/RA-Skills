#!/usr/bin/env bash
set -euo pipefail

SYMBOL="${1:-}"
DAY="${2:-}"
if [ -z "$SYMBOL" ] || [ -z "$DAY" ]; then
  echo "Usage: $0 <SYMBOL> <YYYY-MM-DD>" >&2
  exit 1
fi

source "$HOME/.zshrc" >/dev/null 2>&1 || true
KEY="${MASSIVE_API_KEY:-}"
KEY="${KEY#\"}"; KEY="${KEY%\"}"; KEY="${KEY#\'}"; KEY="${KEY%\'}"

if [ -z "$KEY" ]; then
  echo "ERROR: MASSIVE_API_KEY not set" >&2
  exit 1
fi

RESP=$(curl -sS "https://api.massive.com/v2/aggs/ticker/${SYMBOL}/range/1/day/${DAY}/${DAY}?adjusted=true&sort=asc&limit=5000&apiKey=${KEY}")
python3 - <<'PY' "$RESP"
import json,sys
r=json.loads(sys.argv[1])
if r.get("status")!="OK":
    print(json.dumps(r,ensure_ascii=False))
    raise SystemExit(2)
arr=r.get("results") or []
if not arr:
    print("No data")
    raise SystemExit(3)
a=arr[0]
print(f"symbol={r.get('ticker')} open={a.get('o')} high={a.get('h')} low={a.get('l')} close={a.get('c')} volume={a.get('v')} ts_ms={a.get('t')}")
PY
