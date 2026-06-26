#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}✓${NC} $1"; }
warn()  { echo -e "${YELLOW}!${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
ask()   { echo -en "${YELLOW}?${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." 2>/dev/null && pwd || echo "$SCRIPT_DIR")"
PLUGIN_NAME="context-monitor.30s.sh"
SSH_TARGET=""
FORCE_MODE=""
AUTO_YES=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --remote) SSH_TARGET="$2"; FORCE_MODE="remote"; shift 2 ;;
    --local)  FORCE_MODE="local"; shift ;;
    --yes|-y) AUTO_YES=true; shift ;;
    -h|--help)
      echo "Usage: install.sh [--remote user@host] [--local] [--yes]"
      echo ""
      echo "  --remote user@host  OpenClaw runs on a remote machine (SSH key auth required)"
      echo "  --local             Force local mode (OpenClaw on this Mac)"
      echo "  --yes, -y           Skip confirmation prompts (for automated/agent usage)"
      echo "  (no args)           Auto-detect based on ~/.openclaw/agents directory"
      exit 0
      ;;
    *) echo "Usage: install.sh [--remote user@host] [--local] [--yes]"; exit 1 ;;
  esac
done

# Confirm function: auto-accepts if --yes or no TTY
confirm() {
  local msg="$1"
  if [ "$AUTO_YES" = true ] || [ ! -t 0 ]; then
    info "$msg (auto-confirmed)"
    return 0
  fi
  ask "$msg [Y/n] "
  read -r ans
  if [[ "$ans" =~ ^[Nn] ]]; then
    return 1
  fi
  return 0
}

echo ""
echo "🦞 Context Monitor — Installer"
echo "======================================="
echo ""

# ============================================================
# Pre-flight checks
# ============================================================

# --- Check macOS ---
if [ "$(uname)" != "Darwin" ]; then
  error "This skill requires macOS (SwiftBar is macOS-only)."
  echo "  SwiftBar only runs on macOS. Cannot install on $(uname)."
  exit 1
fi
info "macOS detected ($(sw_vers -productVersion 2>/dev/null || echo 'unknown version'))"

# --- Check Python3 ---
if command -v python3 &>/dev/null; then
  PY3_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  info "Python3 found ($PY3_VERSION)"
else
  error "Python3 not found."
  echo "  Install: brew install python3"
  echo "  Or: xcode-select --install"
  exit 1
fi

# --- Check Homebrew (needed for SwiftBar install) ---
BREW=""
if command -v brew &>/dev/null; then
  BREW=$(command -v brew)
elif [ -x /opt/homebrew/bin/brew ]; then
  BREW=/opt/homebrew/bin/brew
fi

# --- Detect SwiftBar plugin directory ---
PLUGIN_DIR=""
SWIFTBAR_PREFS="$HOME/Library/Preferences/com.ameba.SwiftBar.plist"
if [ -f "$SWIFTBAR_PREFS" ]; then
  CUSTOM_DIR=$(defaults read com.ameba.SwiftBar PluginDirectory 2>/dev/null || true)
  if [ -n "$CUSTOM_DIR" ] && [ -d "$CUSTOM_DIR" ]; then
    PLUGIN_DIR="$CUSTOM_DIR"
    info "SwiftBar plugin directory (from prefs): $PLUGIN_DIR"
  fi
fi
if [ -z "$PLUGIN_DIR" ]; then
  PLUGIN_DIR="$HOME/Library/Application Support/SwiftBar/Plugins"
fi

# ============================================================
# Step 1: Detect environment
# ============================================================
if [ "$FORCE_MODE" = "local" ]; then
  IS_HOST=true
  info "Forced local mode"
elif [ "$FORCE_MODE" = "remote" ]; then
  IS_HOST=false
  info "Remote mode → $SSH_TARGET"
elif [ -d "$HOME/.openclaw/agents" ]; then
  IS_HOST=true
  info "OpenClaw agents detected locally"
else
  IS_HOST=false
  warn "No local OpenClaw agents directory — assuming remote setup"
  if [ -z "$SSH_TARGET" ]; then
    error "No local OpenClaw found and no --remote flag."
    echo ""
    echo "  If OpenClaw runs on this Mac:"
    echo "    bash install.sh --local"
    echo ""
    echo "  If OpenClaw runs on another machine:"
    echo "    bash install.sh --remote user@host"
    exit 1
  fi
