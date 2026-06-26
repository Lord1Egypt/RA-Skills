#!/usr/bin/env bash
set -euo pipefail

# Muster Server Install Script
# Installs the Muster server on this machine. Run ONCE per machine.
# After this completes, run connect.sh to connect an agent.
#
# Usage: bash install.sh [--port PORT] [--install-dir DIR] [--skip-connect]
#        [--service-mode launchd|pm2]  (macOS default: launchd, Linux: pm2)
#        [--db-mode homebrew|docker]   (macOS default: homebrew, Linux: docker)
#
# By default, runs connect.sh at the end to connect the installing agent.
# Use --skip-connect to install the server only.
#
# Outputs JSON report to stdout. Progress to stderr.

# --- Defaults ---
MUSTER_PORT="${MUSTER_PORT:-3000}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/muster}"
SKIP_CONNECT=false
SERVICE_MODE=""
DB_MODE=""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Parse args ---
CONNECT_ARGS=()
while [[ $# -gt 0 ]]; do
  case $1 in
    --port) MUSTER_PORT="$2"; shift 2 ;;
    --install-dir) INSTALL_DIR="$2"; shift 2 ;;
    --skip-connect) SKIP_CONNECT=true; shift ;;
    --service-mode) SERVICE_MODE="$2"; shift 2 ;;
    --db-mode) DB_MODE="$2"; shift 2 ;;
    --name|--title|--slug|--webhook|--workspace)
      CONNECT_ARGS+=("$1" "$2"); shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Helpers ---
log() { echo "[muster-install] $*" >&2; }
fail() { echo "[muster-install] FAILED: $*" >&2; exit 1; }

command_exists() { command -v "$1" &>/dev/null; }

detect_os() {
  case "$(uname -s)" in
    Darwin) echo "macos" ;;
    Linux)  echo "linux" ;;
    *)      fail "Unsupported OS: $(uname -s)" ;;
  esac
}

generate_password() {
  LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 24 || true
}

wait_for_healthy() {
  local url="$1" max_attempts="${2:-30}" attempt=0
  while [ $attempt -lt $max_attempts ]; do
    if curl -sf "$url" &>/dev/null; then return 0; fi
    sleep 2; attempt=$((attempt + 1))
  done
  return 1
}

find_available_port() {
  local port="$1" max=10 i=0
  while [ $i -lt $max ]; do
    if ! lsof -i :"$port" &>/dev/null 2>&1; then echo "$port"; return 0; fi
    log "Port $port in use, trying $((port + 1))..."
    port=$((port + 1)); i=$((i + 1))
  done
  fail "No available port found (tried $1–$port)"
}

OS=$(detect_os)
log "Detected OS: $OS"

# Set defaults based on OS
[ -z "$SERVICE_MODE" ] && { [ "$OS" = "macos" ] && SERVICE_MODE="launchd" || SERVICE_MODE="pm2"; }
[ -z "$DB_MODE" ] && { [ "$OS" = "macos" ] && DB_MODE="homebrew" || DB_MODE="docker"; }

log "Service mode: $SERVICE_MODE"
log "Database mode: $DB_MODE"

# ============================================================
# Phase 1: Port check
# ============================================================
log "Phase 1: Checking port availability..."
MUSTER_PORT=$(find_available_port "$MUSTER_PORT")
log "✓ Using port $MUSTER_PORT"

# ============================================================
# Phase 2: Dependencies
# ============================================================
log "Phase 2: Checking dependencies..."

if ! command_exists git; then
  log "Installing git..."
  if [ "$OS" = "macos" ]; then xcode-select --install 2>/dev/null || true
  else sudo apt-get update -qq && sudo apt-get install -y -qq git; fi
fi
log "✓ git $(git --version | awk '{print $3}')"

if ! command_exists node || [ "$(node -e 'console.log(parseInt(process.versions.node))')" -lt 20 ]; then
  log "Installing Node.js ≥ 20..."
  if [ "$OS" = "macos" ]; then brew install node@20
  else curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y -qq nodejs; fi
fi
log "✓ node $(node --version)"

