
#!/bin/bash
# docker-setup.sh - OpenClaw Docker Management Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  🦞 OpenClaw Docker Management${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not installed. Install from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose not installed."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check .env file
check_env() {
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        echo ""
        echo "Please create a .env file with your configuration:"
        echo "  cp .env.example .env"
        echo "  nano .env"
        echo ""
        echo "Required variables:"
        echo "  - ANTHROPIC_API_KEY or OPENAI_API_KEY"
        echo "  - OPENCLAW_GATEWAY_TOKEN"
        exit 1
    fi
    
    # Check for required keys
    if ! grep -q "ANTHROPIC_API_KEY\|OPENAI_API_KEY" .env; then
        print_warning "No AI API key found in .env file"
    fi
    
    if ! grep -q "OPENCLAW_GATEWAY_TOKEN" .env; then
        print_warning "OPENCLAW_GATEWAY_TOKEN not set in .env file"
    fi
    
    print_success ".env file found"
}

# Fix config if needed
fix_config() {
    if [ -f ~/.openclaw/openclaw.json ]; then
        print_info "Checking OpenClaw config..."
        
        # Check if gateway.mode is set
        if ! grep -q '"mode".*:.*"local"' ~/.openclaw/openclaw.json; then
            print_warning "Config missing gateway.mode, running doctor --fix..."
            docker-compose run --rm openclaw-cli doctor --fix || true
        fi
        
        print_success "Config checked"
    fi
}

# Start OpenClaw
start() {
    print_header
    check_prerequisites
    check_env
    
    print_info "Starting OpenClaw..."
    
    # Clean up orphan containers
    docker-compose down --remove-orphans 2>/dev/null || true
    
    # Pull latest image
    print_info "Pulling latest OpenClaw image..."
    docker-compose pull
    
    # Start services
    docker-compose up -d
    
    # Wait for gateway to start
    print_info "Waiting for gateway to start..."
    sleep 5
    
    # Fix config if needed
    fix_config
    
    # Get status
    echo ""
    print_success "OpenClaw started!"
    echo ""
    
    # Show access info
    show_info
}

# Stop OpenClaw
stop() {
    print_header
    print_info "Stopping OpenClaw..."
    
    docker-compose down
    
    # Stop Tailscale serve if running
    if command -v tailscale &> /dev/null; then
        tailscale serve --bg off 18789 2>/dev/null || true
    fi
    
    print_success "OpenClaw stopped"
}

# Restart OpenClaw
restart() {
    print_header
    print_info "Restarting OpenClaw..."
    
    docker-compose restart openclaw
    sleep 3
    
    print_success "OpenClaw restarted"
    show_info
}

# Show logs
logs() {
    print_header
    print_info "Showing OpenClaw logs (Ctrl+C to exit)..."
    echo ""
    docker-compose logs -f openclaw
}

# Show status and access info
show_info() {
    # Get token from .env (masked for display)
    TOKEN=$(grep OPENCLAW_GATEWAY_TOKEN .env | cut -d '=' -f2)
    MASKED_TOKEN="${TOKEN:0:8}...${TOKEN: -4}"
    
    # Get Tailscale IP if available
    if command -v tailscale &> /dev/null; then
        TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "")
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Access Information"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  Local Access:"
    echo "    http://localhost:18789?token=$MASKED_TOKEN"
    echo "    (token masked — full token in .env)"
    echo ""
    
    if [ -n "$TAILSCALE_IP" ]; then
        echo "  Tailscale Access:"
        echo "    http://$TAILSCALE_IP:18789?token=$MASKED_TOKEN"
        echo ""
    fi
    
    echo "  Useful Commands:"
    echo "    ./docker-setup.sh logs    - View logs"
    echo "    ./docker-setup.sh status  - Check status"
    echo "    ./docker-setup.sh stop    - Stop OpenClaw"
    echo ""
}

# Show status
status() {
    print_header
    
    # Container status
    print_info "Container Status:"
    docker-compose ps
    echo ""
    
    # OpenClaw status
    print_info "OpenClaw Status:"
    docker-compose run --rm openclaw-cli status --all 2>/dev/null || {
        print_error "Could not get OpenClaw status (gateway may not be running)"
    }
}

# Run doctor
doctor() {
    print_header
    print_info "Running OpenClaw doctor..."
    echo ""
    docker-compose run --rm openclaw-cli doctor --fix
}

# Pairing approve telegram
approve_telagram() {
    print_header
    print_info "Running OpenClaw pairing approval..."
    echo ""

    while true; do
        printf "Enter Telegram Approval code: " 
        read CODE

        if [ -n "$CODE" ];  then
            break
        fi
        echo "Code cannot be empty. Try again."
    done

    docker-compose run --rm openclaw-cli pairing approve telegram "$CODE"
}

# Security audit
security_audit() {
    print_header
    print_info "Running OpenClaw security audit..."
    echo ""

    docker-compose run --rm openclaw-cli security audit --deep                           
    docker-compose run --rm openclaw-cli security audit --fix
}

# Setup Tailscale
setup_tailscale() {
    print_header
    
    if ! command -v tailscale &> /dev/null; then
        print_error "Tailscale not installed"
        echo ""
        echo "Install with: sudo apt install tailscale"
        echo "Then run: sudo tailscale up"
        exit 1
    fi
    
    if ! tailscale status &> /dev/null; then
        print_warning "Tailscale not connected"
        echo ""
        echo "Connect with: sudo tailscale up"
        exit 1
    fi
    
    print_info "Starting Tailscale serve on port 18789..."
    tailscale serve --bg http://localhost:18789
    
    print_success "Tailscale serve started"
    echo ""
    
    TAILSCALE_IP=$(tailscale ip -4)
    TOKEN=$(grep OPENCLAW_GATEWAY_TOKEN .env | cut -d '=' -f2)
    
    MASKED_TOKEN="${TOKEN:0:4}...[redacted]"

    echo "Access from other devices:"
    echo "  http://$TAILSCALE_IP:18789?token=$MASKED_TOKEN"
    echo "  (token masked — full token in .env)"
}

# Show help
show_help() {
    print_header
    echo ""
    echo "Usage: ./docker-setup.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start               - Start OpenClaw"
    echo "  stop                - Stop OpenClaw"
    echo "  restart             - Restart OpenClaw"
    echo "  logs                - Show logs (Ctrl+C to exit)"
    echo "  status              - Show status"
    echo "  doctor              - Run diagnostics and fix issues"
    echo "  info                - Show access URLs"
    echo "  approve_telagram    - Telegram pairing approval"
    echo "  security_audit      - Run/fix security audit"
    echo "  tailscale           - Setup Tailscale access"
    echo "  help                - Show this help"
    echo ""
    echo "Examples:"
    echo "  ./docker-setup.sh start"
    echo "  ./docker-setup.sh logs"
    echo "  ./docker-setup.sh status"
    echo ""
}

# Main script
case "${1:-}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    doctor)
        doctor
        ;;
    info)
        print_header
        show_info
        ;;
    approve_telagram)
        approve_telagram
        ;;
    security_audit)
        security_audit
        ;;
    fix_config)
        fix_config
        ;;
    tailscale)
        setup_tailscale
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: ${1:-}"
        echo ""
        show_help
        exit 1
        ;;
esac
