#!/usr/bin/env bash
# OpenClaw Memory Stack — Installer
# Usage: ./install.sh [--upgrade] [--skip-models]
#
# Installs to ~/.openclaw/memory-stack/
# Does NOT touch any git repository or project directory.
#
# Exit codes:
#   0 — installed successfully
#   1 — activation failed
set -euo pipefail

# ── Resolve script location ─────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_ROOT="$HOME/.openclaw/memory-stack"
STATE_DIR="$HOME/.openclaw/state"
BIN_DIR="$HOME/.openclaw/bin"
RELEASE_BASE_URL="${OPENCLAW_RELEASE_URL:-https://openclaw-api.apptah.com/api}"

# ── Color helpers (disabled when not a terminal) ────────────────────
if [[ -t 1 ]]; then
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  RED='\033[0;31m'
  BLUE='\033[0;34m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  GREEN='' YELLOW='' RED='' BLUE='' BOLD='' NC=''
fi

ok()   { printf "${GREEN}  [OK]${NC}    %s\n" "$1"; }
warn() { printf "${YELLOW}  [WARN]${NC}  %s\n" "$1"; }
fail() { printf "${RED}  [FAIL]${NC}  %s\n" "$1"; }
info() { printf "${BLUE}  [..]${NC}    %s\n" "$1"; }
header() { printf "\n${BOLD}%s${NC}\n" "$1"; }

# ── Parse arguments ─────────────────────────────────────────────────
SKIP_MODELS=false
UPGRADE=false
FROM_SELF=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --upgrade) UPGRADE=true; shift ;;
    --from-self) FROM_SELF=true; shift ;;
    --skip-models) SKIP_MODELS=true; shift ;;
    -h|--help)
      echo "Usage: ./install.sh [--upgrade] [--skip-models]"
      echo ""
      echo "  --upgrade       Upgrade to latest version"
      echo "  --skip-models   Skip downloading QMD embedding models"
      echo "  --help          Show this help"
      echo ""
      echo "Source: https://github.com/openclaw/memory-stack"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: ./install.sh" >&2
      exit 1
      ;;
  esac
done

# ── Guards ─────────────────────────────────────────────────────────
case "$(uname -s 2>/dev/null)" in
  MINGW*|MSYS*|CYGWIN*)
    echo ""
    echo "  [ERROR] Windows is not supported natively."
    echo ""
    echo "  OpenClaw Memory Stack requires a POSIX shell environment."
    echo "  Run it inside WSL2 (recommended) or Git Bash:"
    echo ""
    echo "    WSL2:     wsl --install  (then re-run ./install.sh inside Ubuntu)"
    echo "    Git Bash: may work but path/symlink issues are possible"
    echo ""
    echo "  If you see 'plugin not found' in OpenClaw, remove the plugin entry:"
    echo "    openclaw plugin remove openclaw-memory-stack"
    echo ""
    exit 1
    ;;
esac

# WSL detection (Linux only). WSL2 is supported; WSL1 is refused because its
# Plan9 filesystem and lack of a real Linux kernel break sqlite locking + bun.
# WSL2 detection uses multiple signals because kernel naming varies — some
# WSL2 kernels report only `*-microsoft-standard` without an explicit `WSL2`
# suffix. Any one signal is sufficient for WSL2.
IS_WSL=false
IS_WSL2=false
if [[ "$(uname -s 2>/dev/null)" == "Linux" ]]; then
  if grep -qi microsoft /proc/version 2>/dev/null || grep -qi microsoft /proc/sys/kernel/osrelease 2>/dev/null; then
    IS_WSL=true
    KMAJOR=$(uname -r 2>/dev/null | cut -d. -f1)
    if [ -d /run/WSL ] \
       || [ -e /proc/sys/fs/binfmt_misc/WSLInterop-late ] \
       || grep -qi "WSL2" /proc/sys/kernel/osrelease 2>/dev/null \
       || grep -qi "WSL2" /proc/version 2>/dev/null \
       || { [ -n "$KMAJOR" ] && [ "$KMAJOR" -ge 5 ] 2>/dev/null; }; then
      IS_WSL2=true
    fi
  fi
fi

