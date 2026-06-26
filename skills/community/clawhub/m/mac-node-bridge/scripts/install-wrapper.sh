#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  install-wrapper.sh --name NAME --host USER@HOST --remote-bin /abs/path/to/bin [--target-dir DIR]
                     [--ssh-key /abs/path/to/key] [--known-hosts /abs/path/to/known_hosts]

Creates a small wrapper script that runs a remote macOS binary over SSH.

Defaults:
  --target-dir defaults to OPENCLAW_BIN_DIR, then XDG_DATA_HOME/openclaw/bin,
  then HOME/.openclaw/bin.
EOF
}

resolve_target_dir() {
  if [[ -n "${OPENCLAW_BIN_DIR:-}" ]]; then
    printf '%s\n' "$OPENCLAW_BIN_DIR"
    return
  fi
  if [[ -n "${XDG_DATA_HOME:-}" ]]; then
    printf '%s/openclaw/bin\n' "$XDG_DATA_HOME"
    return
  fi
  printf '%s/.openclaw/bin\n' "$HOME"
}

NAME=""
HOST=""
REMOTE_BIN=""
TARGET_DIR=""
SSH_KEY=""
KNOWN_HOSTS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) NAME="${2:-}"; shift 2 ;;
    --host) HOST="${2:-}"; shift 2 ;;
    --remote-bin) REMOTE_BIN="${2:-}"; shift 2 ;;
    --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
    --ssh-key) SSH_KEY="${2:-}"; shift 2 ;;
    --known-hosts) KNOWN_HOSTS="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

TARGET_DIR="${TARGET_DIR:-$(resolve_target_dir)}"

[[ -n "$NAME" && -n "$HOST" && -n "$REMOTE_BIN" ]] || {
  usage
  exit 1
}

safe_name=$(printf '%s' "$NAME" | tr -cd 'a-zA-Z0-9._-')
[[ -n "$safe_name" ]] || { echo "Invalid wrapper name" >&2; exit 1; }
[[ "$REMOTE_BIN" = /* ]] || { echo "remote-bin must be an absolute path" >&2; exit 1; }

mkdir -p "$TARGET_DIR"
wrapper="$TARGET_DIR/$safe_name"

ssh_opts=()
if [[ -n "$SSH_KEY" ]]; then
  ssh_opts+=("-i" "$SSH_KEY" "-o" "IdentitiesOnly=yes")
fi
if [[ -n "$KNOWN_HOSTS" ]]; then
  ssh_opts+=("-o" "UserKnownHostsFile=$KNOWN_HOSTS")
fi

cat > "$wrapper" <<EOF
#!/usr/bin/env bash
set -euo pipefail
remote_cmd=\$(printf '%q ' "$REMOTE_BIN" "\$@")
exec ssh ${ssh_opts[*]:-} -T "$HOST" "bash -lc \$remote_cmd"
EOF

chmod 755 "$wrapper"
echo "Installed wrapper: $wrapper"