fi

# ============================================================
# Step 2: Install SwiftBar (with user confirmation)
# ============================================================
if [ -d "/Applications/SwiftBar.app" ]; then
  info "SwiftBar already installed"
else
  if [ -n "$BREW" ]; then
    if confirm "SwiftBar not found. Install via Homebrew?"; then
      $BREW install --cask swiftbar
      if [ -d "/Applications/SwiftBar.app" ]; then
        info "SwiftBar installed"
      else
        error "SwiftBar installation failed."
        echo "  Try manually: https://github.com/swiftbar/SwiftBar/releases"
        exit 1
      fi
    else
      error "SwiftBar is required. Install manually:"
      echo "  https://github.com/swiftbar/SwiftBar/releases"
      exit 1
    fi
  else
    error "SwiftBar not installed and Homebrew not found."
    echo ""
    echo "  Option 1: Install Homebrew first:"
    echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "    brew install --cask swiftbar"
    echo ""
    echo "  Option 2: Download SwiftBar directly:"
    echo "    https://github.com/swiftbar/SwiftBar/releases"
    echo ""
    echo "  Then run this installer again."
    exit 1
  fi
fi

# ============================================================
# Step 3: Create plugin directory
# ============================================================
mkdir -p "$PLUGIN_DIR"
if [ ! -w "$PLUGIN_DIR" ]; then
  error "Cannot write to plugin directory: $PLUGIN_DIR"
  echo "  Fix: chmod u+w \"$PLUGIN_DIR\""
  exit 1
fi

# ============================================================
# Step 4: Install based on mode
# ============================================================
if [ "$IS_HOST" = true ]; then
  # --- LOCAL MODE ---
  info "Setting up LOCAL mode (OpenClaw on this machine)"

  # Verify OpenClaw directory exists
  if [ ! -d "$HOME/.openclaw" ]; then
    error "~/.openclaw directory not found. Is OpenClaw installed?"
    exit 1
  fi

  # Install status collector
  cp "$SCRIPT_DIR/openclaw-status.py" "$HOME/.openclaw/openclaw-status.py"
  chmod +x "$HOME/.openclaw/openclaw-status.py"
  info "Status collector → ~/.openclaw/openclaw-status.py"

  # Quick test: run collector
  TEST_OUTPUT=$(python3 "$HOME/.openclaw/openclaw-status.py" 2>&1)
  if [ -n "$TEST_OUTPUT" ]; then
    AGENT_COUNT=$(echo "$TEST_OUTPUT" | wc -l | tr -d ' ')
    info "Status collector test passed ($AGENT_COUNT agents found)"
  else
    warn "Status collector returned no data (no agent sessions yet — OK for fresh installs)"
  fi

  # Install plugin (local mode — direct python call, no SSH)
  sed "s|MINI=\".*\"|MINI=\"localhost\"|" "$SCRIPT_DIR/swiftbar-plugin.sh" > "$PLUGIN_DIR/$PLUGIN_NAME"
  sed -i '' 's|RAW=$(ssh $SSH_OPTS $MINI "python3 $STATUS_SCRIPT" 2>/dev/null)|RAW=$(python3 ~/.openclaw/openclaw-status.py 2>/dev/null)|' "$PLUGIN_DIR/$PLUGIN_NAME"
  chmod +x "$PLUGIN_DIR/$PLUGIN_NAME"
  info "Plugin installed (local mode)"

