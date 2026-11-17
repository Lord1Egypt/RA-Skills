#!/usr/bin/env bash
# Opt-in tunnel test. NOT part of the default test path.
#
# This is the only test that makes anything externally reachable. It arms a real
# Cloudflare Quick Tunnel, so for the life of the tunnel a browser is reachable
# by anyone holding the URL. The container holds no LINE session, so what is
# exposed is a blank LINE login page -- but the exposure is real, which is why
# running it requires an explicit opt-in.
#
#   LINE_OA_TEST_ALLOW_TUNNEL=1 containers/test/tunnel.sh [ttl-seconds]
#
# Exposure is bounded four ways: each handoff is revoked as soon as it is
# checked, the handoff's own TTL, the container's lifetime, and --rm on teardown.
# The URL is never printed.
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
ttl="${1:-60}"

if [[ "${LINE_OA_TEST_ALLOW_TUNNEL:-}" != "1" ]]; then
  cat >&2 <<'EOF'
ERROR: this test makes a browser externally reachable and is opt-in.

  It arms a real Cloudflare Quick Tunnel. Anyone holding the emitted URL gets
  interactive control of the container's browser until it is revoked. The
  container has no LINE session, so the exposed page is a login screen.

  To run it anyway:
    LINE_OA_TEST_ALLOW_TUNNEL=1 containers/test/tunnel.sh [ttl-seconds]
EOF
  exit 2
fi

[[ "$ttl" =~ ^[0-9]+$ ]] && (( ttl >= 60 && ttl <= 3600 )) || {
  printf 'ERROR: ttl must be an integer from 60 to 3600 (got %s)\n' "$ttl" >&2
  exit 2
}

printf 'Arming real tunnels with a %ss TTL. Each is revoked as soon as it is checked.\n' "$ttl"
printf 'The URL is deliberately not printed.\n\n'

