#!/usr/bin/env bash
# Self-check for SKILL.md claims. Run after upgrading obscura.
#   ./scripts/smoke.sh              # verify (needs network)
#   ./scripts/smoke.sh --dump-help  # regenerate references/cli.md from `--help`
set -uo pipefail
cd "$(dirname "$0")/.."

if [ "${1:-}" = "--dump-help" ]; then
  { printf '# obscura 0.2.6 CLI reference\n\nVerbatim `--help` output, captured 2026-11-13 from the Homebrew 0.2.6 binary.\nRegenerate with `scripts/smoke.sh --dump-help`; do not hand-edit.\n\n## obscura\n\n```\n'
    obscura --help 2>&1; printf '```\n\n'
    for c in fetch scrape serve mcp; do
      printf '## obscura %s\n\n```\n' "$c"; obscura $c --help 2>&1; printf '```\n\n'
    done; } > references/cli.md
  echo "wrote references/cli.md"; exit 0
fi

command -v obscura >/dev/null || { echo "FAIL: obscura not on PATH"; exit 1; }
fails=0
ok() { printf 'ok   %s\n' "$1"; }
bad() { printf 'FAIL %s\n     %s\n' "$1" "$2"; fails=$((fails+1)); }
# assert <name> <expected> <actual>
assert() { [ "$2" = "$3" ] && ok "$1" || bad "$1" "expected [$2] got [$3]"; }
contains() { case "$3" in *"$2"*) ok "$1";; *) bad "$1" "missing [$2] in [${3:0:120}]";; esac; }

bin_dir=$(cd "$(dirname "$(command -v obscura)")" && pwd)
[ -x "$bin_dir/obscura-worker" ] && ok "obscura-worker sits beside obscura" \
  || bad "obscura-worker" "missing in $bin_dir — scrape will return nothing"

v=$(obscura --version | awk '{print $2}')
case "$v" in 0.2.*) ok "version 0.2.x ($v)";; *) bad "version" "skill targets 0.2.x, binary says $v";; esac

# --- fetch ---
t=$(obscura fetch https://example.com -q --eval "document.title" 2>/dev/null)
assert "fetch --eval document.title" "Example Domain" "$t"

contains "fetch --dump text" "documentation examples" "$(obscura fetch https://example.com -q --dump text 2>/dev/null)"

j=$(obscura fetch https://example.com -q --eval "JSON.stringify({t:document.title,n:document.querySelectorAll('p').length})" 2>/dev/null)
python3 -c 'import json,sys; d=json.loads(sys.argv[1]); assert d["n"]>0' "$j" 2>/dev/null \
  && ok "fetch --eval JSON.stringify parses" || bad "fetch --eval JSON.stringify" "$j"

orig=$(obscura fetch https://api.github.com/repos/h4ckf0r0day/obscura --dump original -q 2>/dev/null)
contains "fetch --dump original returns raw JSON" '"full_name"' "$orig"

# --- scrape ---
scrape_err=$(mktemp)
n=$(obscura scrape https://example.com https://example.org --eval "document.title" -q 2>"$scrape_err" \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["total_urls"])' 2>/dev/null)
assert "scrape json total_urls" "2" "$n"
[ -z "$n" ] && sed -n '1,10p' "$scrape_err" | sed 's/^/     stderr: /'
rm -f "$scrape_err"

lines=$(obscura scrape https://example.com https://example.org --eval "document.title" --format text -q 2>/dev/null | wc -l | tr -d ' ')
assert "scrape --format text line count" "2" "$lines"

# --- misc ---
obscura fetch https://example.com -q --dump cookies 2>/dev/null | python3 -c 'import json,sys; assert isinstance(json.load(sys.stdin),list)' 2>/dev/null \
  && ok "fetch --dump cookies is a JSON array" || bad "fetch --dump cookies" "not a JSON array"

tmp=$(mktemp -d); obscura fetch https://example.com -q -s "$tmp/s.png" >/dev/null 2>&1
[ -s "$tmp/s.png" ] && ok "fetch -s writes a PNG" || bad "fetch -s" "no file"
rm -rf "$tmp"

# SSRF guard: loopback blocked by default, guard not what blocks it once allowed
blocked=$(obscura fetch http://127.0.0.1:1/ -q 2>&1)
contains "loopback blocked by default" "private/internal IP address" "$blocked"
allowed=$(obscura fetch http://127.0.0.1:1/ --allow-private-network -q 2>&1)
case "$allowed" in *"private/internal IP address"*) bad "--allow-private-network" "still blocked";; *) ok "--allow-private-network bypasses guard";; esac

# --- mcp ---
python3 - "$fails" <<'PY'
import json, subprocess, sys
p = subprocess.Popen(["obscura","mcp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, text=True, bufsize=1)
def send(o): p.stdin.write(json.dumps(o)+"\n"); p.stdin.flush()
send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05",
      "capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}})
init = json.loads(p.stdout.readline())["result"]
send({"jsonrpc":"2.0","method":"notifications/initialized"})
send({"jsonrpc":"2.0","id":2,"method":"tools/list"})
n = len(json.loads(p.stdout.readline())["result"]["tools"])
p.kill()
print(("ok   " if n>=38 else "FAIL ") + f"mcp tools/list ({n} tools, protocol {init['protocolVersion']})")
if n < 38: sys.exit(1)
PY
[ $? -ne 0 ] && fails=$((fails+1))

echo
[ "$fails" -eq 0 ] && echo "all checks passed" || { echo "$fails check(s) failed — SKILL.md needs an update"; exit 1; }