else
  # --- REMOTE MODE ---
  if [ -z "$SSH_TARGET" ]; then
    error "SSH target required. Usage: install.sh --remote user@host"
    exit 1
  fi

  # Validate SSH target format
  if [[ ! "$SSH_TARGET" =~ ^[^@]+@[^@]+$ ]]; then
    error "Invalid SSH target format: $SSH_TARGET"
    echo "  Expected format: user@hostname (e.g. john@192.168.1.100)"
    exit 1
  fi

  echo ""
  warn "Testing SSH connection to $SSH_TARGET ..."

  # Test SSH connection
  if ! ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$SSH_TARGET" "echo ok" &>/dev/null; then
    error "Cannot connect to $SSH_TARGET via SSH (passwordless auth required)"
    echo ""
    echo "  Step 1 — Generate SSH key (skip if you already have one):"
    echo "    ssh-keygen -t ed25519 -N '' -f ~/.ssh/id_ed25519"
    echo ""
    echo "  Step 2 — Copy key to remote host:"
    echo "    ssh-copy-id $SSH_TARGET"
    echo ""
    echo "  Step 3 — Test connection:"
    echo "    ssh $SSH_TARGET 'echo connected'"
    echo ""
    echo "  Then run this installer again."
    exit 1
  fi
  info "SSH connection OK"

  # Check remote Python3
  REMOTE_PY3=$(ssh -o ConnectTimeout=5 -o BatchMode=yes "$SSH_TARGET" "command -v python3 2>/dev/null || true")
  if [ -z "$REMOTE_PY3" ]; then
    error "Python3 not found on remote host ($SSH_TARGET)."
    echo "  Install Python3 on the remote machine first."
    exit 1
  fi
  info "Remote Python3 found ($REMOTE_PY3)"

  # Check remote OpenClaw
  REMOTE_OPENCLAW=$(ssh -o BatchMode=yes "$SSH_TARGET" "echo \$HOME/.openclaw")
  REMOTE_HAS_OPENCLAW=$(ssh -o BatchMode=yes "$SSH_TARGET" "test -d \$HOME/.openclaw/agents && echo yes || echo no")
  if [ "$REMOTE_HAS_OPENCLAW" != "yes" ]; then
    error "No OpenClaw agents directory on $SSH_TARGET"
    echo "  Expected: $REMOTE_OPENCLAW/agents/"
    echo "  Is OpenClaw installed and configured on that machine?"
    exit 1
  fi
  info "Remote OpenClaw agents directory found"

  # Deploy status collector
  if ! scp -q -o ConnectTimeout=5 "$SCRIPT_DIR/openclaw-status.py" "$SSH_TARGET:$REMOTE_OPENCLAW/openclaw-status.py"; then
    error "Failed to copy status collector to $SSH_TARGET"
    echo "  Check SSH permissions and disk space on remote host."
    exit 1
  fi
  ssh -o BatchMode=yes "$SSH_TARGET" "chmod +x $REMOTE_OPENCLAW/openclaw-status.py"
  info "Status collector → $SSH_TARGET:~/.openclaw/openclaw-status.py"

  # Quick test: run collector remotely
  TEST_OUTPUT=$(ssh -o ConnectTimeout=5 -o BatchMode=yes "$SSH_TARGET" "python3 $REMOTE_OPENCLAW/openclaw-status.py" 2>/dev/null)
  if [ -n "$TEST_OUTPUT" ]; then
    AGENT_COUNT=$(echo "$TEST_OUTPUT" | wc -l | tr -d ' ')
    info "Remote status collector test passed ($AGENT_COUNT agents found)"
  else
    warn "Remote collector returned no data (no agent sessions yet — OK for fresh installs)"
  fi

  # Install remote-mode plugin
  sed "s|MINI=\".*\"|MINI=\"$SSH_TARGET\"|" "$SCRIPT_DIR/swiftbar-plugin.sh" > "$PLUGIN_DIR/$PLUGIN_NAME"
  chmod +x "$PLUGIN_DIR/$PLUGIN_NAME"
  info "Plugin installed (remote mode → $SSH_TARGET)"
fi

# ============================================================
# Step 5: Launch SwiftBar
# ============================================================
if ! pgrep -x SwiftBar &>/dev/null; then
  open /Applications/SwiftBar.app
  info "SwiftBar launched"

  # First launch guidance
  echo ""
  warn "First launch: SwiftBar may ask for the plugin folder."
  warn "Select: $PLUGIN_DIR"
else
  info "SwiftBar already running — plugin will refresh automatically"
fi

# ============================================================
# Done
# ============================================================
echo ""
echo "======================================="
echo "🦞 Done! Check your menu bar."
echo ""
echo "  Refresh: 30s (rename plugin file to change: 10s, 1m, 5m)"
echo "  Plugin:  $PLUGIN_DIR/$PLUGIN_NAME"
echo ""