exec bash "$repo_root/containers/run.sh" full bash -lc "
set -uo pipefail
export LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login
export LINE_OA_SEND_CHAT_HANDOFF_TTL_SECONDS=$ttl
state=\"\$LINE_OA_SEND_CHAT_RUNTIME_DIR/session.env\"
pass=0; fail=0
ok()   { printf '  ok    %s\n' \"\$1\"; pass=\$((pass+1)); }
bad()  { printf '  FAIL  %s\n' \"\$1\"; fail=\$((fail+1)); }

printf '\n== session ==\n'
bash scripts/start_line_oa_chromium.sh >/tmp/s.log 2>&1 && ok 'session started' || { bad 'session started'; tail -5 /tmp/s.log; }
chromium_pid=\$(grep ^chromium_pid= \"\$state\" | cut -d= -f2)

printf '\n== 6.1 arm while the session runs ==\n'
if bash scripts/start_line_oa_vnc_handoff.sh >/tmp/h1.log 2>&1; then
  ok 'handoff armed and verified'
  grep -q 'url_verified' /tmp/h1.log && ok 'verification phase recorded' || bad 'verification phase recorded'
else
  bad 'handoff armed and verified'; tail -8 /tmp/h1.log
fi
kill -0 \"\$chromium_pid\" 2>/dev/null && ok 'session uninterrupted by arming' || bad 'session uninterrupted by arming'

printf '\n== 6.5 arming twice is refused ==\n'
out=\$(bash scripts/start_line_oa_vnc_handoff.sh 2>&1)
if [ \$? -ne 0 ] && printf '%s' \"\$out\" | grep -q 'already armed'; then
  ok 'second arm refused'
else
  bad 'second arm refused'
fi
[ -f \"\$LINE_OA_SEND_CHAT_RUNTIME_DIR/handoff.env\" ] && ok 'existing handoff left intact' || bad 'existing handoff left intact'

printf '\n== 6.7 handoff run log holds no secret ==\n'
# Every invocation gets a log, including ones refused before a tunnel exists, so
# pick the log belonging to the run that actually armed.
hlog=\$(grep -l 'tunnel_url' \"\$LINE_OA_SEND_CHAT_RUNTIME_DIR\"/timing/handoff-*.log 2>/dev/null | tail -1)
if [ -n \"\$hlog\" ]; then ok 'phases recorded'; else bad 'phases recorded'; hlog=\$(ls -1t \"\$LINE_OA_SEND_CHAT_RUNTIME_DIR\"/timing/handoff-*.log | head -1); fi
grep -q 'dns_resolved' \"\$hlog\" && ok 'DNS phase recorded separately' || bad 'DNS phase recorded separately'
if grep -qiE 'trycloudflare|vnc.html|websockify\?|[0-9a-f]{64}' \"\$hlog\"; then
  bad 'run log free of URL and token'
else
  ok 'run log free of URL and token'
fi

printf '\n== 6.2 revoke leaves the session running ==\n'
bash scripts/stop_line_oa_vnc_handoff.sh >/tmp/r1.log 2>&1 && ok 'revoked' || { bad 'revoked'; cat /tmp/r1.log; }
kill -0 \"\$chromium_pid\" 2>/dev/null && ok 'Chromium still running after revoke' || bad 'Chromium still running after revoke'
curl --max-time 3 -fsS http://127.0.0.1:9222/json/version >/dev/null 2>&1 && ok 'CDP still reachable after revoke' || bad 'CDP still reachable after revoke'
pgrep -x cloudflared >/dev/null && bad 'tunnel stopped' || ok 'tunnel stopped'
port=\$(grep ^caddy_port= \"\$state\" | cut -d= -f2)
[ \"\$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:\$port/anything)\" = 404 ] && ok 'front end closed again' || bad 'front end closed again'

printf '\n== 6.4 re-arm on the same session (mid-session reauth) ==\n'
if bash scripts/start_line_oa_vnc_handoff.sh >/tmp/h2.log 2>&1; then
  ok 'second handoff armed on the same session'
else
  bad 'second handoff armed on the same session'; tail -8 /tmp/h2.log
fi
bash scripts/stop_line_oa_vnc_handoff.sh >/dev/null 2>&1

printf '\n== 6.6 verification failure prints no URL and revokes ==\n'
# Forcing this needs the grace window removed as well as a short deadline: with
# the default grace the name has usually resolved before the deadline is ever
# checked, so the run legitimately succeeds.
out=\$(LINE_OA_SEND_CHAT_HANDOFF_VERIFY_GRACE=0 LINE_OA_SEND_CHAT_HANDOFF_VERIFY_TIMEOUT=1 \
      bash scripts/start_line_oa_vnc_handoff.sh 2>&1)
code=\$?
if [ \$code -ne 0 ]; then ok 'failed verification exits non-zero'; else bad 'failed verification exits non-zero'; fi
printf '%s' \"\$out\" | grep -q 'trycloudflare' && bad 'no URL printed on failure' || ok 'no URL printed on failure'
printf '%s' \"\$out\" | grep -q 'FAILED_' && ok 'failing phase named' || bad 'failing phase named'
sleep 2
pgrep -x cloudflared >/dev/null && bad 'everything started was revoked' || ok 'everything started was revoked'
[ -f \"\$LINE_OA_SEND_CHAT_RUNTIME_DIR/handoff.env\" ] && bad 'handoff state cleaned up' || ok 'handoff state cleaned up'

printf '\n== teardown ==\n'
bash scripts/stop_line_oa_chromium.sh >/tmp/stop.log 2>&1 && ok 'session stopped' || { bad 'session stopped'; cat /tmp/stop.log; }
pgrep -x cloudflared >/dev/null && bad 'no tunnel left behind' || ok 'no tunnel left behind'

printf '\n== summary ==\n  %d passed, %d failed\n\n' \"\$pass\" \"\$fail\"
[ \$fail -eq 0 ]
"
