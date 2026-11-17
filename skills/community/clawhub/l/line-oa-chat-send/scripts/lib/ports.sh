#!/usr/bin/env bash
# Loopback port selection and readiness polling. Sourced, not executed.

[[ -n "${__LINE_OA_PORTS_LOADED:-}" ]] && return 0
__LINE_OA_PORTS_LOADED=1

# pick_loopback_ports <count> [start] [end]
# Prints <count> free loopback ports, space separated, from one interpreter
# start-up rather than one per port.
pick_loopback_ports() {
  python3 - "$1" "${2:-5900}" "${3:-6999}" <<'PY'
import socket, sys

count, start, end = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
found, held = [], []
for port in range(start, end + 1):
    if len(found) == count:
        break
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", port))
    except OSError:
        sock.close()
        continue
    # Hold every chosen port until all are chosen, so one call cannot hand back
    # the same port twice.
    held.append(sock)
    found.append(port)
for sock in held:
    sock.close()
if len(found) != count:
    raise SystemExit("not enough free loopback ports in requested range")
print(" ".join(str(p) for p in found))
PY
}

# wait_for_tcp <port> <timeout-seconds> [interval-seconds]
wait_for_tcp() {
  local port="$1" timeout="$2" interval="${3:-0.05}"
  local deadline
  deadline="$(awk -v t="$timeout" 'BEGIN{printf "%.3f", t}')"
  local waited=0
  while :; do
    if python3 -c "
import socket,sys
s=socket.socket(); s.settimeout(0.3)
sys.exit(0 if s.connect_ex(('127.0.0.1', $port))==0 else 1)
" 2>/dev/null; then
      return 0
    fi
    waited="$(awk -v w="$waited" -v i="$interval" 'BEGIN{printf "%.3f", w+i}')"
    awk -v w="$waited" -v d="$deadline" 'BEGIN{exit !(w<d)}' || return 1
    sleep "$interval"
  done
}

# wait_for_x_display <display> <timeout-seconds>
# Readiness, not liveness: the X socket must accept connections. The previous
# `sleep .2` plus `kill -0` only proved the process existed, which is both
# slower than necessary in the common case and wrong in the slow case.
wait_for_x_display() {
  local display="$1" timeout="$2"
  local num="${display#:}"
  num="${num%%.*}"
  local socket_path="/tmp/.X11-unix/X${num}"
  local waited=0
  while :; do
    [[ -S "$socket_path" ]] && return 0
    waited="$(awk -v w="$waited" 'BEGIN{printf "%.3f", w+0.05}')"
    awk -v w="$waited" -v d="$timeout" 'BEGIN{exit !(w<d)}' || return 1
    sleep 0.05
  done
}

# x_display_in_use <display>
x_display_in_use() {
  local num="${1#:}"
  num="${num%%.*}"
  [[ -S "/tmp/.X11-unix/X${num}" ]]
}
