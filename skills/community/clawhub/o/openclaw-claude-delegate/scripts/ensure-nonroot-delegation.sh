#!/bin/bash
set -euo pipefail

MODE="${1:-env}"
RUNNER_USER="${2:-ccbot}"
RUNNER_HOME="${3:-/home/${RUNNER_USER}}"

OPENCLAW_ACPX_PACKAGE="${OPENCLAW_ACPX_PACKAGE:-/usr/lib/node_modules/openclaw/dist/extensions/acpx/package.json}"
ROOT_CLAUDE_LINK="${ROOT_CLAUDE_LINK:-/root/.local/bin/claude}"
ROOT_CLAUDE_CREDS="${ROOT_CLAUDE_CREDS:-/root/.claude/.credentials.json}"
ROOT_ACPX_CONFIG="${ROOT_ACPX_CONFIG:-/root/.acpx/config.json}"
DEFAULT_ACPX_SPEC="${DEFAULT_ACPX_SPEC:-0.5.3}"

fail() {
  echo "$*" >&2
  exit 1
}

[ -d "$RUNNER_HOME" ] || fail "Runner home not found: $RUNNER_HOME"
id "$RUNNER_USER" >/dev/null 2>&1 || fail "Runner user not found: $RUNNER_USER"

resolve_acpx_spec() {
  if [ -f "$OPENCLAW_ACPX_PACKAGE" ]; then
    node -e "const p=require('$OPENCLAW_ACPX_PACKAGE'); process.stdout.write((p.dependencies&&p.dependencies.acpx)||'')" 2>/dev/null || true
  fi
}

sanitize_version_label() {
  python3 - "$1" <<'PY'
import re, sys
spec = sys.argv[1]
m = re.search(r'(\d+\.\d+\.\d+)', spec)
print(m.group(1) if m else re.sub(r'[^0-9A-Za-z._-]+', '-', spec).strip('-') or 'unknown')
PY
}

ensure_runner_home_owned() {
  chown "$RUNNER_USER:$RUNNER_USER" "$RUNNER_HOME"
}

ensure_claude_binary() {
  local root_target version_name dst_dir dst_bin
  install -d -o "$RUNNER_USER" -g "$RUNNER_USER" "$RUNNER_HOME/.local/bin" "$RUNNER_HOME/.local/share/claude/versions"

  if [ -x "$ROOT_CLAUDE_LINK" ]; then
    root_target=$(readlink -f "$ROOT_CLAUDE_LINK")
    version_name=$(basename "$root_target")
    dst_bin="$RUNNER_HOME/.local/share/claude/versions/$version_name"
    if [ ! -x "$dst_bin" ] || ! cmp -s "$root_target" "$dst_bin"; then
      install -o "$RUNNER_USER" -g "$RUNNER_USER" -m 0755 "$root_target" "$dst_bin"
    fi
    ln -sfn "$dst_bin" "$RUNNER_HOME/.local/bin/claude"
    chown -h "$RUNNER_USER:$RUNNER_USER" "$RUNNER_HOME/.local/bin/claude"
  fi
}

sync_claude_auth() {
  install -d -o "$RUNNER_USER" -g "$RUNNER_USER" "$RUNNER_HOME/.claude"
  if [ -f "$ROOT_CLAUDE_CREDS" ]; then
    cp "$ROOT_CLAUDE_CREDS" "$RUNNER_HOME/.claude/.credentials.json"
    chown "$RUNNER_USER:$RUNNER_USER" "$RUNNER_HOME/.claude/.credentials.json"
    chmod 600 "$RUNNER_HOME/.claude/.credentials.json"
  fi
}

sync_acpx_config() {
  install -d -o "$RUNNER_USER" -g "$RUNNER_USER" "$RUNNER_HOME/.acpx"
  if [ -f "$ROOT_ACPX_CONFIG" ]; then
    cp "$ROOT_ACPX_CONFIG" "$RUNNER_HOME/.acpx/config.json"
    chown "$RUNNER_USER:$RUNNER_USER" "$RUNNER_HOME/.acpx/config.json"
    chmod 644 "$RUNNER_HOME/.acpx/config.json"
  fi
}

ensure_acpx_install() {
  local spec label install_root bin_path
  spec="$(resolve_acpx_spec)"
  spec="${spec:-$DEFAULT_ACPX_SPEC}"
  label="$(sanitize_version_label "$spec")"
  install_root="$RUNNER_HOME/.local/share/clawd/vendor/acpx/$label"
  bin_path="$install_root/node_modules/.bin/acpx"

  install -d -o "$RUNNER_USER" -g "$RUNNER_USER" "$install_root"
  if [ ! -x "$bin_path" ]; then
    sudo -u "$RUNNER_USER" -H env HOME="$RUNNER_HOME" npm install --prefix "$install_root" --no-save "acpx@$spec" >/dev/null 2>&1
  fi
  printf '%s\n%s\n%s\n' "$spec" "$label" "$bin_path"
}

ensure_runner_home_owned
ensure_claude_binary
sync_claude_auth
sync_acpx_config
mapfile -t ACPX_INFO < <(ensure_acpx_install)
ACPX_SPEC="${ACPX_INFO[0]}"
ACPX_LABEL="${ACPX_INFO[1]}"
ACPX_BIN="${ACPX_INFO[2]}"
CLAUDE_BIN="$RUNNER_HOME/.local/bin/claude"

case "$MODE" in
  env)
    printf "ENSURED_RUNNER_USER=%q\n" "$RUNNER_USER"
    printf "ENSURED_RUNNER_HOME=%q\n" "$RUNNER_HOME"
    printf "ENSURED_CLAUDE_BIN=%q\n" "$CLAUDE_BIN"
    printf "ENSURED_ACPX_SPEC=%q\n" "$ACPX_SPEC"
    printf "ENSURED_ACPX_LABEL=%q\n" "$ACPX_LABEL"
    printf "ENSURED_ACPX_BIN=%q\n" "$ACPX_BIN"
    ;;
  *)
    fail "Unknown mode: $MODE"
    ;;
esac
