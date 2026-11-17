#!/usr/bin/env bash
# Default test path. Runs from the host and drives the container variants.
#
# Nothing here creates an externally reachable URL. Every handoff case exercised
# below is refused before the script reaches the point of starting a tunnel, so
# this path needs no external egress beyond pulling the LINE login page.
#
# Tunnel behaviour is covered separately and opt-in: containers/test/tunnel.sh
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
run="$repo_root/containers/run.sh"
image="${LINE_OA_TEST_IMAGE:-line-oa-test}"

pass=0
fail=0
check() {
  local name="$1"; shift
  if "$@" >/tmp/line-oa-check.out 2>&1; then
    printf '  ok    %s\n' "$name"; pass=$((pass + 1))
  else
    printf '  FAIL  %s\n' "$name"; sed 's/^/          /' /tmp/line-oa-check.out | head -6; fail=$((fail + 1))
  fi
}

# Asserts a command fails with a specific exit code and message fragment.
refuses() {
  local name="$1" want_code="$2" want_text="$3"; shift 3
  local out code
  out="$("$@" 2>&1)" && code=0 || code=$?
  if [[ "$code" == "$want_code" ]] && grep -qF "$want_text" <<<"$out"; then
    printf '  ok    %s\n' "$name"; pass=$((pass + 1))
  else
    printf '  FAIL  %s (exit=%s, wanted %s containing %q)\n' "$name" "$code" "$want_code" "$want_text"
    sed 's/^/          /' <<<"$out" | head -4; fail=$((fail + 1))
  fi
}

printf '\n== architecture guard ==\n'
refuses 'unset host arch is refused' 2 'emulation cannot be ruled out' \
  docker run --rm "${image}:full" true
refuses 'architecture mismatch is refused' 2 'architecture mismatch' \
  docker run --rm -e LINE_OA_CONTAINER_HOST_ARCH=amd64 "${image}:full" true
check 'matching architecture runs' bash "$run" full true

printf '\n== full variant is complete ==\n'
check 'handoff dependencies present' bash "$run" full bash -lc '
  for c in Xvfb x11vnc websockify caddy cloudflared chromium python3; do command -v "$c" >/dev/null || { echo "missing: $c"; exit 1; }; done
  for d in /usr/share/novnc /usr/share/noVNC; do [ -d "$d" ] && exit 0; done; echo "missing noVNC assets"; exit 1'
check 'playwright importable' bash "$run" full \
  /opt/line-oa-runtime/venv/bin/python -c 'import playwright'
# PYTHONPYCACHEPREFIX keeps bytecode out of the read-only source mount.
check 'send CLI compiles' bash "$run" full bash -lc \
  'PYTHONPYCACHEPREFIX=/tmp/pycache /opt/line-oa-runtime/venv/bin/python -m py_compile scripts/send_line_oa_chat.py'
check 'send CLI --help' bash "$run" full \
  bash -lc 'LINE_OA_PYTHON=/opt/line-oa-runtime/venv/bin/python bash scripts/run_line_oa_chat.sh --help'

printf '\n== isolation ==\n'
check 'workspace is read-only' bash "$run" full \
  bash -lc 'touch /workspace/__rw_probe 2>/dev/null && { echo "workspace was writable"; exit 1; }; exit 0'
check 'profile is on container-native storage' bash "$run" full \
  bash -lc 'mount | grep -q " /opt/data/chromium .*ext4" || { mount | grep " /opt/data/chromium "; exit 1; }'
refuses 'host profile override is refused' 2 'never uses a host profile' \
  env LINE_OA_SEND_CHAT_CHROMIUM_PROFILE=/tmp/pretend-real-profile bash "$run" full true

printf '\n== browser session lifecycle ==\n'
check 'session starts, CDP responds, LINE login page loads, state recorded' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/tmp/s.log 2>&1 || { tail -5 /tmp/s.log; exit 1; }
  curl --max-time 3 -fsS http://127.0.0.1:9222/json/version >/dev/null || exit 1
  curl -fsS http://127.0.0.1:9222/json/list | grep -q "line.biz" || { echo "no LINE page"; exit 1; }
  [ -f "$LINE_OA_SEND_CHAT_RUNTIME_DIR/session.env" ] || { echo "no state file"; exit 1; }'
# The session guard now runs ahead of display setup, so the refusal names the
# live session whether or not DISPLAY is set. Previously a start with no DISPLAY
# died at Xvfb and reported a display error instead of the real reason.
check 'second session is refused, naming the live session (no DISPLAY)' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1 || exit 1
  out="$(bash scripts/start_line_oa_chromium.sh 2>&1)" && { echo "second start allowed"; exit 1; }
  grep -qF "already reachable" <<<"$out" || { echo "wrong message: $out"; exit 1; }
  grep -qF "Xvfb" <<<"$out" && { echo "still reports Xvfb: $out"; exit 1; }
  exit 0'
