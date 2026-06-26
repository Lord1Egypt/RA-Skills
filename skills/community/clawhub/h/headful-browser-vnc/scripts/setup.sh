SKILL_DIR=/
#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Configuration & Globals
# ==============================================================================
CHECK_ONLY=false
ASSUME_YES=false
SET_PASSWORD_ONLY=false

# Resolve ENV_FILE path (skill-local preferred, fallback to parent)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
  ENV_FILE="$(dirname "$SCRIPT_DIR")/.env"
fi

# Detect containerized environment (Docker / containerd) and set package-prefix accordingly
IS_CONTAINER=false
PKG_PREFIX="sudo "
# Detect common container indicators
if [ -f "/.dockerenv" ] || (grep -qaE "docker|containerd|kubepods" /proc/1/cgroup 2>/dev/null); then
  IS_CONTAINER=true
  PKG_PREFIX=""
fi
if [ "${IS_CONTAINER}" = true ]; then
echo "Detected containerized environment: package-manager commands will run without sudo by default" >&2
else
echo "Detected host environment: package-manager commands will use sudo when needed" >&2
fi

# ==============================================================================
# Helper Functions
# ==============================================================================

log() { echo "$*" >&2; }

ask_confirm() {
  local prompt="$1"
  if [ "$ASSUME_YES" = true ]; then return 0; fi
  read -r -p "$prompt (y/N) " yn
  [[ "$yn" = "y" || "$yn" = "Y" ]]
}

has_cmd() { command -v "$1" >/dev/null 2>&1; }

update_env_var() {
  local key="$1"; local value="$2"
  if [ ! -f "$ENV_FILE" ]; then
    mkdir -p "$(dirname "$ENV_FILE")" || true
    : > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
  fi
  if grep -q "^${key}=" "$ENV_FILE"; then
    sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
    log "Updated $key=$value in $ENV_FILE"
  else
    echo "${key}=${value}" >> "$ENV_FILE"
    log "Added $key=$value to $ENV_FILE"
  fi
  chmod 600 "$ENV_FILE"
}

