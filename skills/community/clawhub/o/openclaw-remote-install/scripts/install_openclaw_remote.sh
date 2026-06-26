#!/bin/bash
# Remote OpenClaw Installation Script
# Automatically selects best installation method based on OS and environment
# Supports async execution with log monitoring

set -e

# Default variables
HOST=""
USER=""
AUTH=""
SSH_PORT=22
AUTH_TYPE="key"  # key or password
METHOD=""  # auto-detect if empty
VERSION="latest"
CONFIGURE=false
NON_INTERACTIVE=false
DOCKER=false
PODMAN=false
ASYNC_MODE=false
LOG_DIR=""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { 
    echo -e "${GREEN}[INFO]${NC} $1"
    [[ -n "$LOG_FILE" ]] && echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_FILE"
}
log_warn() { 
    echo -e "${YELLOW}[WARN]${NC} $1"
    [[ -n "$LOG_FILE" ]] && echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" >> "$LOG_FILE"
}
log_error() { 
    echo -e "${RED}[ERROR]${NC} $1"
    [[ -n "$LOG_FILE" ]] && echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}
log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
    [[ -n "$LOG_FILE" ]] && echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] [DEBUG] $1" >> "$LOG_FILE"
}

# Setup log directory
setup_log_dir() {
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local host_safe=$(echo "$HOST" | tr '.' '_' | tr '@' '_')
    
    if [[ -z "$LOG_DIR" ]]; then
        LOG_DIR="$HOME/.openclaw/remote-install-logs/${host_safe}_${timestamp}"
    fi
    
    mkdir -p "$LOG_DIR"
    LOG_FILE="$LOG_DIR/install.log"
    
    # Create symlink to latest
    local latest_link="$HOME/.openclaw/remote-install-logs/latest"
    rm -f "$latest_link"
    ln -sf "$LOG_DIR" "$latest_link"
    
    log_info "Log directory: $LOG_DIR"
    log_info "Log file: $LOG_FILE"
}

show_help() {
    cat << EOF
OpenClaw Remote Installer
Usage: $0 <host> <user> <auth> [options]

Arguments:
  host              Remote server hostname/IP
  user              SSH username
  auth              SSH password or key path

Options:
  --port <port>         SSH port (default: 22)
  --method <method>     Installation method: auto, npm, git, docker, podman, cli
                        auto = auto-detect based on OS (default)
  --version <ver>       OpenClaw version (default: latest)
  --key-based           Use SSH key authentication
  --password-based      Use password authentication
  --docker              Use Docker installation
  --podman              Use Podman installation
  --configure           Run configuration after installation
  --non-interactive     Run in non-interactive mode
  --async               Run installation asynchronously with progress monitoring
  --log-dir <path>      Custom log directory (default: ~/.openclaw/remote-install-logs/)
  --help                Show this help

Examples:
  # Auto-detect best method
  $0 root@server.com user ~/.ssh/id_rsa

  # Async installation with monitoring
  $0 root@server.com user ~/.ssh/id_rsa --async

  # Force Docker installation
  $0 root@server.com user ~/.ssh/id_rsa --docker

  # Non-interactive with custom auth
  $0 admin@192.168.1.100 pass "mypassword" --password-based --non-interactive

EOF
    exit 0
}

# Parse arguments
if [[ $# -lt 3 ]]; then
    show_help
fi

HOST="$1"
USER="$2"
AUTH="$3"
shift 3

while [[ $# -gt 0 ]]; do
    case "$1" in
        --port) SSH_PORT="$2"; shift 2 ;;
        --method) METHOD="$2"; shift 2 ;;
        --version) VERSION="$2"; shift 2 ;;
        --key-based) AUTH_TYPE="key"; shift ;;
        --password-based) AUTH_TYPE="password"; shift ;;
        --docker) DOCKER=true; shift ;;
        --podman) PODMAN=true; shift ;;
        --configure) CONFIGURE=true; shift ;;
        --non-interactive) NON_INTERACTIVE=true; shift ;;
        --async) ASYNC_MODE=true; shift ;;
        --log-dir) LOG_DIR="$2"; shift 2 ;;
        --help) show_help ;;
        *) shift ;;
    esac
done