check 'second session is refused, naming the live session (DISPLAY set)' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1 || exit 1
  out="$(DISPLAY=:99 bash scripts/start_line_oa_chromium.sh 2>&1)" || true
  grep -qF "already reachable" <<<"$out"'
check 'shutdown stops the session and leaves the profile' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1 || exit 1
  out="$(bash scripts/stop_line_oa_chromium.sh 2>&1)" || { echo "$out"; exit 1; }
  grep -qF "CDP endpoint is unreachable" <<<"$out" || exit 1
  grep -qF "persistent profile is unchanged" <<<"$out" || exit 1
  [ -f "$LINE_OA_SEND_CHAT_RUNTIME_DIR/session.env" ] && { echo "state file survived"; exit 1; }
  [ -d /opt/data/chromium ] || { echo "profile removed"; exit 1; }
  exit 0'
check 'a stale profile lock does not block the next start' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1 || exit 1
  pid=$(grep ^chromium_pid= "$LINE_OA_SEND_CHAT_RUNTIME_DIR/session.env" | cut -d= -f2)
  kill -KILL "$pid" 2>/dev/null || true            # hard kill leaves SingletonLock behind
  sleep 1; rm -f "$LINE_OA_SEND_CHAT_RUNTIME_DIR/session.env"
  pkill -f Xvfb 2>/dev/null || true; sleep 1
  out="$(bash scripts/start_line_oa_chromium.sh 2>&1)" || { echo "$out"; exit 1; }
  grep -qF "Cleared a stale profile lock" <<<"$out"'

printf '\n== front end is closed while no handoff is armed ==\n'
check 'caddy answers 404 on an unarmed session' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1 || exit 1
  port=$(grep ^caddy_port= "$LINE_OA_SEND_CHAT_RUNTIME_DIR/session.env" | cut -d= -f2)
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$port/anything")
  [ "$code" = 404 ] || { echo "got $code"; exit 1; }'

printf '\n== handoff refusals (all pre-tunnel) ==\n'
refuses 'missing handoff purpose' 2 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login' \
  bash "$run" full bash scripts/start_line_oa_vnc_handoff.sh
refuses 'wrong handoff purpose' 2 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login' \
  bash "$run" full bash -lc 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=browse bash scripts/start_line_oa_vnc_handoff.sh'
refuses 'TTL below range' 2 'must be an integer from 60 to 3600' \
  bash "$run" full bash -lc 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login LINE_OA_SEND_CHAT_HANDOFF_TTL_SECONDS=59 bash scripts/start_line_oa_vnc_handoff.sh'
refuses 'TTL above range' 2 'must be an integer from 60 to 3600' \
  bash "$run" full bash -lc 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login LINE_OA_SEND_CHAT_HANDOFF_TTL_SECONDS=3601 bash scripts/start_line_oa_vnc_handoff.sh'
refuses 'non-numeric TTL' 2 'must be an integer from 60 to 3600' \
  bash "$run" full bash -lc 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login LINE_OA_SEND_CHAT_HANDOFF_TTL_SECONDS=abc bash scripts/start_line_oa_vnc_handoff.sh'
refuses 'no browser session' 2 'no browser session is running' \
  bash "$run" full bash -lc 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login bash scripts/start_line_oa_vnc_handoff.sh'
refuses 'stale session state' 2 'not live' \
  bash "$run" full bash -lc '
    mkdir -p "$LINE_OA_SEND_CHAT_RUNTIME_DIR"
    printf "display=:99\ncdp_url=http://127.0.0.1:9222\n" > "$LINE_OA_SEND_CHAT_RUNTIME_DIR/session.env"
    LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login bash scripts/start_line_oa_vnc_handoff.sh'
check 'a refused handoff creates no external route' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1 || exit 1
  LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login LINE_OA_SEND_CHAT_HANDOFF_TTL_SECONDS=1 \
    bash scripts/start_line_oa_vnc_handoff.sh >/dev/null 2>&1 || true
  pgrep -x cloudflared >/dev/null && { echo "cloudflared is running"; exit 1; }
  [ -f "$LINE_OA_SEND_CHAT_RUNTIME_DIR/handoff.env" ] && { echo "handoff state left behind"; exit 1; }
  exit 0'

printf '\n== phase timing ==\n'
check 'session run log records phases and holds no secret' bash "$run" full bash -lc '
  bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1 || exit 1
  log=$(ls -1 "$LINE_OA_SEND_CHAT_RUNTIME_DIR"/timing/session-*.log | head -1)
  grep -q "cdp_reachable" "$log" || { echo "no phases"; exit 1; }
  grep -q "caddy_listening" "$log" || { echo "missing phase"; exit 1; }
  grep -qiE "trycloudflare|token=|password|https://" "$log" && { echo "secret-like content in log"; exit 1; }
  [ "$(stat -c %a "$log")" = 600 ] || { echo "log mode $(stat -c %a "$log")"; exit 1; }
  exit 0'

