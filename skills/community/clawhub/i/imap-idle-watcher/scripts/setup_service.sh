#!/usr/bin/env bash
set -euo pipefail

# ── IMAP IDLE Watcher — Systemd Service Setup ────────────────────────────
# Installs or uninstalls the watcher as a systemd service.
#
# Usage:
#   ./setup_service.sh                          # Interactive setup
#   ./setup_service.sh --account x --password y --command "..." [options]
#   ./setup_service.sh --uninstall [--service-name NAME]
#   ./setup_service.sh --test --account x --password y [--host H --port P]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DAEMON_SCRIPT="$SCRIPT_DIR/imap_idle_daemon.py"

# Defaults
SERVICE_NAME=""
ACCOUNT=""
PASSWORD=""
HOST="imap.gmail.com"
PORT="993"
FOLDER="INBOX"
COMMAND=""
IDLE_TIMEOUT="1200"
DEBOUNCE="10"
FILTER_FROM=""
FILTER_SUBJECT=""
UNINSTALL=false
TEST_ONLY=false

# ── Provider detection ────────────────────────────────────────────────────

detect_provider() {
    local email="$1"
    local domain="${email##*@}"
    domain="${domain,,}"  # lowercase

    case "$domain" in
        gmail.com|googlemail.com)
            HOST="imap.gmail.com"; PORT="993"
            echo "📧 Detected: Gmail"
            echo "   You need a Gmail App Password."
            echo "   1. Go to: https://myaccount.google.com/apppasswords"
            echo "   2. Select app: Mail → Generate"
            echo "   3. Copy the 16-character password"
            echo "   ℹ️  Requires 2FA enabled on your Google account"
            ;;
        outlook.com|hotmail.com|live.com)
            HOST="outlook.office365.com"; PORT="993"
            echo "📧 Detected: Outlook/Hotmail"
            echo "   You need an App Password."
            echo "   1. Go to: https://account.live.com/proofs/AppPassword"
            echo "   2. Generate and copy the password"
            ;;
        yahoo.com|ymail.com)
            HOST="imap.mail.yahoo.com"; PORT="993"
            echo "📧 Detected: Yahoo"
            echo "   You need an App Password."
            echo "   1. Go to: https://login.yahoo.com/account/security/app-passwords"
            echo "   2. Generate and copy the password"
            ;;
        *)
            echo "📧 Provider: $domain (custom)"
            echo "   Using host: $HOST:$PORT"
            echo "   Make sure IMAP is enabled and you have the right credentials."
            ;;
    esac
}

# ── Test connection ───────────────────────────────────────────────────────

test_connection() {
    echo ""
    echo "🔍 Testing connection to $HOST:$PORT..."
    IMAP_ACCOUNT="$ACCOUNT" IMAP_PASSWORD="$PASSWORD" IMAP_HOST="$HOST" \
        IMAP_PORT="$PORT" IMAP_FOLDER="$FOLDER" ON_NEW_MAIL_CMD="" \
        python3 "$DAEMON_SCRIPT" --preflight-only 2>&1 || true

    # Simple Python test as fallback
    python3 -c "
import imaplib, ssl, sys
try:
    ctx = ssl.create_default_context()
    m = imaplib.IMAP4_SSL('$HOST', $PORT, ssl_context=ctx)
    m.login('$ACCOUNT', '$PASSWORD')
    m.select('$FOLDER')
    typ, caps = m.capability()
    cap_str = caps[0].decode() if caps and caps[0] else ''
    if 'IDLE' not in cap_str:
        print('⚠️  Server does not advertise IDLE support. Watcher may not work.')
    else:
        print('✅ Connection OK — IDLE supported')
    m.logout()
except imaplib.IMAP4.error as e:
    print(f'❌ Auth failed: {e}')
    print('   Check your credentials. For Gmail, use an App Password (not your regular password).')
    sys.exit(1)
except Exception as e:
    print(f'❌ Connection failed: {e}')
    sys.exit(1)
" 2>&1
}

