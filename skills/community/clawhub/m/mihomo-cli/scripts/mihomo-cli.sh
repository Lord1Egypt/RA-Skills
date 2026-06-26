#!/bin/bash
# Mihomo CLI Helper Script
# Usage: mihomo-cli <command> [args]

set -e

# Auto-detect Mihomo installation
MIHOMO_CONFIG_PATH=""
MIHOMO_API_HOST="127.0.0.1:9090"
MIHOMO_SECRET=""

# Configuration sources (priority order: env > arg > auto-detect)
MIHOMO_CONFIG_PATH="${MIHOMO_CONFIG:-}"
MIHOMO_API_HOST="${MIHOMO_HOST:-127.0.0.1:9090}"
MIHOMO_SECRET="${MIHOMO_SECRET:-}"

# Try to find mihomo config
detect_mihomo() {
    # Skip if already set via environment
    [ -n "$MIHOMO_CONFIG_PATH" ] && [ -f "$MIHOMO_CONFIG_PATH" ] && {
        extract_from_config
        return 0
    }
    
    # Common paths to check
    local paths=(
        # macOS ClashMac
        "$HOME/Library/Application Support/clashmac/work/config.yaml"
        "$HOME/Library/Application Support/com.metacubex.mihomo/config.yaml"
        # Linux standard
        "$HOME/.config/mihomo/config.yaml"
        "$HOME/.config/clash/config.yaml"
        "$HOME/.config/clash-verge/config.yaml"
        # Windows WSL path
        "/mnt/c/Users/$USER/.config/mihomo/config.yaml"
        # Custom install
        "/etc/mihomo/config.yaml"
        "/usr/local/etc/mihomo/config.yaml"
    )
    
    # Check if mihomo is running and get config from process
    local proc_config=$(ps aux 2>/dev/null | grep -E "mihomo|clash" | grep -v grep | grep -oE "\-f\s+\S+" | head -1 | sed 's/-f //' | xargs)
    [ -n "$proc_config" ] && [ -f "$proc_config" ] && {
        MIHOMO_CONFIG_PATH="$proc_config"
        extract_from_config
        return 0
    }
    
    # Check home directory variations
    for path in "${paths[@]}"; do
        [ -f "$path" ] && {
            MIHOMO_CONFIG_PATH="$path"
            extract_from_config
            return 0
        }
    done
    
    return 1
}

# Extract config values from file
extract_from_config() {
    [ -z "$MIHOMO_CONFIG_PATH" ] && return 1
    [ -f "$MIHOMO_CONFIG_PATH" ] || return 1
    
    # Extract secret (handle various formats)
    [ -z "$MIHOMO_SECRET" ] && {
        MIHOMO_SECRET=$(grep -E "^\s*secret:" "$MIHOMO_CONFIG_PATH" 2>/dev/null | head -1 | sed 's/.*secret:\s*//' | tr -d '"' | tr -d "'" | xargs)
    }
    
    # Extract external-controller
    [ "$MIHOMO_API_HOST" = "127.0.0.1:9090" ] && {
        local controller=$(grep -E "^\s*external-controller:" "$MIHOMO_CONFIG_PATH" 2>/dev/null | head -1 | sed 's/.*external-controller:\s*//' | tr -d '"' | tr -d "'" | xargs)
        [ -n "$controller" ] && MIHOMO_API_HOST="$controller"
    }
}

# Make API request
api_request() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    local url="http://$MIHOMO_API_HOST$endpoint"
    local curl_args=(-s)
    [ -n "$MIHOMO_SECRET" ] && curl_args+=(-H "Authorization: Bearer $MIHOMO_SECRET")

    if [ "$method" = "GET" ]; then
        curl "${curl_args[@]}" "$url"
    else
        curl "${curl_args[@]}" -X "$method" -H "Content-Type: application/json" "$url" ${data:+-d "$data"}
    fi
}

# Commands
cmd_status() {
    echo "=== Mihomo Status ==="
    echo "Config: $MIHOMO_CONFIG_PATH"
    echo "API: http://$MIHOMO_API_HOST"
    echo "Secret: ${MIHOMO_SECRET:+(set)}"
    echo ""
    
    # Try to get version
    local version=$(api_request GET "/version" 2>/dev/null | jq -r '.version // .meta // "unknown"' 2>/dev/null || echo "unknown")
    echo "Version: $version"

    # Check if running
    if api_request GET "/version" > /dev/null 2>&1; then
        echo "Status: ✅ Running"
    else
        echo "Status: ❌ Not responding"
    fi
}

cmd_proxies() {
    local format="${1:-table}"
    
    if [ "$format" = "json" ]; then
        api_request GET "/proxies" | jq .
    else
        # Table format
        api_request GET "/proxies" | jq -r '
            .proxies | to_entries[] 
            | select(.value.history | length > 0)
            | select(.key | test("^[🇦-🇿]|^[A-Z]"))
            | "\(.value.history[-1].delay)ms | \(.key)"
        ' 2>/dev/null | sort -n | head -30 || echo "Failed to fetch proxies"
    fi
}

cmd_groups() {
    api_request GET "/group" | jq -r '.proxies // [] | .[].name' 2>/dev/null || echo "Failed to fetch groups"
}