# Database dependencies
if [ "$DB_MODE" = "homebrew" ]; then
  if ! command_exists psql; then
    log "Installing PostgreSQL via Homebrew..."
    brew install postgresql@16
  fi
  log "✓ PostgreSQL $(psql --version | awk '{print $3}')"
elif [ "$DB_MODE" = "docker" ]; then
  if ! command_exists docker; then
    log "Installing Docker..."
    if [ "$OS" = "macos" ]; then
      brew install --cask docker; open -a Docker
      log "⚠ Docker Desktop is opening. Accept the license agreement to continue."
      while ! docker info &>/dev/null; do sleep 5; done
    else
      curl -fsSL https://get.docker.com | sh
      sudo usermod -aG docker "$USER" 2>/dev/null || true
    fi
  fi
  log "✓ docker $(docker --version | awk '{print $3}' | tr -d ',')"
fi

# Service manager dependencies
if [ "$SERVICE_MODE" = "pm2" ]; then
  if ! command_exists pm2; then log "Installing pm2..."; npm install -g pm2; fi
  log "✓ pm2 $(pm2 --version)"
fi

if ! command_exists cloudflared; then
  log "Installing cloudflared..."
  if [ "$OS" = "macos" ]; then brew install cloudflare/cloudflare/cloudflared
  else
    curl -fsSL -o /tmp/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared; rm -f /tmp/cloudflared
  fi
fi
log "✓ cloudflared $(cloudflared --version 2>&1 | awk '{print $3}')"

# ============================================================
# Phase 3: Clone and install
# ============================================================
log "Phase 3: Installing Muster..."
if [ -d "$INSTALL_DIR" ]; then
  log "$INSTALL_DIR exists — pulling latest..."; cd "$INSTALL_DIR"; git pull origin main
else
  git clone https://github.com/AirborneEagle/muster.git "$INSTALL_DIR"; cd "$INSTALL_DIR"
fi
npm install --silent
log "✓ Dependencies installed"

# ============================================================
# Phase 4: Environment file
# ============================================================
log "Phase 4: Configuring environment..."
ENV_FILE="$INSTALL_DIR/.env"

if [ "$DB_MODE" = "homebrew" ]; then
  MUSTER_DB_URL="postgresql://$(whoami)@localhost:5432/muster"
else
  MUSTER_DB_URL="postgresql://muster:muster@localhost:5432/muster"
fi

if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" << EOF
MUSTER_DB_URL=${MUSTER_DB_URL}
PORT=${MUSTER_PORT}
EOF
  log "✓ Created .env"
else
  grep -q "^MUSTER_DB_URL=" "$ENV_FILE" || echo "MUSTER_DB_URL=${MUSTER_DB_URL}" >> "$ENV_FILE"
  if grep -q "^PORT=" "$ENV_FILE"; then
    sed -i.bak "s/^PORT=.*/PORT=${MUSTER_PORT}/" "$ENV_FILE" && rm -f "${ENV_FILE}.bak"
  else
    echo "PORT=${MUSTER_PORT}" >> "$ENV_FILE"
  fi
  log "✓ .env verified"
fi

# ============================================================
# Phase 5: Database
# ============================================================
log "Phase 5: Starting database..."

if [ "$DB_MODE" = "homebrew" ]; then
  # Start postgres via Homebrew services (launchd-managed)
  if ! brew services list | grep -q "postgresql.*started"; then
    brew services start postgresql@16
    sleep 3
  fi
  # Wait for postgres to be ready
  ATTEMPTS=0
  while ! pg_isready -q 2>/dev/null; do
    sleep 2; ATTEMPTS=$((ATTEMPTS + 1))
    [ $ATTEMPTS -gt 15 ] && fail "PostgreSQL did not become healthy"
  done
  # Create database if it doesn't exist
  createdb muster 2>/dev/null || true
  log "✓ PostgreSQL is running (Homebrew)"