# ── Interactive setup ─────────────────────────────────────────────────────

interactive_setup() {
    echo "═══════════════════════════════════════════"
    echo "  IMAP IDLE Watcher — Setup"
    echo "═══════════════════════════════════════════"
    echo ""

    # Account
    read -rp "Email address: " ACCOUNT
    if [ -z "$ACCOUNT" ]; then
        echo "❌ Email address is required."; exit 1
    fi

    # Detect provider
    echo ""
    detect_provider "$ACCOUNT"
    echo ""

    # Allow host override
    read -rp "IMAP host [$HOST]: " input
    HOST="${input:-$HOST}"
    read -rp "IMAP port [$PORT]: " input
    PORT="${input:-$PORT}"

    # Password
    read -rsp "App password: " PASSWORD
    echo ""
    if [ -z "$PASSWORD" ]; then
        echo "❌ Password is required."; exit 1
    fi

    # Test
    test_connection

    # Folder
    read -rp "Folder to watch [INBOX]: " input
    FOLDER="${input:-$FOLDER}"

    # Command
    echo ""
    echo "What command should run when new email arrives?"
    echo "  Examples:"
    echo "    python3 /path/to/my_script.py"
    echo "    curl -X POST https://my-webhook.com/notify"
    echo "    echo 'New mail!' >> /var/log/mail-events.log"
    echo ""
    read -rp "Command: " COMMAND

    # Filters
    echo ""
    echo "Optional: filter emails (comma-separated, case-insensitive substring match)"
    echo "  Leave blank to process ALL incoming emails."
    read -rp "Filter by sender (e.g. paypal.com,bank.com): " FILTER_FROM
    read -rp "Filter by subject (e.g. payment,invoice): " FILTER_SUBJECT

    # Service name
    read -rp "Service name [imap-idle-watcher]: " input
    SERVICE_NAME="${input:-imap-idle-watcher}"

    echo ""
    echo "═══════════════════════════════════════════"
    echo "  Summary"
    echo "═══════════════════════════════════════════"
    echo "  Account:  $ACCOUNT"
    echo "  Host:     $HOST:$PORT"
    echo "  Folder:   $FOLDER"
    echo "  Command:  ${COMMAND:-(none)}"
    echo "  Filter:   from=${FILTER_FROM:-(all)} subject=${FILTER_SUBJECT:-(all)}"
    echo "  Service:  $SERVICE_NAME"
    echo "═══════════════════════════════════════════"
    echo ""
    read -rp "Install service? [Y/n]: " confirm
    if [[ "${confirm,,}" == "n" ]]; then
        echo "Aborted."; exit 0
    fi
}

# ── Install service ───────────────────────────────────────────────────────

install_service() {
    local env_file="/etc/${SERVICE_NAME}.env"
    local unit_file="/etc/systemd/system/${SERVICE_NAME}.service"

    echo ""
    echo "📦 Installing service: $SERVICE_NAME"

    # Write env file (restricted permissions)
    cat > "$env_file" <<EOF
IMAP_ACCOUNT=$ACCOUNT
IMAP_PASSWORD=$PASSWORD
IMAP_HOST=$HOST
IMAP_PORT=$PORT
IMAP_FOLDER=$FOLDER
ON_NEW_MAIL_CMD=$COMMAND
FILTER_FROM=$FILTER_FROM
FILTER_SUBJECT=$FILTER_SUBJECT
IDLE_TIMEOUT=$IDLE_TIMEOUT
DEBOUNCE_SECONDS=$DEBOUNCE
EOF
    chmod 600 "$env_file"
    echo "   ✅ Env file: $env_file (mode 600)"

    # Write systemd unit
    cat > "$unit_file" <<EOF
[Unit]
Description=IMAP IDLE Watcher ($ACCOUNT)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=$env_file
ExecStart=$(command -v python3) $DAEMON_SCRIPT
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    echo "   ✅ Unit file: $unit_file"

    # Enable and start
    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    systemctl start "$SERVICE_NAME"

    echo "   ✅ Service started!"
    echo ""
    echo "📋 Useful commands:"
    echo "   systemctl status $SERVICE_NAME"
    echo "   journalctl -u $SERVICE_NAME -f"
    echo "   systemctl restart $SERVICE_NAME"
    echo "   systemctl stop $SERVICE_NAME"
    echo ""

    # Quick status check
    sleep 2
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo "✅ $SERVICE_NAME is running."
    else
        echo "⚠️  Service may have failed to start. Check:"
        echo "   journalctl -u $SERVICE_NAME --no-pager -n 20"
    fi
}