# Build SSH command
build_ssh_cmd() {
    local cmd_type="$1"
    if [[ "$AUTH_TYPE" == "password" ]]; then
        if ! command -v sshpass &> /dev/null; then
            log_error "sshpass required for password authentication"
            log_info "Install: apt-get install sshpass (Debian/Ubuntu) or brew install sshpass (macOS)"
            exit 1
        fi
        if [[ "$cmd_type" == "ssh" ]]; then
            echo "sshpass -p '$AUTH' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SSH_PORT $USER@$HOST"
        else
            echo "sshpass -p '$AUTH' scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $SSH_PORT"
        fi
    else
        if [[ "$cmd_type" == "ssh" ]]; then
            echo "ssh -i '$AUTH' -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SSH_PORT $USER@$HOST"
        else
            echo "scp -i '$AUTH' -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $SSH_PORT"
        fi
    fi
}

SSH_CMD=$(build_ssh_cmd "ssh")
SCP_CMD=$(build_ssh_cmd "scp")

# Setup logging
setup_log_dir

echo "=========================================="
echo "  OpenClaw Remote Installer"
echo "=========================================="
log_info "Host: $USER@$HOST:$SSH_PORT"
log_info "Method: ${METHOD:-auto-detect}"
log_info "Async Mode: $ASYNC_MODE"
echo "=========================================="

# Check connectivity
log_info "Checking SSH connectivity..."
if ! $SSH_CMD "echo 'SSH OK'" &>/dev/null; then
    log_error "Failed to connect to $HOST"
    exit 1
fi
log_info "SSH connection successful"

# Detect OS
log_info "Detecting remote OS..."
OS_INFO=$($SSH_CMD "cat /etc/os-release 2>/dev/null")
OS_ID=$(echo "$OS_INFO" | grep "^ID=" | cut -d= -f2 | tr -d '"')
OS_VERSION=$(echo "$OS_INFO" | grep "^VERSION_ID=" | cut -d= -f2 | tr -d '"')
OS_NAME=$(echo "$OS_INFO" | grep "^NAME=" | cut -d= -f2 | tr -d '"')

# Detect package manager
if $SSH_CMD "command -v apt-get &> /dev/null" &>/dev/null; then
    PKG_MGR="apt"
elif $SSH_CMD "command -v dnf &> /dev/null" &>/dev/null; then
    PKG_MGR="dnf"
elif $SSH_CMD "command -v yum &> /dev/null" &>/dev/null; then
    PKG_MGR="yum"
elif $SSH_CMD "command -v apk &> /dev/null" &>/dev/null; then
    PKG_MGR="apk"
elif $SSH_CMD "command -v pacman &> /dev/null" &>/dev/null; then
    PKG_MGR="pacman"
else
    PKG_MGR="unknown"
fi

log_info "OS: $OS_NAME (ID: $OS_ID, Version: $OS_VERSION)"
log_info "Package Manager: $PKG_MGR"

# Check if OpenClaw already installed
if $SSH_CMD "command -v openclaw &> /dev/null" 2>/dev/null; then
    EXISTING_VERSION=$($SSH_CMD "openclaw --version 2>/dev/null || echo 'unknown'")
    log_warn "OpenClaw already installed: $EXISTING_VERSION"
    if [[ "$ASYNC_MODE" != "true" ]]; then
        read -p "Update? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Installation cancelled"
            exit 0
        fi
    fi
fi

# Auto-detect best installation method
detect_install_method() {
    local detected=""
    
    # Docker option
    if [[ "$DOCKER" == "true" ]]; then
        if $SSH_CMD "command -v docker &> /dev/null" 2>/dev/null; then
            echo "docker"
            return
        else
            log_warn "Docker not installed, falling back to installer script"
        fi
    fi
    
    # Podman option
    if [[ "$PODMAN" == "true" ]]; then
        if $SSH_CMD "command -v podman &> /dev/null" 2>/dev/null; then
            echo "podman"
            return
        else
            log_warn "Podman not installed, falling back to installer script"
        fi
    fi
    
    # Check if Node.js 22+ is available
    if $SSH_CMD "command -v node &> /dev/null" 2>/dev/null; then
        NODE_VERSION=$($SSH_CMD "node -v" | sed 's/v//')
        NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)
        if [[ "$NODE_MAJOR" -ge 22 ]]; then
            if $SSH_CMD "command -v pnpm &> /dev/null" 2>/dev/null; then
                detected="pnpm"
            elif $SSH_CMD "command -v npm &> /dev/null" 2>/dev/null; then
                detected="npm"
            fi
        fi
    fi
    
    # Default: installer script
    if [[ -z "$detected" ]]; then
        detected="installer"
    fi
    
    echo "$detected"
}