load_env() {
  if [ -f "$ENV_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$ENV_FILE"
    set +a
  fi
}

# Check if file is a binary rfbauth
is_rfbauth() {
  [ ! -f "$1" ] && return 1
  file "$1" 2>/dev/null | grep -qi 'byte\|data\|encrypted\|binary'
}

# Check if VNC_PASSFILE is configured AND valid
is_valid_passfile() {
  load_env
  local pf="${VNC_PASSFILE:-}"
  [ -z "$pf" ] && return 1
  [ ! -f "$pf" ] && return 1
  is_rfbauth "$pf" || return 1
  return 0
}

# ==============================================================================
# Distro-specific install guidance (no automatic privileged installs)
# ==============================================================================
print_install_hints() {
  cat <<'EOF'

Platform install hints (guidance-only — these commands will NOT be run automatically):

Debian / Ubuntu (apt):
  apt-get update
  apt-get install -y --no-install-recommends \
    xvfb x11vnc fluxbox x11-utils tigervnc-standalone-server tightvnc-tools \
    fonts-noto-cjk fontconfig chromium-browser google-chrome-stable \
    nodejs npm python3-pip

RHEL / CentOS / Alma (dnf/yum):
  # enable EPEL if needed
  dnf install -y epel-release || yum install -y epel-release
  dnf install -y Xvfb x11vnc fluxbox xorg-x11-utils tigervnc-server tigervnc-server-module \
    fontconfig freetype

Arch Linux (pacman):
  pacman -Syu --noconfirm xorg-server-xvfb x11vnc fluxbox xorg-x11-utils \
    chromium nodejs npm python-pip noto-fonts-cjk

Notes:
- Package names vary by distro and release; adapt the commands accordingly.
- Prefer google-chrome-stable (.deb) on Debian/Ubuntu for automation (non-snap). In container images prefer adding it in the Dockerfile.
- Prefer vncpasswd (from tightvnc-tools / tigervnc) to generate rfbauth non-interactively.
- These are guidance commands only; the installer will present them and ask before running privileged commands.
EOF
}

# ==============================================================================
# Core Logic Functions
# ==============================================================================

resolve_passfile() {
  load_env
  local current_pf="${VNC_PASSFILE:-}"
  local default_pf user_input final_pf
  if [ -n "$current_pf" ]; then
    default_pf="$current_pf"
    log "Found existing VNC_PASSFILE in .env: $default_pf"
  else
    default_pf="$(pwd)/vnc_passwd"
    log "No VNC_PASSFILE in .env. Defaulting to: $default_pf"
  fi

  echo -n "Enter VNC passfile path [$default_pf]: " >&2
  read -r user_input
  final_pf="${user_input:-$default_pf}"
  log "Using passfile: $final_pf"

  if ! mkdir -p "$(dirname "$final_pf")" 2>/dev/null; then
    log "Error: Cannot create directory for $final_pf"
    return 1
  fi

  if [ -z "$current_pf" ] || [ "$current_pf" != "$final_pf" ]; then
    update_env_var "VNC_PASSFILE" "$final_pf"
  fi

  echo "$final_pf"
}

generate_passfile_auto() {
  local PF="$1"
  local PW PW_CONFIRM

  if [[ "$PF" == *$'\n'* ]]; then
    log "Error: Invalid passfile path (contains newlines)."
    return 1
  fi

  # Strategy 1: vncpasswd
  if has_cmd vncpasswd; then
    log "Tool 'vncpasswd' found. Preparing automated generation..."
    echo -n "Enter VNC password (hidden): " >&2
    read -r -s PW || { log "Error reading password."; return 1; }
    echo >&2
    echo -n "Confirm password: " >&2
    read -r -s PW_CONFIRM || { log "Error reading confirmation."; return 1; }
    echo >&2
    if [ "$PW" != "$PW_CONFIRM" ] || [ -z "$PW" ]; then
      log "Passwords mismatch or empty. Aborting."
      return 1
    fi
    log "Generating rfbauth via vncpasswd..."
    printf '%s\n%s\n' "$PW" "$PW" | vncpasswd -f > "$PF" 2>/dev/null || true
    if is_rfbauth "$PF"; then
      chmod 600 "$PF"; log "SUCCESS: rfbauth generated at $PF"; return 0
    else
      log "vncpasswd did not produce expected rfbauth; cleaning up and trying other methods."
      rm -f "$PF" || true
    fi
  fi



  return 1
}

run_interactive_store() {
  local PF="$1"
  log "Running: x11vnc -storepasswd $PF"
  if x11vnc -storepasswd "$PF"; then
    if is_rfbauth "$PF"; then
      chmod 600 "$PF"; log "SUCCESS: rfbauth created interactively at $PF"; return 0
    else
      log "Interactive run completed but validation failed."
    fi
  else
    log "Interactive run failed or cancelled."
  fi
  return 1
}

# ==============================================================================
# Main Workflows
# ==============================================================================

run_password_only() {
  log "Running VNC password-only setup..."
  local PF
  PF=$(resolve_passfile) || exit 1
  if generate_passfile_auto "$PF"; then exit 0; fi
  run_interactive_store "$PF" && exit 0
  log "Password setup cancelled."; exit 4
}

run_check_only() {
  local missing=()
  has_cmd Xvfb || missing+=("Xvfb")
  has_cmd x11vnc || missing+=("x11vnc")
  if has_cmd google-chrome || has_cmd chromium-browser; then :; else missing+=("chrome"); fi

  if has_cmd node; then
    local ver=$(node -v | sed 's/^v//')
    local major=${ver%%.*}
    if [ "$major" -lt 22 ]; then missing+=("node(v$ver<22)"); fi
  elif [ -s "$HOME/.nvm/nvm.sh" ]; then
    . "$HOME/.nvm/nvm.sh"
    if has_cmd node; then
      local ver=$(node -v | sed 's/^v//')
      local major=${ver%%.*}
      if [ "$major" -lt 22 ]; then missing+=("node(v$ver<22)"); fi
    else
      missing+=("node")
    fi
  else
    missing+=("node")
  fi

  if ! is_valid_passfile; then
    load_env
    if [ -z "${VNC_PASSFILE:-}" ]; then
      missing+=("VNC_PASSFILE(not_set)")
    elif [ ! -f "${VNC_PASSFILE}" ]; then
      missing+=("VNC_PASSFILE(file_missing:${VNC_PASSFILE})")
    else
      missing+=("VNC_PASSFILE(invalid_format)")
    fi
  fi

  if [ ${#missing[@]} -ne 0 ]; then
    log "Missing requirements: ${missing[*]}"; exit 2
  fi
  log "All checks passed."; exit 0
}

run_installer() {
  log "Starting interactive installation..."

  # Detect distro
  local os_id="unknown"
  if [ -f /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release 2>/dev/null || true
    os_id="${ID:-unknown}"
  fi
  os_id="${os_id,,}"

  # Build distro-specific install commands (strings only; will not run unless explicitly confirmed).
  local cmd_xvfb cmd_x11vnc cmd_chrome cmd_node
  case "${os_id}" in
    ubuntu|debian)
      cmd_xvfb="${PKG_PREFIX}apt-get update && ${PKG_PREFIX}apt-get install -y xvfb"
      cmd_x11vnc="${PKG_PREFIX}apt-get install -y x11vnc"
      cmd_chrome="wget -q -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && ${PKG_PREFIX}apt-get install -y /tmp/google-chrome.deb || true"
      cmd_node="curl -fsSL https://deb.nodesource.com/setup_22.x | ${PKG_PREFIX}-E bash - && ${PKG_PREFIX}apt-get install -y nodejs"
      ;;
    rhel|centos|almalinux|rocky|fedora)
      cmd_xvfb="${PKG_PREFIX}dnf install -y xorg-x11-server-Xvfb || ${PKG_PREFIX}yum install -y xorg-x11-server-Xvfb"
      cmd_x11vnc="${PKG_PREFIX}dnf install -y x11vnc || ${PKG_PREFIX}yum install -y x11vnc"
      cmd_chrome="echo 'Install Google Chrome RPM via vendor package (manual step)'"
      cmd_node="echo 'Use Nodesource or dnf module for Node.js >=22 (manual)'
      "
      ;;
    arch)
      cmd_xvfb="${PKG_PREFIX}pacman -Syu --noconfirm xorg-server-xvfb"
      cmd_x11vnc="${PKG_PREFIX}pacman -S --noconfirm x11vnc"
      cmd_chrome="${PKG_PREFIX}pacman -S --noconfirm chromium || true"
      cmd_node="${PKG_PREFIX}pacman -S --noconfirm nodejs npm"
      ;;
    alpine)
      cmd_xvfb="${PKG_PREFIX}apk add --no-cache xvfb"
      cmd_x11vnc="${PKG_PREFIX}apk add --no-cache x11vnc"
      cmd_chrome="echo 'Google Chrome not available on Alpine; consider using chromium from community'"
      cmd_node="${PKG_PREFIX}apk add --no-cache nodejs npm"
      ;;
    *)
      cmd_xvfb="echo 'Install Xvfb via your distro package manager'"
      cmd_x11vnc="echo 'Install x11vnc via your distro package manager'"
      cmd_chrome="echo 'Install Google Chrome or Chromium manually'"
      cmd_node="echo 'Install Node.js v22+ manually'"
      ;;
  esac

  # Determine missing components
  local missing=()
  has_cmd Xvfb || missing+=("Xvfb")
  has_cmd x11vnc || missing+=("x11vnc")
  if has_cmd google-chrome || has_cmd chromium-browser || has_cmd chromium; then :; else missing+=("chrome"); fi
  if ! has_cmd node; then
    if [ -s "$HOME/.nvm/nvm.sh" ]; then
      . "$HOME/.nvm/nvm.sh"
      has_cmd node || missing+=("node")
    else
      missing+=("node")
    fi
  fi
  if ! is_valid_passfile; then missing+=("VNC_PASSFILE"); fi
  if [ ! -f "$ENV_FILE" ]; then missing+=(".env"); fi

  if [ ${#missing[@]} -eq 0 ]; then log "All components already present."; return 0; fi

  print_install_hints

  for comp in "${missing[@]}"; do
    log "--- Handling missing: $comp ---"
    case "$comp" in
      Xvfb)
        log "Suggested command: $cmd_xvfb"
        if ask_confirm "Run the above command to install Xvfb?"; then
          printf "About to run:\n%s\n" "$cmd_xvfb"
          read -r -p "Type the exact word 'yes' to proceed: " CONFIRM
          if [ "$CONFIRM" = "yes" ] && [ "${AUTO_INSTALL:-false}" = "true" ]; then
            eval "$cmd_xvfb" || log "Command returned non-zero status"
          else
            log "Skipped automatic install. Please run the printed command manually."
            read -r -p "Press Enter when done..." _ || true
          fi
        fi
        ;;
      x11vnc)
        log "Suggested command: $cmd_x11vnc"
        if ask_confirm "Run the above command to install x11vnc?"; then
          printf "About to run:\n%s\n" "$cmd_x11vnc"
          read -r -p "Type the exact word 'yes' to proceed: " CONFIRM
          if [ "$CONFIRM" = "yes" ] && [ "${AUTO_INSTALL:-false}" = "true" ]; then
            eval "$cmd_x11vnc" || log "Command returned non-zero status"
          else
            log "Skipped automatic install. Please run the printed command manually."
          fi
        fi
        # After possible install attempt, set VNC port/env and password
        local def_port=${VNC_PORT:-5901}
        read -r -p "VNC Port [$def_port]: " port_input
        local final_port=${port_input:-$def_port}
        update_env_var "VNC_PORT" "$final_port"
        local PF
        PF=$(resolve_passfile) || { log "Skipping password setup due to path error."; continue; }
        if ! generate_passfile_auto "$PF"; then
          if ask_confirm "Run interactive 'x11vnc -storepasswd'?"; then run_interactive_store "$PF"; fi
        fi
        ;;
      chrome)
        log "Suggested command: $cmd_chrome"
        if ask_confirm "Install Chrome/Chromium using suggested command?"; then
          printf "About to run:\n%s\n" "$cmd_chrome"
          read -r -p "Type the exact word 'yes' to proceed: " CONFIRM
          if [ "$CONFIRM" = "yes" ] && [ "${AUTO_INSTALL:-false}" = "true" ]; then
            eval "$cmd_chrome" || log "Command returned non-zero status"
          else
            log "Skipped automatic install. Please run the printed command manually."
          fi
        fi
        ;;
      node)
        log "Suggested command: $cmd_node"
        if ask_confirm "Install Node.js v22+ using suggested command?"; then
          printf "About to run:\n%s\n" "$cmd_node"
          read -r -p "Type the exact word 'yes' to proceed: " CONFIRM
          if [ "$CONFIRM" = "yes" ] && [ "${AUTO_INSTALL:-false}" = "true" ]; then
            eval "$cmd_node" || log "Command returned non-zero status"
          else
            log "Skipped automatic install. Please run the printed command manually."
          fi
        fi
        ;;
      .env)
        if ask_confirm "Create template .env?"; then
          cat > "$ENV_FILE" <<EOF
