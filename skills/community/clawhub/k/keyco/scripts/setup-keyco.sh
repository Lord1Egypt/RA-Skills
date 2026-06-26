#!/usr/bin/env bash
#
# Keyco CLI setup helper
#
# Installs the Keyco CLI via npm if missing, then prompts the user to configure
# their API key. Safe to run multiple times — exits early if already set up.
#
# Usage: bash setup-keyco.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()    { printf "${GREEN}==>${NC} %s\n" "$1"; }
warn()    { printf "${YELLOW}!!${NC} %s\n" "$1"; }
error()   { printf "${RED}xx${NC} %s\n" "$1" >&2; }

# ---------------------------------------------------------------------------
# 1. Check Node / npm
# ---------------------------------------------------------------------------
if ! command -v npm >/dev/null 2>&1; then
  error "npm is not installed."
  echo "Install Node.js (which includes npm) from https://nodejs.org"
  echo "Or via Homebrew:  brew install node"
  exit 1
fi

# ---------------------------------------------------------------------------
# 2. Install Keyco CLI if missing
# ---------------------------------------------------------------------------
if command -v keyco >/dev/null 2>&1; then
  CURRENT_VERSION="$(keyco --version 2>/dev/null || echo unknown)"
  info "Keyco CLI already installed (${CURRENT_VERSION})"
else
  info "Installing @keyco/cli globally via npm..."
  if ! npm install -g @keyco/cli; then
    warn "Global install failed. Retrying with sudo (you may be prompted for your password)..."
    sudo npm install -g @keyco/cli
  fi
  info "Installed: $(keyco --version 2>/dev/null || echo @keyco/cli)"
fi

# ---------------------------------------------------------------------------
# 3. Check configuration
# ---------------------------------------------------------------------------
CONFIG_FILE="${HOME}/.keyco.yaml"

if [[ -f "$CONFIG_FILE" ]] && grep -q "^api_key:" "$CONFIG_FILE" && ! grep -q "^api_key:[[:space:]]*$" "$CONFIG_FILE"; then
  info "Found existing config at $CONFIG_FILE"

  # Quick connectivity test
  if keyco status >/dev/null 2>&1; then
    info "Connection to Keyco API verified."
    echo
    echo "You're all set. Try:"
    echo "  keyco dub list"
    echo "  keyco analytics summary"
    exit 0
  else
    warn "Existing config found but connection failed. Re-running configure..."
  fi
else
  info "No API key configured yet."
fi

# ---------------------------------------------------------------------------
# 4. Walk user through configure
# ---------------------------------------------------------------------------
echo
echo "------------------------------------------------------------"
echo " Keyco CLI Setup"
echo "------------------------------------------------------------"
echo
echo "You'll need an API key to authenticate. Get one here:"
echo "  https://dashboard.qrdub.com  ->  Settings  ->  API Keys"
echo
echo "Recommended scopes for general CLI use:"
echo "  - dubs:read"
echo "  - analytics:read"
echo "  - lifecycles:read"
echo "  - lifecycles:create"
echo "  - workflows:read"
echo "  - groups:read"
echo
echo "API keys start with 'kc_live_' and are shown only once at creation."
echo
read -rp "Press Enter when you have your API key ready..."
echo

keyco configure

# ---------------------------------------------------------------------------
# 5. Verify
# ---------------------------------------------------------------------------
echo
info "Verifying connection..."
if keyco status; then
  echo
  info "Setup complete!"
  echo
  echo "Try one of these to get started:"
  echo "  keyco dub list"
  echo "  keyco analytics weekly-digest"
  echo "  keyco user get"
  echo "  keyco --help"
else
  error "Connection failed. Double-check your API key and base URL."
  echo "Run 'keyco configure' to try again."
  exit 1
fi