if [[ -z "$METHOD" ]] || [[ "$METHOD" == "auto" ]]; then
    METHOD=$(detect_install_method)
fi

log_info "Selected installation method: $METHOD"

# Prepare installation command
prepare_install_cmd() {
    local install_cmd=""
    
    case "$METHOD" in
        docker)
            log_info "Preparing Docker installation..."
            # Check if Docker is available
            if ! $SSH_CMD "command -v docker &> /dev/null" 2>/dev/null; then
                log_info "Installing Docker first..."
                install_cmd="curl -fsSL https://get.docker.com | sh"
            fi
            # Run OpenClaw Docker
            install_cmd="docker run -d --name openclaw \
                -v ~/.openclaw:/home/node/.openclaw \
                -p 18789:18789 \
                openclawai/openclaw:latest"
            ;;
            
        podman)
            log_info "Preparing Podman installation..."
            if ! $SSH_CMD "command -v podman &> /dev/null" 2>/dev/null; then
                log_info "Installing Podman first..."
                case "$PKG_MGR" in
                    apt) install_cmd="apt-get update && apt-get install -y podman" ;;
                    dnf|yum) install_cmd="$PKG_MGR install -y podman" ;;
                    apk) install_cmd="apk add podman" ;;
                esac
            fi
            install_cmd="podman run -d --name openclaw \
                -v ~/.openclaw:/home/node/.openclaw \
                -p 18789:18789 \
                openclawai/openclaw:latest"
            ;;
            
        pnpm)
            log_info "Preparing pnpm installation..."
            if [[ "$NON_INTERACTIVE" == "true" ]]; then
                install_cmd="pnpm add -g openclaw@$VERSION && pnpm approve-builds -g openclaw"
            else
                install_cmd="pnpm add -g openclaw@$VERSION"
            fi
            ;;
            
        npm)
            log_info "Preparing npm installation..."
            install_cmd="npm install -g openclaw@$VERSION"
            ;;
            
        cli|install-cli)
            log_info "Preparing install-cli.sh installation..."
            install_cmd="curl -fsSL https://openclaw.ai/install-cli.sh | bash -s -- --version $VERSION"
            if [[ "$NON_INTERACTIVE" == "true" ]]; then
                install_cmd="$install_cmd --no-onboard"
            fi
            ;;
            
        installer|*)
            log_info "Preparing installer script installation..."
            install_cmd="curl -fsSL https://openclaw.ai/install.sh | bash -s --"
            if [[ "$VERSION" != "latest" ]]; then
                install_cmd="$install_cmd --version $VERSION"
            fi
            if [[ "$NON_INTERACTIVE" == "true" ]]; then
                install_cmd="$install_cmd --no-prompt --no-onboard"
            fi
            ;;
    esac
    
    echo "$install_cmd"
}

# Async installation with progress monitoring
run_async_install() {
    local install_cmd="$1"
    local pid_file="$LOG_DIR/install.pid"
    local status_file="$LOG_DIR/install.status"
    local output_file="$LOG_DIR/install_output.log"
    
    echo "running" > "$status_file"
    
    log_info "Starting async installation..."
    log_info "Monitor with: tail -f $LOG_DIR/install_output.log"
    log_info "Check status: cat $LOG_DIR/install_status"
    
    # Run installation in background, capture output
    (
        set -e
        {
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting installation..."
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Command: $install_cmd"
            echo "---"
            $SSH_CMD "$install_cmd" 2>&1
            exit_code=$?
            echo "---"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Installation finished with exit code: $exit_code"
            exit $exit_code
        } | tee "$output_file"
    ) &
    
    local bg_pid=$!
    echo $bg_pid > "$pid_file"
    
    log_info "Installation running in background (PID: $bg_pid)"
    log_info "Log file: $output_file"
    
    # Monitor progress
    monitor_installation "$pid_file" "$status_file" "$output_file"
}