elif [ "$DB_MODE" = "docker" ]; then
  docker compose up -d
  sleep 5
  ATTEMPTS=0
  while ! docker compose exec -T db pg_isready -q 2>/dev/null; do
    sleep 2; ATTEMPTS=$((ATTEMPTS + 1))
    [ $ATTEMPTS -gt 15 ] && fail "PostgreSQL did not become healthy"
  done
  log "✓ PostgreSQL is running (Docker)"
fi

npx drizzle-kit migrate
log "✓ Migrations applied"

# ============================================================
# Phase 6: Build and start
# ============================================================
log "Phase 6: Building and starting Muster..."
npm run build
log "✓ Production build complete"

SERVICE_LABEL="com.bai.muster"
PLIST_PATH="$HOME/Library/LaunchAgents/${SERVICE_LABEL}.plist"

if [ "$SERVICE_MODE" = "launchd" ]; then
  mkdir -p "$INSTALL_DIR/logs"

  # Create launchd plist
  cat > "$PLIST_PATH" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${SERVICE_LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>$(command -v npm)</string>
        <string>run</string>
        <string>start</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${INSTALL_DIR}</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>${HOME}</string>
    </dict>

    <key>StandardOutPath</key>
    <string>${INSTALL_DIR}/logs/launchd-stdout.log</string>

    <key>StandardErrorPath</key>
    <string>${INSTALL_DIR}/logs/launchd-stderr.log</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
PLIST

  # Load and start the service
  launchctl bootout "gui/$(id -u)/${SERVICE_LABEL}" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
  log "✓ launchd service installed and started"

  # Install git hooks for auto-rebuild
  HOOKS_DIR="$INSTALL_DIR/.git/hooks"
  mkdir -p "$HOOKS_DIR"
  for hook in post-commit post-merge; do
    cat > "$HOOKS_DIR/$hook" << 'HOOKEOF'
#!/usr/bin/env bash
set -e
MUSTER_DIR="$(git rev-parse --show-toplevel)"
SERVICE="com.bai.muster"
LOGFILE="$MUSTER_DIR/logs/deploy.log"
mkdir -p "$MUSTER_DIR/logs"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ${hook}: starting rebuild..." | tee -a "$LOGFILE"
cd "$MUSTER_DIR"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Building..." | tee -a "$LOGFILE"
/opt/homebrew/bin/npm run build >> "$LOGFILE" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restarting $SERVICE..." | tee -a "$LOGFILE"
launchctl kickstart -k "gui/$(id -u)/$SERVICE" >> "$LOGFILE" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done." | tee -a "$LOGFILE"
HOOKEOF
    chmod +x "$HOOKS_DIR/$hook"
  done
  log "✓ Git hooks installed (auto-rebuild on commit/merge)"

elif [ "$SERVICE_MODE" = "pm2" ]; then
  pm2 delete muster 2>/dev/null || true
  pm2 start npm --name muster -- run start
  log "✓ Muster started via pm2"
fi

if ! wait_for_healthy "http://localhost:${MUSTER_PORT}/api/health" 30; then
  fail "Muster did not become healthy at http://localhost:${MUSTER_PORT}/api/health"
fi
log "✓ Muster is running on port $MUSTER_PORT"

# ============================================================
# Phase 7: Quick tunnel
# ============================================================
log "Phase 7: Starting remote access tunnel..."

if [ "$SERVICE_MODE" = "launchd" ]; then
  TUNNEL_LABEL="com.bai.muster-tunnel"
  TUNNEL_PLIST="$HOME/Library/LaunchAgents/${TUNNEL_LABEL}.plist"

  cat > "$TUNNEL_PLIST" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${TUNNEL_LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>$(command -v cloudflared)</string>
        <string>tunnel</string>
        <string>--url</string>
        <string>http://localhost:${MUSTER_PORT}</string>
    </array>

    <key>StandardOutPath</key>
    <string>${INSTALL_DIR}/logs/tunnel-stdout.log</string>

    <key>StandardErrorPath</key>
    <string>${INSTALL_DIR}/logs/tunnel-stderr.log</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>ThrottleInterval</key>
    <integer>30</integer>
</dict>
</plist>
PLIST

  launchctl bootout "gui/$(id -u)/${TUNNEL_LABEL}" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$TUNNEL_PLIST"
  sleep 8
  TUNNEL_URL=$(grep -o 'https://[^ ]*trycloudflare.com' "$INSTALL_DIR/logs/tunnel-stderr.log" 2>/dev/null | tail -1 || echo "")

elif [ "$SERVICE_MODE" = "pm2" ]; then
  pm2 delete muster-tunnel 2>/dev/null || true
  pm2 start cloudflared --name muster-tunnel -- tunnel --url "http://localhost:${MUSTER_PORT}"
  sleep 8
  TUNNEL_URL=$(pm2 logs muster-tunnel --lines 30 --nostream 2>&1 | grep -o 'https://[^ ]*trycloudflare.com' | tail -1 || echo "")
fi

[ -z "$TUNNEL_URL" ] && TUNNEL_URL="(check tunnel logs)"
log "✓ Tunnel: $TUNNEL_URL"

# ============================================================
# Phase 8: Persistence
# ============================================================
log "Phase 8: Setting up persistence..."

if [ "$SERVICE_MODE" = "launchd" ]; then
  log "✓ launchd services auto-start on boot (RunAtLoad + KeepAlive)"
elif [ "$SERVICE_MODE" = "pm2" ]; then
  pm2 save
  STARTUP_CMD=""
  if sudo -n true 2>/dev/null; then
    pm2 startup -s 2>/dev/null && log "✓ pm2 boot hook installed" || {
      STARTUP_CMD=$(pm2 startup 2>&1 | grep -E "^sudo" || echo "")
    }
  else
    STARTUP_CMD=$(pm2 startup 2>&1 | grep -E "^sudo" || echo "")
    [ -n "$STARTUP_CMD" ] && log "⚠ Human needs to run: $STARTUP_CMD"
  fi
fi

# ============================================================
# Phase 9: Admin account + tunnel state
# ============================================================
log "Phase 9: Creating admin account..."
# Admin auth uses MUSTER_ADMIN_KEY env var (no user table needed).
# Generate and persist the key in .env if not already set.
if grep -q "^MUSTER_ADMIN_KEY=" "$ENV_FILE" 2>/dev/null; then
  ADMIN_PASSWORD=$(grep "^MUSTER_ADMIN_KEY=" "$ENV_FILE" | cut -d= -f2)
  log "✓ Admin key already set in .env"
else
  ADMIN_PASSWORD="sk-muster-admin-$(openssl rand -hex 32)"
  echo "MUSTER_ADMIN_KEY=${ADMIN_PASSWORD}" >> "$ENV_FILE"
  log "✓ Admin key generated and saved to .env"
fi

mkdir -p "$HOME/.muster"
cat > "$HOME/.muster/tunnel.json" << EOF
{"tunnel_url": "${TUNNEL_URL}", "updated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF

# ============================================================
# Report
# ============================================================
cat <<REPORT_JSON
{
  "success": true,
  "muster_url": "http://localhost:${MUSTER_PORT}",
  "muster_endpoint": "http://localhost:${MUSTER_PORT}/mcp",
  "tunnel_url": "${TUNNEL_URL}",
  "admin_email": "admin@localhost",
  "admin_password": "${ADMIN_PASSWORD}",
  "install_dir": "${INSTALL_DIR}",
  "port": ${MUSTER_PORT},
  "db_url": "${MUSTER_DB_URL}",
  "db_mode": "${DB_MODE}",
  "service_mode": "${SERVICE_MODE}",
  "os": "${OS}"
}
REPORT_JSON

log ""
log "========================================="
log "  Muster server installed."
log "========================================="

# ============================================================
# Auto-connect this agent (unless --skip-connect)
# ============================================================
if [ "$SKIP_CONNECT" = "false" ] && [ -f "$SCRIPT_DIR/connect.sh" ]; then
  log ""
  log "Connecting this agent to Muster..."
  bash "$SCRIPT_DIR/connect.sh" --endpoint "http://localhost:${MUSTER_PORT}/mcp" "${CONNECT_ARGS[@]}" 2>&2
fi