# ── Uninstall ─────────────────────────────────────────────────────────────

uninstall_service() {
    local svc="${SERVICE_NAME:-imap-idle-watcher}"
    local env_file="/etc/${svc}.env"
    local unit_file="/etc/systemd/system/${svc}.service"

    echo "🗑️  Uninstalling service: $svc"

    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        systemctl stop "$svc"
        echo "   Stopped."
    fi

    if systemctl is-enabled --quiet "$svc" 2>/dev/null; then
        systemctl disable "$svc"
        echo "   Disabled."
    fi

    [ -f "$unit_file" ] && rm -f "$unit_file" && echo "   Removed: $unit_file"
    [ -f "$env_file" ] && rm -f "$env_file" && echo "   Removed: $env_file"

    systemctl daemon-reload
    echo "✅ Uninstalled."
}

# ── Parse args ────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case "$1" in
        --account)      ACCOUNT="$2"; shift 2 ;;
        --password)     PASSWORD="$2"; shift 2 ;;
        --host)         HOST="$2"; shift 2 ;;
        --port)         PORT="$2"; shift 2 ;;
        --folder)       FOLDER="$2"; shift 2 ;;
        --command)      COMMAND="$2"; shift 2 ;;
        --service-name) SERVICE_NAME="$2"; shift 2 ;;
        --filter-from)  FILTER_FROM="$2"; shift 2 ;;
        --filter-subject) FILTER_SUBJECT="$2"; shift 2 ;;
        --idle-timeout) IDLE_TIMEOUT="$2"; shift 2 ;;
        --debounce)     DEBOUNCE="$2"; shift 2 ;;
        --uninstall)    UNINSTALL=true; shift ;;
        --test)         TEST_ONLY=true; shift ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --account EMAIL       Email address"
            echo "  --password PASS       App password"
            echo "  --host HOST           IMAP host (default: auto-detect from email)"
            echo "  --port PORT           IMAP port (default: 993)"
            echo "  --folder FOLDER       Folder to watch (default: INBOX)"
            echo "  --command CMD         Command to run on new mail"
            echo "  --service-name NAME   Systemd service name (default: imap-idle-watcher)"
            echo "  --filter-from VALS    Only trigger for these senders (comma-separated)"
            echo "  --filter-subject VALS Only trigger for these subjects (comma-separated)"
            echo "  --idle-timeout SECS   IDLE renewal interval (default: 1200)"
            echo "  --debounce SECS       Min seconds between runs (default: 10)"
            echo "  --test                Test connection only"
            echo "  --uninstall           Remove service"
            echo "  -h, --help            Show this help"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# ── Main ──────────────────────────────────────────────────────────────────

if $UNINSTALL; then
    uninstall_service
    exit 0
fi

if $TEST_ONLY; then
    if [ -z "$ACCOUNT" ] || [ -z "$PASSWORD" ]; then
        echo "❌ --test requires --account and --password"
        exit 1
    fi
    detect_provider "$ACCOUNT"
    test_connection
    exit 0
fi

# Interactive if no account provided
if [ -z "$ACCOUNT" ]; then
    interactive_setup
else
    SERVICE_NAME="${SERVICE_NAME:-imap-idle-watcher}"
    detect_provider "$ACCOUNT"
    if [ -n "$ACCOUNT" ] && [ -n "$PASSWORD" ]; then
        test_connection
    fi
fi

install_service