VNC_DISPLAY=:99
VNC_RESOLUTION=1366x768
VNC_PORT=5901
VNC_PASSFILE=
VNC_USER=user
CHROME_USER_DATA_DIR=/tmp/chrome_profile_for_vnc
REMOTE_DEBUG_PORT=9222
NOVNC_ENABLED=false
EOF
          chmod 600 "$ENV_FILE"
          log "Created $ENV_FILE"
        fi
        ;;
      VNC_PASSFILE)
        log "VNC Passfile is missing or invalid."; log "Setting up VNC authentication (binary passfile) now..."
        local PF
        PF=$(resolve_passfile) || { log "Failed to determine passfile path. Skipping."; continue; }
        local success=false
        if generate_passfile_auto "$PF"; then success=true
        elif ask_confirm "Automated generation failed. Run interactive mode?"; then run_interactive_store "$PF" && success=true; fi
        if [ "$success" = true ]; then log "VNC Passfile setup complete."; else log "VNC Passfile setup skipped or failed."; fi
        ;;
    esac
  done

  log "Installation flow complete."
}


show_help() {
  cat <<'HELP'
Usage: bash [options]

Options:
  --check-only       Run non-destructive checks for required tools and config
  --yes              Assume yes for confirmation prompts (non-destructive only)
  --set-password     Run only the VNC password setup flow (interactive)
  --auto-install     Allow the installer to execute distro package manager commands (requires typing 'yes' at prompt)
  --help             Show this help text

Examples:
  # Run checks only (no installs)
  ./skills/headful-browser-vnc/scripts/setup.sh --check-only

  # Interactively set up a VNC password only
  ./skills/headful-browser-vnc/scripts/setup.sh --set-password

  # Print distro-specific install hints (manual mode)
  ./skills/headful-browser-vnc/scripts/setup.sh

  # Allow the script to execute package-manager commands (requires typing exact 'yes' when prompted)
  AUTO_INSTALL=true ./skills/headful-browser-vnc/scripts/setup.sh --auto-install

Safety:
  The installer will NOT run privileged package manager commands unless both --auto-install is provided and you explicitly type the full word 'yes' when prompted. By default the script only prints distro-appropriate install commands for manual execution.
HELP
}


# ==============================================================================
# Entry Point
# ==============================================================================
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=true ;;
    --yes) ASSUME_YES=true ;;
    --set-password) SET_PASSWORD_ONLY=true ;;
    --auto-install) AUTO_INSTALL=true ;;
    --help) show_help; exit 0 ;;
  esac
done

if [ "$SET_PASSWORD_ONLY" = true ]; then
  run_password_only
elif [ "$CHECK_ONLY" = true ]; then
  run_check_only
else
  run_installer
fi

exit 0