if [[ "$IS_WSL" == true && "$IS_WSL2" != true ]]; then
  echo ""
  echo "  [ERROR] WSL1 is not supported."
  echo ""
  echo "  WSL1 uses a translation layer that breaks SQLite locking and Bun."
  echo "  Upgrade to WSL2 from PowerShell (admin):"
  echo ""
  echo "    wsl --set-version <distro> 2"
  echo "    wsl --set-default-version 2"
  echo ""
  echo "  Verify with: wsl -l -v   (VERSION column should show 2)"
  echo ""
  exit 1
fi

# WSL2 + project sitting on /mnt/c (or any /mnt/<drive>): non-fatal warning.
# Cross-filesystem IO is ~10x slower and chmod/symlink semantics are unreliable,
# which causes intermittent breakage in qmd, git hooks, and node_modules.
if [[ "$IS_WSL2" == true ]]; then
  if [[ "$SCRIPT_DIR" == /mnt/* || "$HOME" == /mnt/* ]]; then
    echo ""
    echo "  [WARN] Running from a Windows-mounted path (/mnt/...)."
    echo ""
    echo "  WSL2 cross-filesystem IO is slow and chmod/symlinks may misbehave."
    echo "  Recommended: clone into your Linux home and re-run:"
    echo ""
    echo "    cp -R \"$SCRIPT_DIR\" ~/openclaw-memory-stack"
    echo "    cd ~/openclaw-memory-stack && ./install.sh"
    echo ""
    echo "  Continuing in 5 seconds — Ctrl+C to abort..."
    sleep 5
  fi
fi

if [[ "$FROM_SELF" == true && "$UPGRADE" != true ]]; then
  echo "Error: --from-self is an internal flag. Use --upgrade instead." >&2
  exit 1
fi

# ── Upgrade flow ───────────────────────────────────────────────────
if [[ "$UPGRADE" == true && "$FROM_SELF" != true ]]; then
  header "Upgrade — Phase 1: Download"

  CURRENT_VERSION=$(python3 -c "import json; print(json.load(open('$INSTALL_ROOT/version.json'))['version'])" 2>/dev/null || echo "0.0.0")

  info "Current version: $CURRENT_VERSION"
  info "Downloading latest release..."

  DOWNLOAD_URL="$RELEASE_BASE_URL/download/latest"
  TMP_TAR="${TMPDIR:-/tmp}/openclaw-update-$$.tar.gz"
  TMP_DIR="${TMPDIR:-/tmp}/openclaw-update-$$"

  HTTP_CODE=$(curl -sL -w "%{http_code}" -o "$TMP_TAR" "$DOWNLOAD_URL")
  if [[ "$HTTP_CODE" != "200" ]]; then
    fail "Download failed (HTTP $HTTP_CODE)"
    rm -f "$TMP_TAR"
    exit 1
  fi

  # Verify SHA-256 checksum (mandatory — prevents tampered downloads)
  SHA256_URL="$RELEASE_BASE_URL/download/latest/sha256"
  [[ -n "${ENCODED_EMAIL:-}" ]] && SHA256_URL="${SHA256_URL}&email=$ENCODED_EMAIL"
  EXPECTED_SHA=$(curl -sf "$SHA256_URL" 2>/dev/null || echo "")
  if [[ -z "$EXPECTED_SHA" ]]; then
    fail "Could not fetch checksum from server — aborting for safety"
    fail "  If this persists, contact support@apptah.com"
    rm -f "$TMP_TAR"
    exit 1
  fi
  if command -v shasum &>/dev/null; then
    ACTUAL_SHA=$(shasum -a 256 "$TMP_TAR" | cut -d' ' -f1)
  elif command -v sha256sum &>/dev/null; then
    ACTUAL_SHA=$(sha256sum "$TMP_TAR" | cut -d' ' -f1)
  else
    fail "Neither shasum nor sha256sum found — cannot verify download integrity"
    rm -f "$TMP_TAR"
    exit 1
  fi
  if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
    fail "Checksum mismatch — download may be corrupted or tampered"
    fail "  Expected: $EXPECTED_SHA"
    fail "  Actual:   $ACTUAL_SHA"
    rm -f "$TMP_TAR"
    exit 1
  fi
  ok "SHA-256 checksum verified"

  # Verify tarball integrity
  if ! tar -tzf "$TMP_TAR" > /dev/null 2>&1; then
    fail "Downloaded file is corrupt"
    rm -f "$TMP_TAR"
    exit 1
  fi

  if ! tar -tzf "$TMP_TAR" | grep -q 'install.sh'; then
    fail "Invalid package: no installer found"
    rm -f "$TMP_TAR"
    exit 1
  fi

  # Extract and check version
  mkdir -p "$TMP_DIR"
  tar -xzf "$TMP_TAR" -C "$TMP_DIR"
  rm -f "$TMP_TAR"

  # Find the extracted directory
  EXTRACTED_DIR=$(find "$TMP_DIR" -maxdepth 1 -type d -name "openclaw-memory-stack-*" | head -1)
  if [[ -z "$EXTRACTED_DIR" ]]; then
    EXTRACTED_DIR="$TMP_DIR"
  fi

  if [[ ! -f "$EXTRACTED_DIR/install.sh" ]]; then
    fail "Extracted package missing install.sh"
    rm -rf "$TMP_DIR"
    exit 1
  fi

  # Version check: new must be strictly greater than current
  NEW_VERSION=$(python3 -c "import json; print(json.load(open('$EXTRACTED_DIR/version.json'))['version'])" 2>/dev/null || echo "")
  if [[ -z "$NEW_VERSION" ]]; then
    fail "Could not read version from downloaded package"
    rm -rf "$TMP_DIR"
    exit 1
  fi

  IS_NEWER=$(python3 -c "
cv = list(map(int, '$CURRENT_VERSION'.split('.')))
nv = list(map(int, '$NEW_VERSION'.split('.')))
print('yes' if nv > cv else 'no')
" 2>/dev/null || echo "no")

  if [[ "$IS_NEWER" != "yes" ]]; then
    ok "Already up to date (v$CURRENT_VERSION)"
    rm -rf "$TMP_DIR"
    exit 0
  fi

  info "Upgrading v$CURRENT_VERSION → v$NEW_VERSION"
  ok "Download verified"

  chmod +x "$EXTRACTED_DIR/install.sh"
  exec "$EXTRACTED_DIR/install.sh" --upgrade --from-self
fi

if [[ "$UPGRADE" == true && "$FROM_SELF" == true ]]; then
  header "Upgrade — Phase 2: Install"

  NEW_VERSION=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/version.json'))['version'])" 2>/dev/null || echo "unknown")

  # Copy files
  info "Copying files..."
  for dir in bin lib skills; do
    if [[ -d "$SCRIPT_DIR/$dir" ]]; then
      cp -R "$SCRIPT_DIR/$dir/" "$INSTALL_ROOT/$dir/"
    fi
  done
  # Ensure qmd-compat shim is executable
  [[ -f "$INSTALL_ROOT/bin/openclaw-memory-qmd" ]] && chmod +x "$INSTALL_ROOT/bin/openclaw-memory-qmd"
  # Ensure symlink exists
  ln -sf "$INSTALL_ROOT/bin/openclaw-memory-qmd" "$BIN_DIR/openclaw-memory-qmd" 2>/dev/null || true
  ok "Files updated"

  # Copy plugin
  EXT_DIR="$HOME/.openclaw/extensions/openclaw-memory-stack"
  mkdir -p "$EXT_DIR"
  if [[ -f "$SCRIPT_DIR/plugin/dist/index.mjs" ]]; then
    mkdir -p "$EXT_DIR/dist"
    cp "$SCRIPT_DIR/plugin/dist/index.mjs" "$EXT_DIR/dist/"
  else
    cp "$SCRIPT_DIR/plugin/index.mjs" "$EXT_DIR/"
  fi
  cp "$SCRIPT_DIR/plugin/package.json" "$EXT_DIR/"
  [[ -f "$SCRIPT_DIR/plugin/openclaw.plugin.json" ]] && cp "$SCRIPT_DIR/plugin/openclaw.plugin.json" "$EXT_DIR/"
  [[ -f "$SCRIPT_DIR/openclaw.plugin.json" ]] && cp "$SCRIPT_DIR/openclaw.plugin.json" "$EXT_DIR/"
  # Copy lib/ modules to both paths needed by the bundle:
  #   dist/index.mjs imports ./lib/llm.mjs  → $EXT_DIR/dist/lib/
  #   dist/index.mjs imports ../lib/llm.mjs → $EXT_DIR/lib/
  if [[ -d "$SCRIPT_DIR/plugin/lib" ]]; then
    rm -rf "$EXT_DIR/lib" "$EXT_DIR/dist/lib"
    cp -R "$SCRIPT_DIR/plugin/lib" "$EXT_DIR/lib"
    cp -R "$SCRIPT_DIR/plugin/lib" "$EXT_DIR/dist/lib"
  fi
  ok "Plugin updated"

  # Update version.json
  NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  OLD_VERSION=$(python3 -c "import json; print(json.load(open('$INSTALL_ROOT/version.json')).get('version','unknown'))" 2>/dev/null || echo "unknown")
  cat > "$INSTALL_ROOT/version.json" <<JSONEOF
{
  "version": "$NEW_VERSION",
  "installed_at": "$NOW",
  "upgraded_from": "$OLD_VERSION"
}
JSONEOF
  ok "version.json → v$NEW_VERSION"

  # Update openclaw.json plugin install record
  OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"
  if [[ -f "$OPENCLAW_JSON" ]] && command -v python3 &>/dev/null; then
    python3 -c "
import json, datetime
config_path = '$OPENCLAW_JSON'
with open(config_path) as f:
    config = json.load(f)
installs = config.get('plugins', {}).get('installs', {})
if 'openclaw-memory-stack' in installs:
    installs['openclaw-memory-stack']['version'] = '$NEW_VERSION'
    installs['openclaw-memory-stack']['resolvedVersion'] = '$NEW_VERSION'
    installs['openclaw-memory-stack']['resolvedSpec'] = 'openclaw-memory-stack@$NEW_VERSION'
    installs['openclaw-memory-stack']['updatedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null && ok "openclaw.json updated" || warn "Could not update openclaw.json version"
  fi

  # Update Python deps if venv exists
  if [[ -d "$INSTALL_ROOT/.venv" && -f "$SCRIPT_DIR/requirements.txt" ]]; then
    info "Updating Python dependencies..."
    "$INSTALL_ROOT/.venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt" --quiet 2>/dev/null && ok "Python deps updated" || warn "Python deps update failed (non-fatal)"
  fi

  # Clean up tmp dir if we were exec'd from Phase 1
  PARENT_TMP=$(dirname "$SCRIPT_DIR")
  if [[ "$PARENT_TMP" == "${TMPDIR:-/tmp}/openclaw-update-"* ]] || [[ "$PARENT_TMP" == /tmp/openclaw-update-* ]]; then
    rm -rf "$PARENT_TMP"
  fi

  echo ""
  echo -e "${BOLD}=========================================${NC}"
  echo -e "${GREEN}  ✅ Updated to v$NEW_VERSION${NC}"
  echo -e "${BOLD}=========================================${NC}"
  echo ""
  if command -v openclaw &>/dev/null; then
    openclaw gateway restart 2>/dev/null &
    disown
    echo "  OpenClaw gateway restarting."
  else
    echo "  Start OpenClaw when ready."
  fi
  echo ""
  exit 0
fi

# ── Banner ──────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}=========================================${NC}"
echo -e "${BOLD}  OpenClaw Memory Stack — Installer${NC}"
echo -e "${BOLD}=========================================${NC}"
echo -e "  Date: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

# ── Step 1: Detect platform capabilities ────────────────────────────
header "Step 1/5 — Checking platform"

OS="unknown"
case "$(uname -s)" in
  Darwin*) OS="macOS" ;;
  Linux*)  OS="Linux" ;;
  *)       OS="$(uname -s)" ;;
esac
ok "Platform: $OS"

# ── Runtime bootstrap helpers ────────────────────────────────────────
install_git() {
  if command -v git &>/dev/null; then
    return 0
  fi
  info "Installing git..."
  local _sudo=""
  command -v sudo &>/dev/null && _sudo="sudo"
  if command -v apt-get &>/dev/null; then
    $_sudo apt-get update -qq 2>/dev/null && $_sudo apt-get install -y git --quiet 2>/dev/null && ok "git installed" && return 0
  elif command -v yum &>/dev/null; then
    $_sudo yum install -y git --quiet 2>/dev/null && ok "git installed" && return 0
  elif command -v pacman &>/dev/null; then
    $_sudo pacman -Sy --noconfirm git 2>/dev/null && ok "git installed" && return 0
  fi
  warn "Could not auto-install git. Install manually: sudo apt-get install git"
  return 1
}

# Check runtime capabilities for backends
GIT_READY=false
BUN_READY=false

if command -v git &>/dev/null; then
  ok "git: $(git --version 2>/dev/null | head -1)"
  GIT_READY=true
else
  install_git && GIT_READY=true
  if $GIT_READY; then
    ok "git: $(git --version 2>/dev/null | head -1)"
  else
    warn "git not found. Total Recall will not be available."
  fi
fi

if command -v bun &>/dev/null; then
  ok "bun: v$(bun --version 2>/dev/null)"
  BUN_READY=true
elif [ -x "$HOME/.bun/bin/bun" ]; then
  export PATH="$HOME/.bun/bin:$PATH"
  ok "bun: v$(bun --version 2>/dev/null) (found at \$HOME/.bun/bin)"
  BUN_READY=true
else
  warn "bun not found — will attempt to install in Step 3."
fi

command -v python3 &>/dev/null && ok "python3: $(python3 --version 2>/dev/null)" || warn "python3 not found."

install_bun() {
  # Check if bun is already in PATH or at known location
  if command -v bun &>/dev/null; then
    ok "bun: v$(bun --version 2>/dev/null)"
    return 0
  fi
  # Bun may be installed but not in PATH (common on WSL after fresh install)
  if [ -x "$HOME/.bun/bin/bun" ]; then
    export BUN_INSTALL="$HOME/.bun"
    export PATH="$BUN_INSTALL/bin:$PATH"
    ok "bun: v$(bun --version 2>/dev/null) (added to PATH)"
  else
    info "Installing Bun..."
    curl -fsSL https://bun.sh/install | bash 2>/dev/null
    export BUN_INSTALL="$HOME/.bun"
    export PATH="$BUN_INSTALL/bin:$PATH"
    ok "bun: v$(bun --version 2>/dev/null)"
  fi
  # Persist bun PATH in shell profile
  local shell_profile=""
  if [ -f "$HOME/.bashrc" ]; then shell_profile="$HOME/.bashrc"
  elif [ -f "$HOME/.zshrc" ]; then shell_profile="$HOME/.zshrc"
  fi
  if [ -n "$shell_profile" ] && ! grep -q '\.bun/bin' "$shell_profile" 2>/dev/null; then
    echo 'export PATH="$HOME/.bun/bin:$PATH"' >> "$shell_profile"
    ok "Added bun to $shell_profile"
  fi
}

install_uv() {
  if command -v uv &>/dev/null; then
    ok "uv: $(uv --version 2>/dev/null)"
    return 0
  fi
  info "Installing uv (Python manager)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null
  export PATH="$HOME/.local/bin:$PATH"
  ok "uv: $(uv --version 2>/dev/null)"
}

setup_python_venv() {
  local venv_dir="$HOME/.openclaw/venv"
  # Windows venvs use Scripts/pip.exe; Unix venvs use bin/pip
  if [ -f "$venv_dir/bin/pip" ] || [ -f "$venv_dir/Scripts/pip.exe" ]; then
    ok "Python venv: $venv_dir (exists)"
    return 0
  fi
  # On Debian/Ubuntu, python3-venv may not be installed
  if ! python3 -c "import ensurepip" 2>/dev/null; then
    info "Installing python3-venv (required for backend dependencies)..."
    if command -v apt-get &>/dev/null; then
      sudo apt-get install -y python3-venv --quiet 2>/dev/null || true
    fi
  fi
  info "Creating Python venv..."
  rm -rf "$venv_dir"
  uv venv "$venv_dir" --python 3.12 --seed 2>/dev/null || python3 -m venv "$venv_dir" 2>/dev/null
  if [ ! -f "$venv_dir/bin/pip" ] && [ ! -f "$venv_dir/Scripts/pip.exe" ]; then
    warn "Python venv created but pip missing — some backends may be unavailable"
    return 0
  fi
  ok "Python venv: $venv_dir"
}

# ── Step 4: Install files ──────────────────────────────────────────
header "Step 2/5 — Installing files"

mkdir -p "$INSTALL_ROOT" "$STATE_DIR" "$BIN_DIR"

# Copy bin/, lib/, and install.sh itself (needed by `openclaw-memory upgrade`)
cp -r "$SCRIPT_DIR/bin" "$INSTALL_ROOT/"
cp -r "$SCRIPT_DIR/lib" "$INSTALL_ROOT/"
cp "$SCRIPT_DIR/install.sh" "$INSTALL_ROOT/"

# Copy all backend skills dynamically
mkdir -p "$INSTALL_ROOT/skills"
for skill_dir in "$SCRIPT_DIR/skills/memory-"*; do
  [[ -d "$skill_dir" ]] || continue
  skill_name=$(basename "$skill_dir")
  rm -rf "$INSTALL_ROOT/skills/$skill_name"
  cp -r "$skill_dir" "$INSTALL_ROOT/skills/"
done

# Make CLI executable
chmod +x "$INSTALL_ROOT/bin/openclaw-memory"
chmod +x "$INSTALL_ROOT/bin/openclaw-memory-qmd"

ok "Files installed to $INSTALL_ROOT"

# ── Step 3/5 — Installing backend dependencies ─────────────────────
header "Step 3/5 — Installing backend dependencies"

# Bootstrap Python venv + ensure PATH includes openclaw bins
install_uv
setup_python_venv

# Bootstrap bun if missing — qmd's install_hint depends on it.
if ! $BUN_READY; then
  install_bun || true
  if command -v bun &>/dev/null; then
    BUN_READY=true
  else
    warn "bun install failed — qmd backend will be skipped"
    warn "  retry manually: curl -fsSL https://bun.sh/install | bash"
  fi
fi

export PATH="$BIN_DIR:$INSTALL_ROOT/bin:$PATH"

for skill_dir in "$INSTALL_ROOT/skills/memory-"*; do
  [[ -f "$skill_dir/capability.json" ]] || continue
  bname=$(basename "$skill_dir" | sed 's/memory-//')
  [[ "$bname" == "router" ]] && continue

  # Skip optional backends
  is_optional=$(python3 -c "import json; d=json.load(open('$skill_dir/capability.json')); print(d.get('optional', False))" 2>/dev/null || echo "False")
  [[ "$is_optional" == "True" ]] && { info "Skipping $bname (optional — install manually)"; continue; }

  install_hint=$(python3 -c "import json; print(json.load(open('$skill_dir/capability.json'))['install_hint'])" 2>/dev/null || echo "")
  [[ -z "$install_hint" ]] && continue

  info "Installing $bname..."
  if bash -c "$install_hint" 2>&1 | tail -3; then
    ok "$bname installed"
  else
    warn "$bname: install failed (non-fatal)"
    warn "  hint: $install_hint"
  fi
done

if ! $SKIP_MODELS && command -v qmd &>/dev/null; then
  info "Downloading QMD models (~2.1GB)..."
  qmd embed --download-models 2>/dev/null && ok "QMD models downloaded" || warn "Model download failed (retry: qmd embed --download-models)"
fi

# ── Step 5: Create symlink ─────────────────────────────────────────
header "Step 4/5 — Setting up PATH"

ln -sf "$INSTALL_ROOT/bin/openclaw-memory" "$BIN_DIR/openclaw-memory"
ln -sf "$INSTALL_ROOT/bin/openclaw-memory-qmd" "$BIN_DIR/openclaw-memory-qmd"
ok "Symlinked: $BIN_DIR/openclaw-memory"
ok "Symlinked: $BIN_DIR/openclaw-memory-qmd (OpenClaw qmd-compat shim)"

# Check if ~/.openclaw/bin is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
  warn "$BIN_DIR is not in your PATH."
  echo ""
  echo "  Add to your shell profile (~/.zshrc or ~/.bashrc):"
  echo "    export PATH=\"$BIN_DIR:\$PATH\""
  echo ""
fi

# ── Step 6: Write state files ──────────────────────────────────────
header "Step 5/5 — Writing configuration"

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
VERSION=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/version.json'))['version'])" 2>/dev/null || echo "0.0.0")

# version.json
cat > "$INSTALL_ROOT/version.json" <<JSONEOF
{
  "version": "$VERSION",
  "installed_at": "$NOW"
}
JSONEOF
ok "version.json"

# backends.json — dynamic discovery from installed wrappers
_gen_backends() {
  echo '{'
  echo '  "version": "2.0",'
  echo "  \"installed_at\": \"$NOW\","
  echo '  "backends": {'
  local first=true bname bstatus
  for skill_dir in "$INSTALL_ROOT/skills/memory-"*; do
    [[ -f "$skill_dir/wrapper.sh" ]] || continue
    bname=$(basename "$skill_dir" | sed 's/memory-//')
    [[ "$bname" == "router" ]] && continue
    bstatus="installed"
    if bash "$skill_dir/wrapper.sh" health &>/dev/null; then
      bstatus=$(OPENCLAW_INSTALL_ROOT="$INSTALL_ROOT" bash "$skill_dir/wrapper.sh" health 2>/dev/null \
        | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','installed'))" 2>/dev/null || echo "installed")
    fi
    $first || echo ','
    printf '    "%s": { "status": "%s" }' "$bname" "$bstatus"
    first=false
  done
  echo ''
  echo '  }'
  echo '}'
}
_gen_backends > "$STATE_DIR/backends.json"
ok "backends.json"

# ── Step 5b/5 — Register as OpenClaw memory plugin ──────────────────
header "Step 6b/6 — Connecting to OpenClaw"

# Copy plugin to OpenClaw extensions directory (same structure as npm-installed plugins)
OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"
EXT_DIR="$HOME/.openclaw/extensions/openclaw-memory-stack"

if [[ -f "$OPENCLAW_JSON" ]] && command -v python3 &>/dev/null; then
  # 1. Install plugin files to extensions dir
  mkdir -p "$EXT_DIR"
  # Copy bundled plugin (minified)
  if [[ -f "$SCRIPT_DIR/plugin/dist/index.mjs" ]]; then
    mkdir -p "$EXT_DIR/dist"
    cp "$SCRIPT_DIR/plugin/dist/index.mjs" "$EXT_DIR/dist/"
    # External modules are resolved relative to dist/index.mjs via two paths:
    #   ./lib/llm.mjs  → $EXT_DIR/dist/lib/llm.mjs
    #   ../lib/llm.mjs → $EXT_DIR/lib/llm.mjs
    # Both must exist for the bundled plugin to load.
    if [[ -d "$SCRIPT_DIR/plugin/lib" ]]; then
      rm -rf "$EXT_DIR/dist/lib" "$EXT_DIR/lib"
      cp -R "$SCRIPT_DIR/plugin/lib" "$EXT_DIR/dist/lib"
      cp -R "$SCRIPT_DIR/plugin/lib" "$EXT_DIR/lib"
    fi
  else
    cp "$SCRIPT_DIR/plugin/index.mjs" "$EXT_DIR/"
  fi
  cp "$SCRIPT_DIR/plugin/package.json" "$EXT_DIR/"
  if [[ -f "$SCRIPT_DIR/plugin/openclaw.plugin.json" ]]; then
    cp "$SCRIPT_DIR/plugin/openclaw.plugin.json" "$EXT_DIR/"
  elif [[ -f "$SCRIPT_DIR/openclaw.plugin.json" ]]; then
    cp "$SCRIPT_DIR/openclaw.plugin.json" "$EXT_DIR/"
  fi
  # lib/ modules are mirrored into dist/lib/ (above) — no separate copy needed
  ok "Plugin files → $EXT_DIR"

  # 2. Register in openclaw.json (matching native openclaw plugins install format)
  python3 -c "
import json, datetime

config_path = '$OPENCLAW_JSON'
ext_dir = '$EXT_DIR'

with open(config_path) as f:
    config = json.load(f)

plugins = config.setdefault('plugins', {})

# allow list
allow = plugins.setdefault('allow', [])
if 'openclaw-memory-stack' not in allow:
    allow.append('openclaw-memory-stack')

# slots — register as memory provider
slots = plugins.setdefault('slots', {})
slots['memory'] = 'openclaw-memory-stack'

# entries — plugin config
entries = plugins.setdefault('entries', {})
entries['openclaw-memory-stack'] = {
    'enabled': True,
    'config': {
        'routerMode': 'auto',
        'searchMode': 'hybrid',
        'autoRecall': True,
        'autoCapture': True,
        'maxRecallResults': 5,
        'maxRecallTokens': 1500
    }
}

# Configure OpenClaw to use memory-stack as the qmd backend
memory_cfg = config.setdefault('memory', {})
memory_cfg['backend'] = 'qmd'
qmd_cfg = memory_cfg.setdefault('qmd', {})
qmd_cfg['command'] = 'openclaw-memory-qmd'
qmd_cfg.setdefault('searchMode', 'query')
qmd_cfg.setdefault('includeDefaultMemory', True)

# installs — required by OpenClaw plugin validator
installs = plugins.setdefault('installs', {})
now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
pkg_version = '0.1.3'
try:
    import os
    pkg_json = os.path.join('$SCRIPT_DIR', 'plugin', 'package.json')
    with open(pkg_json) as pf:
        pkg_version = json.load(pf).get('version', pkg_version)
except:
    pass
installs['openclaw-memory-stack'] = {
    'source': 'path',
    'spec': ext_dir,
    'installPath': ext_dir,
    'version': pkg_version,
    'resolvedName': 'openclaw-memory-stack',
    'resolvedVersion': pkg_version,
    'resolvedSpec': f'openclaw-memory-stack@{pkg_version}',
    'installedAt': now
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
" 2>/dev/null && ok "Registered as OpenClaw memory plugin" || warn "Could not update openclaw.json (configure manually)"
else
  if [[ ! -f "$OPENCLAW_JSON" ]]; then
    warn "openclaw.json not found — is OpenClaw installed?"
  else
    warn "python3 not found — please register manually"
  fi
  echo "  Run: openclaw plugins install $EXT_DIR" >&2
fi

# ── Summary ─────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}=========================================${NC}"
echo -e "${BOLD}  Installation Complete${NC}"
echo -e "${BOLD}=========================================${NC}"
echo ""
echo -e "  Install path: ${BOLD}${INSTALL_ROOT}${NC}"
echo -e "  License:      ${GREEN}activated${NC}"
echo -e "  OpenClaw:     ${GREEN}memory plugin registered${NC}"
echo ""
echo "  Backends:"
for skill_dir in "$INSTALL_ROOT/skills/memory-"*; do
  [[ -f "$skill_dir/wrapper.sh" ]] || continue
  bname=$(basename "$skill_dir" | sed 's/memory-//')
  [[ "$bname" == "router" ]] && continue
  bstatus=$(python3 -c "import json; d=json.load(open('$STATE_DIR/backends.json')); print(d['backends'].get('$bname',{}).get('status','unknown'))" 2>/dev/null || echo "unknown")
  case "$bstatus" in
    ready)    echo -e "    $bname: ${GREEN}$bstatus${NC}" ;;
    degraded) echo -e "    $bname: ${YELLOW}$bstatus${NC}" ;;
    *)        echo -e "    $bname: ${YELLOW}$bstatus${NC}" ;;
  esac
done

echo ""
echo -e "  ${GREEN}Memory Stack is now active.${NC}"

# Auto-restart OpenClaw gateway
if command -v openclaw &>/dev/null; then
  echo -e "  Restarting OpenClaw gateway..."
  openclaw gateway restart 2>/dev/null &
  disown
  echo -e "  ${GREEN}OpenClaw gateway restarting.${NC}"
else
  echo -e "  ${YELLOW}OpenClaw not found — start it manually when ready.${NC}"
fi
echo ""
