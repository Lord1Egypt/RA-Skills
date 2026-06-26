#!/usr/bin/env bash
set -euo pipefail

METHOD="auto"
REINSTALL="false"
VERSION=""

usage() {
  cat <<'EOF'
Usage: install_junie.sh [--method auto|script|brew|npm] [--version VERSION] [--reinstall]

Installs or reinstalls JetBrains Junie CLI using a documented method.

Options:
  --method      Install method. Default: auto
  --version     Pin a Junie version for the official installer path
  --reinstall   Reinstall even if junie is already present on PATH
  -h, --help    Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --method)
      METHOD="$2"
      shift 2
      ;;
    --version)
      VERSION="$2"
      shift 2
      ;;
    --reinstall)
      REINSTALL="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

log() {
  printf '[junie-install] %s\n' "$*"
}

fail() {
  printf '[junie-install] ERROR: %s\n' "$*" >&2
  exit 1
}

have() {
  command -v "$1" >/dev/null 2>&1
}

os_name() {
  case "$(uname -s)" in
    Darwin) echo "macos" ;;
    Linux) echo "linux" ;;
    *) echo "other" ;;
  esac
}

ensure_path_for_current_shell() {
  case ":$PATH:" in
    *":$HOME/.local/bin:"*) ;;
    *) export PATH="$HOME/.local/bin:$PATH" ;;
  esac
}

if [[ "$REINSTALL" != "true" ]] && have junie; then
  log "Junie already exists at $(command -v junie)"
  junie --version || true
  exit 0
fi

if [[ "$METHOD" == "auto" ]]; then
  if [[ "$(os_name)" == "macos" ]] && have brew; then
    METHOD="brew"
  elif have npm; then
    METHOD="npm"
  else
    METHOD="script"
  fi
fi

case "$METHOD" in
  script)
    have curl || fail "curl is required for script install"
    local_tmp="$(mktemp)"
    trap 'rm -f "$local_tmp"' EXIT
    log "Downloading official Junie installer from https://junie.jetbrains.com/install.sh"
    log "Trust note: this method downloads a shell script and executes it locally. Prefer --method brew or --method npm when that is a better fit."
    curl -fsSL https://junie.jetbrains.com/install.sh -o "$local_tmp"
    if [[ -n "$VERSION" ]]; then
      log "Running installer with JUNIE_VERSION=$VERSION"
      JUNIE_VERSION="$VERSION" bash "$local_tmp"
    else
      log "Running installer"
      bash "$local_tmp"
    fi
    ;;
  brew)
    [[ "$(os_name)" == "macos" ]] || fail "Homebrew install is only supported here on macOS"
    have brew || fail "brew is required for --method brew"
    log "Installing Junie via Homebrew"
    brew tap jetbrains/junie
    if [[ "$REINSTALL" == "true" ]]; then
      brew reinstall junie
    else
      brew install junie || brew upgrade junie
    fi
    ;;
  npm)
    have npm || fail "npm is required for --method npm"
    log "Installing Junie via npm"
    npm install -g @jetbrains/junie
    ;;
  *)
    fail "Unsupported method: $METHOD"
    ;;
esac

ensure_path_for_current_shell

have junie || fail "Junie is still not on PATH after install. Try: export PATH=\"$HOME/.local/bin:\$PATH\""

log "Installed $(command -v junie)"
junie --version