cmd_connections() {
    api_request GET "/connections" | jq '.connections // []' 2>/dev/null || echo "[]"
}

cmd_traffic() {
    echo "Traffic information (WebSocket stream):"
    echo "Use: curl -N http://$MIHOMO_API_HOST/traffic"
}

cmd_switch() {
    local group="$1"
    local proxy="$2"
    
    if [ -z "$group" ] || [ -z "$proxy" ]; then
        echo "Usage: mihomo-cli switch <group> <proxy>"
        echo ""
        echo "Available groups:"
        cmd_groups
        return 1
    fi
    
    # URL encode the proxy name
    local encoded_proxy=$(printf '%s' "$proxy" | jq -sRr @uri)
    
    api_request PUT "/proxies/${encoded_proxy}" '{"name":"'"$proxy"'"}' | jq .
}

cmd_test() {
    local proxy="${1:-}"
    local url="${2:-http://www.gstatic.com/generate_204}"
    
    if [ -z "$proxy" ]; then
        echo "Testing all proxies..."
        api_request GET "/proxies" | jq -r '
            .proxies | to_entries[] 
            | select(.value.history | length > 0)
            | "\(.value.history[-1].delay)ms | \(.key)"
        ' 2>/dev/null | sort -n | head -20
    else
        local encoded=$(printf '%s' "$proxy" | jq -sRr @uri)
        api_request GET "/proxies/${encoded}/delay?url=${url}&timeout=5000" | jq .
    fi
}

cmd_logs() {
    local level="${1:-info}"
    echo "Log stream (WebSocket):"
    echo "Use: curl -N 'http://$MIHOMO_API_HOST/logs?level=$level'"
}

cmd_flush() {
    local type="${1:-dns}"
    
    case "$type" in
        dns)
            api_request POST "/cache/dns/flush" | jq .
            ;;
        fakeip)
            api_request POST "/cache/fakeip/flush" | jq .
            ;;
        *)
            echo "Usage: mihomo-cli flush [dns|fakeip]"
            return 1
            ;;
    esac
}

cmd_restart() {
    api_request POST "/restart" | jq .
}

cmd_config() {
    api_request GET "/configs" | jq .
}

# Parse global options before commands
parse_opts() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -c|--config)
                MIHOMO_CONFIG_PATH="$2"
                shift 2
                ;;
            -h|--host)
                MIHOMO_API_HOST="$2"
                shift 2
                ;;
            -s|--secret)
                MIHOMO_SECRET="$2"
                shift 2
                ;;
            --)
                shift
                break
                ;;
            -*)
                echo "Unknown option: $1"
                echo "Usage: mihomo-cli [-c config] [-h host] [-s secret] <command> [args]"
                exit 1
                ;;
            *)
                break
                ;;
        esac
    done
    # Return remaining args as command
    echo "$@"
}

# Main
# Check if first arg looks like an option
if [[ "${1:-}" == -* ]]; then
    # Parse options and get remaining command
    remaining=$(parse_opts "$@")
    set -- $remaining
fi

# Auto-detect if not fully specified
[ -z "$MIHOMO_CONFIG_PATH" ] && detect_mihomo

case "${1:-status}" in
    status)
        cmd_status
        ;;
    proxies|nodes)
        cmd_proxies "${2:-table}"
        ;;
    groups)
        cmd_groups
        ;;
    connections|conns)
        cmd_connections
        ;;
    traffic)
        cmd_traffic
        ;;
    switch|select)
        cmd_switch "$2" "$3"
        ;;
    test|delay)
        cmd_test "$2" "$3"
        ;;
    logs)
        cmd_logs "$2"
        ;;
    flush)
        cmd_flush "$2"
        ;;
    restart)
        cmd_restart
        ;;
    config)
        cmd_config
        ;;
    help|--help|-h)
        cat << 'EOF'
Mihomo CLI Helper

Usage: mihomo-cli [options] <command> [args]

Options:
  -c, --config PATH   Specify config file path
  -h, --host HOST     Specify API host:port (default: 127.0.0.1:9090)
  -s, --secret SECRET Specify API secret

Environment:
  MIHOMO_CONFIG       Config file path
  MIHOMO_HOST         API host:port
  MIHOMO_SECRET       API secret

Commands:
  status              Show mihomo status and version
  proxies [format]    List all proxies (table|json)
  groups              List all proxy groups
  connections         List active connections
  traffic             Show traffic info endpoint
  switch <g> <p>      Switch group to proxy
  test [proxy]        Test proxy delay
  logs [level]        Show logs endpoint
  flush [type]        Flush cache (dns|fakeip)
  restart             Restart mihomo
  config              Show current config
  help                Show this help

Examples:
  mihomo-cli status
  mihomo-cli -c /etc/mihomo/config.yaml status
  mihomo-cli -s mysecret proxies
  mihomo-cli proxies
  mihomo-cli switch GLOBAL "🇭🇰 Hong Kong"
  mihomo-cli test "🇯🇵 Japan"
  mihomo-cli flush dns

Auto-detection:
  The script tries to auto-detect config from:
  1. Running mihomo/clash process arguments
  2. Common paths (ClashMac, mihomo, clash-verge)
  3. Standard config directories

EOF
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run 'mihomo-cli help' for usage"
        exit 1
        ;;
esac