printf '\n== dependency detection drives real verdicts ==\n'
# Dependencies moved with the components they belong to: the session owns the
# display and screen-sharing stack, the handoff owns only the tunnel client.
refuses 'no-handoff-deps: session names its missing commands' 2 'missing browser-session dependencies' \
  bash "$run" no-handoff-deps bash scripts/start_line_oa_chromium.sh
refuses 'no-handoff-deps: handoff names the missing tunnel client' 2 'missing handoff dependency: cloudflared' \
  bash "$run" no-handoff-deps bash -lc 'LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login bash scripts/start_line_oa_vnc_handoff.sh'
refuses 'no-runtime reports no Playwright runtime' 2 'No Python runtime with Playwright' \
  bash "$run" no-runtime bash scripts/run_line_oa_chat.sh --recipient x --message y
# The disclaimer text mentions sudo, so the assertion is that no line *invokes*
# sudo, not that the word is absent.
check 'no-handoff-deps prints operator install instructions, invoking no sudo' bash -c '
  for cmd in "bash scripts/start_line_oa_chromium.sh" \
             "LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login bash scripts/start_line_oa_vnc_handoff.sh"; do
    out="$(bash '"$run"' no-handoff-deps bash -lc "$cmd" 2>&1 || true)"
    grep -q "apt-get" <<<"$out" || { echo "no install instructions from: $cmd"; exit 1; }
    grep -qE "^[[:space:]]*sudo " <<<"$out" && { echo "instructions invoke sudo"; exit 1; }
  done
  exit 0'
check 'unauth-profile has an initialized but session-free profile' bash "$run" unauth-profile \
  bash -lc '[ -e /opt/data/chromium/Default ] || { echo "profile not initialized"; exit 1; }'

printf '\n== environment preflight (doctor.sh) ==\n'
# Exit codes: 0 usable and authenticated, 1 blocked, 3 usable but not logged in.
# Exit 0 is unreachable in a credential-free container by design; the target
# host covers it.
check 'full: no blockers, verdict is auth-required (exit 3)' bash -c '
  out="$(bash '"$run"' full bash scripts/doctor.sh 2>&1)"; code=$?
  [ "$code" = 3 ] || { echo "exit=$code"; echo "$out" | tail -3; exit 1; }
  grep -q "environment usable; LINE authentication required" <<<"$out" || exit 1
  grep -q "NOT usable" <<<"$out" && exit 1
  exit 0'
check 'full: a running session is still reported unauthenticated' bash -c '
  out="$(bash '"$run"' full bash -lc "bash scripts/start_line_oa_chromium.sh >/dev/null 2>&1; bash scripts/doctor.sh" 2>&1)"; code=$?
  [ "$code" = 3 ] || { echo "exit=$code"; exit 1; }
  grep -q "CDP endpoint responds" <<<"$out" || exit 1
  grep -q "LINE authentication is required" <<<"$out" || exit 1
  grep -q "security checkpoint, not an installation failure" <<<"$out" || exit 1
  exit 0'
check 'unauth-profile: dependency checks pass, verdict is auth-required' bash -c '
  out="$(bash '"$run"' unauth-profile bash scripts/doctor.sh 2>&1)"; code=$?
  [ "$code" = 3 ] || { echo "exit=$code"; exit 1; }
  grep -q "display, VNC, websockify, noVNC assets" <<<"$out" || exit 1
  grep -q "environment usable; LINE authentication required" <<<"$out" || exit 1
  exit 0'
check 'no-runtime: blocked on the runtime (exit 1)' bash -c '
  out="$(bash '"$run"' no-runtime bash scripts/doctor.sh 2>&1)"; code=$?
  [ "$code" = 1 ] || { echo "exit=$code"; exit 1; }
  grep -q "no Python runtime with Playwright" <<<"$out" || exit 1
  grep -q "setup_line_oa_runtime.sh" <<<"$out" || exit 1
  exit 0'
check 'no-handoff-deps: blocked on session dependencies (exit 1)' bash -c '
  out="$(bash '"$run"' no-handoff-deps bash scripts/doctor.sh 2>&1)"; code=$?
  [ "$code" = 1 ] || { echo "exit=$code"; exit 1; }
  grep -q "missing: Xvfb x11vnc websockify caddy" <<<"$out" || exit 1
  grep -q "only the login handoff is unavailable" <<<"$out" || exit 1
  exit 0'
check 'no remediation widens a binding or invokes sudo' bash -c '
  for v in full no-runtime no-handoff-deps unauth-profile; do
    out="$(bash '"$run"' $v bash scripts/doctor.sh 2>&1 || true)"
    grep -qE "0\.0\.0\.0|--remote-debugging-address=[^1]|listen_address|expose .*(CDP|VNC|profile)" <<<"$out" \
      && { echo "$v suggests widening a binding"; exit 1; }
    grep -qE "^[[:space:]]*(→ )?sudo " <<<"$out" && { echo "$v invokes sudo"; exit 1; }
  done
  exit 0'

printf '\n== summary ==\n'
printf '  %d passed, %d failed\n\n' "$pass" "$fail"
(( fail == 0 ))
