#!/bin/bash
# OpenClaw Command Test Script
# Used to test and validate OpenClaw commands

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
check_command() {
    if command -v "$1" &> /dev/null; then
        log_success "Command $1 exists"
        return 0
    else
        log_error "Command $1 does not exist"
        return 1
    fi
}

# Test OpenClaw basic commands
test_openclaw_basic() {
    log_info "Testing OpenClaw basic commands..."
    
    # Test if openclaw command exists
    check_command "openclaw"
    
    # Test openclaw help
    log_info "Running openclaw help..."
    if openclaw help &> /dev/null; then
        log_success "openclaw help executed successfully"
    else
        log_error "openclaw help execution failed"
        return 1
    fi
    
    # Test openclaw status
    log_info "Running openclaw status..."
    if openclaw status &> /dev/null; then
        log_success "openclaw status executed successfully"
    else
        log_warning "openclaw status execution failed (may be normal)"
    fi
    
    # Test openclaw version
    log_info "Running openclaw version..."
    if openclaw version &> /dev/null; then
        log_success "openclaw version executed successfully"
    else
        log_warning "openclaw version execution failed"
    fi
}

# Test OpenClaw subcommands
test_openclaw_subcommands() {
    log_info "Testing OpenClaw subcommands..."
    
    local subcommands=("agents" "cron" "skills" "gateway" "config" "configure")
    
    for cmd in "${subcommands[@]}"; do
        log_info "Testing openclaw $cmd --help..."
        if openclaw "$cmd" --help &> /dev/null; then
            log_success "openclaw $cmd --help executed successfully"
        else
            log_warning "openclaw $cmd --help execution failed"
        fi
    done
}

# Test specific feature
test_specific_feature() {
    local feature="$1"
    
    log_info "Testing $feature functionality..."
    
    case "$feature" in
        "agents")
            # Test agents related commands
            log_info "Listing agents..."
            openclaw agents list 2>/dev/null || log_warning "Unable to list agents"
            ;;
        "cron")
            # Test cron related commands
            log_info "Listing cron jobs..."
            openclaw cron list 2>/dev/null || log_warning "Unable to list cron jobs"
            ;;
        "skills")
            # Test skills related commands
            log_info "Listing skills..."
            openclaw skills list 2>/dev/null || log_warning "Unable to list skills"
            ;;
        "gateway")
            # Test gateway related commands
            log_info "Checking gateway status..."
            openclaw gateway status 2>/dev/null || log_warning "Unable to check gateway status"
            ;;
        *)
            log_warning "Unknown feature: $feature"
            ;;
    esac
}

# Save command help
save_command_help() {
    local command="$1"
    local output_file="${2:-memory/openclaw-knowledge/commands/$command.md}"
    
    log_info "Getting $command help and saving to $output_file..."
    
    # Create directory
    mkdir -p "$(dirname "$output_file")"
    
    # Get help information
    if openclaw "$command" --help &> /dev/null; then
        {
            echo "# openclaw $command command help"
            echo ""
            echo "## Command Help"
            echo '```bash'
            openclaw "$command" --help
            echo '```'
            echo ""
            echo "## Obtained At"
            echo "$(date '+%Y-%m-%d %H:%M:%S')"
        } > "$output_file"
        log_success "Saved $command help to $output_file"
    else
        log_error "Unable to get $command help"
    fi
}

# Search OpenClaw information
search_openclaw_info() {
    local query="$1"
    local output_file="${2:-memory/openclaw-knowledge/search-results/$(date +%Y%m%d).md}"
    
    log_info "Searching OpenClaw information: $query"
    
    # Create directory
    mkdir -p "$(dirname "$output_file")"
    
    # Use MiniMax web_search (if available)
    if command -v mcporter &> /dev/null; then
        log_info "Using MiniMax web_search..."
        {
            echo "# Search Results: $query"
            echo ""
            echo "## Search Time"
            echo "$(date '+%Y-%m-%d %H:%M:%S')"
            echo ""
            echo "## Search Results"
            echo '```json'
            mcporter call MiniMax.web_search query:"$query" 2>/dev/null || echo "Search failed"
            echo '```'
        } >> "$output_file"
        log_success "Search completed, results saved to $output_file"
    else
        log_warning "mcporter not available, unable to use MiniMax web_search"
    fi
}

# Main function
main() {
    log_info "Starting OpenClaw command testing"
    
    # Check if openclaw is installed
    if ! check_command "openclaw"; then
        log_error "OpenClaw not installed, testing terminated"
        exit 1
    fi
    
    # Test basic commands
    test_openclaw_basic
    
    # Test subcommands
    test_openclaw_subcommands
    
    # Test specific features based on arguments
    if [ $# -gt 0 ]; then
        for arg in "$@"; do
            test_specific_feature "$arg"
        done
    fi
    
    # Save command help (optional)
    if [ "$SAVE_HELP" = "true" ]; then
        save_command_help "agents"
        save_command_help "cron"
        save_command_help "skills"
        save_command_help "gateway"
    fi
    
    # Search information (optional)
    if [ -n "$SEARCH_QUERY" ]; then
        search_openclaw_info "$SEARCH_QUERY"
    fi
    
    log_success "OpenClaw command testing completed"
}

# Show usage
usage() {
    echo "Usage: $0 [options] [features...]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Display this help information"
    echo "  --save-help         Save command help to knowledge base"
    echo "  --search <query>    Search OpenClaw information"
    echo ""
    echo "Features:"
    echo "  agents             Test agents functionality"
    echo "  cron               Test cron functionality"
    echo "  skills             Test skills functionality"
    echo "  gateway            Test gateway functionality"
    echo ""
    echo "Examples:"
    echo "  $0                 Run all basic tests"
    echo "  $0 agents cron     Test agents and cron functionality"
    echo "  $0 --save-help     Save command help"
    echo "  $0 --search \"OpenClaw agents configuration\" Search information"
}

# Parse arguments
POSITIONAL_ARGS=()
SAVE_HELP="false"
SEARCH_QUERY=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        --save-help)
            SAVE_HELP="true"
            shift
            ;;
        --search)
            SEARCH_QUERY="$2"
            shift 2
            ;;
        --*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Set positional arguments
set -- "${POSITIONAL_ARGS[@]}"

# Run main function
main "$@"
