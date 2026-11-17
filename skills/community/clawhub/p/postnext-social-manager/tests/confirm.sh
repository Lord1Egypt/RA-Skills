#!/usr/bin/env bash
# The six commands that change the account (post, schedule, cancel, delete,
# upload, analytics sync) must send NOTHING until called with the --confirm code from their own
# preview. A fake curl on PATH records every call, so each case proves whether a
# request went out. Usage: bash tests/confirm.sh   (no network, no key needed;
# PN_BASH=/bin/bash runs the helper under bash 3.2)
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PN="$HERE/postnext"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/bin"
cat > "$WORK/bin/curl" <<'EOF'
#!/usr/bin/env bash
echo "$*" >> "$CURL_LOG"
out=""; url=""; prev=""
for a in "$@"; do
  [ "$prev" = "-o" ] && out="$a"
  case "$a" in https://*) url="$a";; esac
  prev="$a"
done
body='{"success":true,"data":{}}'
case "$url" in */api/connections) body='[{"provider":"twitter","channelName":"@acme","providerId":"123"}]';; esac
if [ -n "$out" ]; then printf '%s' "$body" > "$out"; echo 200; else printf '%s' "$body"; fi
EOF
chmod +x "$WORK/bin/curl"
export CURL_LOG="$WORK/curl.log" PATH="$WORK/bin:$PATH" POSTNEXT_API_KEY=apikey_dummy-not-a-key
printf 'png-one' > "$WORK/a.png"
FUTURE="$(date -u -v+2d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '+2 days' +%Y-%m-%dT%H:%M:%SZ)"

pass=0; fail=0
ok()  { pass=$((pass+1)); printf 'ok   %s\n' "$1"; }
bad() { fail=$((fail+1)); printf 'FAIL %s\n     %s\n' "$1" "$2"; }
calls() { if [ -s "$CURL_LOG" ]; then wc -l < "$CURL_LOG" | tr -d ' '; else echo 0; fi; }
# run ARGS... -> sets OUT, RC; clears the curl log first
run() { : > "$CURL_LOG"; OUT="$(cd "$WORK" && "${PN_BASH:-bash}" "$PN" "$@" 2>&1)"; RC=$?; }
code_of() { printf '%s' "$OUT" | sed -n 's/.*--confirm \([0-9a-f]\{12\}\).*/\1/p' | tail -1; }

# check NAME ARGS... : no code -> preview, wrong code -> refused, right code -> sent
check() {
  local name="$1"; shift
  run "$@"
  if [ "$RC" -eq 3 ] && [ "$(calls)" -eq 0 ] && [[ "$OUT" == *"PREVIEW (nothing was sent)"* ]]; then ok "$name: no --confirm previews, sends nothing"
  else bad "$name: no --confirm" "rc=$RC calls=$(calls) out=$OUT"; fi
  local code; code="$(code_of)"
  run "$@" --confirm 000000000000
  if [ "$RC" -eq 3 ] && [ "$(calls)" -eq 0 ] && [[ "$OUT" == *"does not match"* ]]; then ok "$name: wrong code refused, sends nothing"
  else bad "$name: wrong code" "rc=$RC calls=$(calls) out=$OUT"; fi
  run "$@" --confirm "$code"
  if [ "$(calls)" -gt 0 ] && [[ "$OUT" != *"PREVIEW"* ]]; then ok "$name: matching code sends the request"
  else bad "$name: matching code" "rc=$RC calls=$(calls) code=$code out=$OUT"; fi
}

check "post"     post --provider twitter --text "hello" --media a.png
check "schedule" schedule --provider twitter --text "hello" --at "$FUTURE"
check "cancel"   cancel abc123
check "delete"   delete abc123
check "upload"   upload a.png
check "analytics sync" analytics sync

# a confirmed sync sends exactly one request: the POST to the sync route
run analytics sync; C="$(code_of)"
run analytics sync --confirm "$C"
if [ "$RC" -eq 0 ] && [ "$(calls)" -eq 1 ] && grep -q -- "-X POST https://api-app.postnext.io/api/v1/analytics/sync" "$CURL_LOG"; then ok "confirmed sync sends one POST to /api/v1/analytics/sync"
else bad "confirmed sync" "rc=$RC calls=$(calls) log=$(cat "$CURL_LOG")"; fi

# a code approves ONE exact operation: changed text, target or file bytes need a new one
run post --provider twitter --text "hello"; C="$(code_of)"
run post --provider twitter --text "hello, edited" --confirm "$C"
if [ "$RC" -eq 3 ] && [ "$(calls)" -eq 0 ]; then ok "changed text invalidates the code"; else bad "changed text" "rc=$RC calls=$(calls)"; fi
run delete abc123; C="$(code_of)"
run delete abc124 --confirm "$C"
if [ "$RC" -eq 3 ] && [ "$(calls)" -eq 0 ]; then ok "different target invalidates the code"; else bad "different target" "rc=$RC calls=$(calls)"; fi
run delete abc123; C="$(code_of)"
run cancel abc123 --confirm "$C"
if [ "$RC" -eq 3 ] && [ "$(calls)" -eq 0 ]; then ok "a delete code does not authorize a cancel"; else bad "op binding" "rc=$RC calls=$(calls)"; fi
run upload a.png; C="$(code_of)"
printf 'png-two' > "$WORK/a.png"
run upload a.png --confirm "$C"
if [ "$RC" -eq 3 ] && [ "$(calls)" -eq 0 ]; then ok "swapped file bytes invalidate the code"; else bad "file swap" "rc=$RC calls=$(calls)"; fi

# reads are not gated
run channels
if [ "$RC" -eq 0 ] && [ "$(calls)" -gt 0 ]; then ok "reads run without a code"; else bad "reads" "rc=$RC calls=$(calls)"; fi
run analytics overview
if [ "$RC" -eq 0 ] && [ "$(calls)" -eq 1 ]; then ok "analytics reads run without a code"; else bad "analytics reads" "rc=$RC calls=$(calls)"; fi

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