# Monitor installation progress
monitor_installation() {
    local pid_file="$1"
    local status_file="$2"
    local output_file="$3"
    local check_interval=5
    local max_wait=3600  # 1 hour max
    local elapsed=0
    local spinner=('|' '/' '-' '\\')
    local spin_idx=0
    
    echo ""
    log_info "Monitoring installation progress..."
    echo "=========================================="
    
    while [[ $elapsed -lt $max_wait ]]; do
        # Check if process is still running
        if [[ -f "$pid_file" ]]; then
            local pid=$(cat "$pid_file" 2>/dev/null)
            if ! kill -0 "$pid" 2>/dev/null; then
                # Process finished
                wait "$pid"
                local exit_code=$?
                
                if [[ $exit_code -eq 0 ]]; then
                    echo "success" > "$status_file"
                    echo ""
                    echo "=========================================="
                    log_info "Installation completed successfully!"
                    echo "=========================================="
                else
                    echo "failed" > "$status_file"
                    echo ""
                    echo "=========================================="
                    log_error "Installation failed with exit code: $exit_code"
                    echo "=========================================="
                fi
                
                log_info "Final output saved to: $output_file"
                return $exit_code
            fi
        fi
        
        # Show last few lines of output
        if [[ -f "$output_file" ]]; then
            local last_line=$(tail -1 "$output_file" 2>/dev/null)
            printf "\r${CYAN}[%s]${NC} Checking... Last: %s" \
                "${spinner[$((spin_idx % 4))]}" \
                "${last_line:0:50}"
        fi
        
        sleep $check_interval
        elapsed=$((elapsed + check_interval))
        spin_idx=$((spin_idx + 1))
    done
    
    echo ""
    log_warn "Installation timeout reached ($max_wait seconds)"
    echo "timeout" > "$status_file"
    return 1
}

# Sync installation (original behavior)
run_sync_install() {
    local install_cmd="$1"
    local output_file="$LOG_DIR/install_output.log"
    
    log_info "Running installation (synchronous)..."
    {
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting installation..."
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Command: $install_cmd"
        echo "---"
        $SSH_CMD "$install_cmd" 2>&1
        exit_code=$?
        echo "---"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Installation finished with exit code: $exit_code"
    } | tee "$output_file"
    
    return $exit_code
}

# Execute installation
INSTALL_CMD=$(prepare_install_cmd)

if [[ "$ASYNC_MODE" == "true" ]]; then
    run_async_install "$INSTALL_CMD"
    EXIT_CODE=$?
else
    run_sync_install "$INSTALL_CMD"
    EXIT_CODE=$?
fi

if [[ $EXIT_CODE -ne 0 ]]; then
    log_error "Installation failed with exit code: $EXIT_CODE"
    log_info "Check logs: $LOG_DIR/install_output.log"
    exit $EXIT_CODE
fi

# Verify installation
log_info "Verifying installation..."
sleep 2

if [[ "$METHOD" == "docker" ]] || [[ "$METHOD" == "podman" ]]; then
    if $SSH_CMD "docker ps | grep -q openclaw" 2>/dev/null; then
        log_info "OpenClaw container is running!"
        log_info "Container logs: $SSH_CMD docker logs openclaw"
    else
        log_error "Container failed to start"
        exit 1
    fi
else
    if $SSH_CMD "command -v openclaw &> /dev/null" 2>/dev/null; then
        VERSION_INSTALLED=$($SSH_CMD "openclaw --version")
        log_info "OpenClaw installed successfully: $VERSION_INSTALLED"
    else
        log_error "Installation verification failed"
        exit 1
    fi
fi

# Configuration (optional)
if [[ "$CONFIGURE" == "true" ]]; then
    log_info "Configuration requested..."
    if [[ "$NON_INTERACTIVE" == "true" ]]; then
        log_warn "Non-interactive configuration requires additional setup"
        log_info "Run 'openclaw configure' manually on remote host"
    else
        log_info "Starting configuration wizard..."
        $SSH_CMD "openclaw configure"
    fi
fi

echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
log_info "Connect to remote: ssh $USER@$HOST"
log_info "Check status: $SSH_CMD openclaw status"
log_info "Run dashboard: $SSH_CMD openclaw dashboard"
log_info "Log directory: $LOG_DIR"
echo "=========================================="
