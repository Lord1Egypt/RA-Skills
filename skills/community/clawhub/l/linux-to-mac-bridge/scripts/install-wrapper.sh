#!/usr/bin/env bash
set -euo pipefail

NAME=""
HOST=""
REMOTE_BIN=""
TARGET_DIR=""
SSH_KEY=""
KNOWN_HOSTS=""
WAKE_MAC=""
WAKE_BROADCAST="255.255.255.255"
WAKE_PORT="9"
WAKE_WAIT="20"
WAKE_RETRIES="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) NAME="${2:-}"; shift 2 ;;
    --host) HOST="${2:-}"; shift 2 ;;
    --remote-bin) REMOTE_BIN="${2:-}"; shift 2 ;;
    --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
    --ssh-key) SSH_KEY="${2:-}"; shift 2 ;;
    --known-hosts) KNOWN_HOSTS="${2:-}"; shift 2 ;;
    --wake-mac) WAKE_MAC="${2:-}"; shift 2 ;;
    --wake-broadcast) WAKE_BROADCAST="${2:-}"; shift 2 ;;
    --wake-port) WAKE_PORT="${2:-}"; shift 2 ;;
    --wake-wait) WAKE_WAIT="${2:-}"; shift 2 ;;
    --wake-retries) WAKE_RETRIES="${2:-}"; shift 2 ;;
    -h|--help)
      echo "usage: install-wrapper.sh --name NAME --host USER@HOST --remote-bin /abs/path --target-dir DIR [--ssh-key KEY] [--known-hosts FILE] [--wake-mac AA:BB:CC:DD:EE:FF] [--wake-broadcast IP] [--wake-port PORT] [--wake-wait SECONDS] [--wake-retries N]"
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

[[ -n "$NAME" && -n "$HOST" && -n "$REMOTE_BIN" && -n "$TARGET_DIR" ]] || {
  echo "missing required arguments" >&2
  exit 1
}

safe_name="$(printf '%s' "$NAME" | tr -cd 'a-zA-Z0-9._-')"
[[ -n "$safe_name" ]] || { echo "invalid wrapper name" >&2; exit 1; }
[[ "$REMOTE_BIN" = /* ]] || { echo "remote-bin must be absolute" >&2; exit 1; }
[[ "$WAKE_PORT" =~ ^[0-9]+$ ]] || { echo "wake-port must be an integer" >&2; exit 1; }
[[ "$WAKE_WAIT" =~ ^[0-9]+$ ]] || { echo "wake-wait must be an integer" >&2; exit 1; }
[[ "$WAKE_RETRIES" =~ ^[0-9]+$ ]] || { echo "wake-retries must be an integer" >&2; exit 1; }
if [[ -n "$WAKE_MAC" ]]; then
  [[ "$WAKE_MAC" =~ ^([[:xdigit:]]{2}[:-]){5}[[:xdigit:]]{2}$ ]] || {
    echo "wake-mac must look like AA:BB:CC:DD:EE:FF" >&2
    exit 1
  }
fi

mkdir -p "$TARGET_DIR"
wrapper="$TARGET_DIR/$safe_name"

ssh_opts=()
[[ -n "$SSH_KEY" ]] && ssh_opts+=("-i" "$SSH_KEY" "-o" "IdentitiesOnly=yes")
[[ -n "$KNOWN_HOSTS" ]] && ssh_opts+=("-o" "UserKnownHostsFile=$KNOWN_HOSTS")

{
cat <<EOF
#!/usr/bin/env bash
set -euo pipefail
HOST=$(printf '%q' "$HOST")
REMOTE_BIN=$(printf '%q' "$REMOTE_BIN")
SSH_OPTS=(
EOF
for opt in "${ssh_opts[@]-}"; do
  [[ -n "$opt" ]] || continue
  printf '  %q\n' "$opt"
done
cat <<EOF
)
WAKE_MAC=$(printf '%q' "$WAKE_MAC")
WAKE_BROADCAST=$(printf '%q' "$WAKE_BROADCAST")
WAKE_PORT=$(printf '%q' "$WAKE_PORT")
WAKE_WAIT=$(printf '%q' "$WAKE_WAIT")
WAKE_RETRIES=$(printf '%q' "$WAKE_RETRIES")

run_remote() {
  local remote_cmd
  remote_cmd=\$(printf '%q ' "\$REMOTE_BIN" "\$@")
  ssh "\${SSH_OPTS[@]}" -T "\$HOST" "bash -lc \$(printf %q "\$remote_cmd")"
}

send_wol() {
  [[ -n "\$WAKE_MAC" ]] || return 0

  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required for Wake-on-LAN support" >&2
    return 1
  fi

  python3 - "\$WAKE_MAC" "\$WAKE_BROADCAST" "\$WAKE_PORT" <<'PY'
import re
import socket
import sys

mac = sys.argv[1]
broadcast = sys.argv[2]
port = int(sys.argv[3])

normalized = re.sub(r"[^0-9A-Fa-f]", "", mac)
if len(normalized) != 12:
    raise SystemExit(f"invalid Wake-on-LAN MAC: {mac}")

payload = b"\xff" * 6 + bytes.fromhex(normalized) * 16
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(payload, (broadcast, port))
sock.close()
PY
}

if run_remote "\$@"; then
  exit 0
fi

status=\$?
[[ -n "\$WAKE_MAC" ]] || exit "\$status"

echo "Initial SSH to \$HOST failed. Sending Wake-on-LAN to \$WAKE_MAC." >&2
attempt=0
last_status="\$status"
while [[ "\$attempt" -lt "\$WAKE_RETRIES" ]]; do
  attempt=\$((attempt + 1))
  send_wol
  sleep "\$WAKE_WAIT"
  if run_remote "\$@"; then
    exit 0
  fi
  last_status=\$?
done

exit "\$last_status"
EOF
} > "$wrapper"

chmod 755 "$wrapper"
echo "Installed wrapper: $wrapper"
