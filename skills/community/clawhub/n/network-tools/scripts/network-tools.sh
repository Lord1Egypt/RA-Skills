#!/bin/bash

# Enhanced Network Tools Skill for AI Agents
# No API keys required - uses only local command-line tools

set -euo pipefail

PROXY_HOST="127.0.0.1"
PROXY_PORT="9050"
PROXY_URL="socks5://${PROXY_HOST}:${PROXY_PORT}"

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $*" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

# Check if a tool is available
tool_available() {
    command -v "$1" >/dev/null 2>&1
}

# Get user agent string
get_user_agent() {
    local agents=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        "curl/8.5.0"
        "wget/1.21.4"
    )
    echo "${agents[$((RANDOM % ${#agents[@]}))]}"
}

# Common curl options
get_curl_opts() {
    local opts=(--silent --show-error --max-time 30 --location --compressed)
    opts+=(--user-agent "$(get_user_agent)")
    echo "${opts[@]}"
}

# Common wget options
get_wget_opts() {
    local opts=(--quiet --timeout=30 --tries=3 --user-agent="$(get_user_agent)")
    echo "${opts[@]}"
}

# Fetch URL with specified tool
fetch_with_tool() {
    local tool="$1"
    local url="$2"
    local use_proxy="${3:-false}"
    local output_file="${4:-}"
    
    case "$tool" in
        "curl")
            local opts=($(get_curl_opts))
            if [ "$use_proxy" = "true" ]; then
                opts+=(--proxy "$PROXY_URL")
                log_info "Using proxy: $PROXY_URL"
            fi
            if [ -n "$output_file" ]; then
                opts+=(--output "$output_file")
            fi
            curl "${opts[@]}" "$url"
            ;;
        "wget")
            local opts=($(get_wget_opts))
            if [ "$use_proxy" = "true" ]; then
                export http_proxy="$PROXY_URL"
                export https_proxy="$PROXY_URL"
                log_info "Using proxy: $PROXY_URL"
            fi
            if [ -n "$output_file" ]; then
                opts+=(--output-document="$output_file")
            fi
            wget "${opts[@]}" "$url"
            local result=$?
            unset http_proxy https_proxy
            return $result
            ;;
        "httpie")
            local opts=(--timeout=30 --headers --body)
            if [ "$use_proxy" = "true" ]; then
                export HTTP_PROXY="$PROXY_URL"
                export HTTPS_PROXY="$PROXY_URL"
                log_info "Using proxy: $PROXY_URL"
            fi
            http "${opts[@]}" "$url"
            local result=$?
            unset HTTP_PROXY HTTPS_PROXY
            return $result
            ;;
        *)
            log_error "Unsupported tool: $tool"
            return 1
            ;;
    esac
}

# Intelligent tool selection based on content type and size
select_best_tool() {
    local url="$1"
    local content_type=""
    local file_size=0
    
    # Try to get content info first
    if tool_available curl; then
        content_type=$(curl --silent --head --max-time 10 "$url" | grep -i "content-type" | head -1 | cut -d: -f2- | tr -d '[:space:]' || echo "")
        file_size=$(curl --silent --head --max-time 10 "$url" | grep -i "content-length" | head -1 | cut -d: -f2- | tr -d '[:space:]' || echo "0")
    fi
    
    # For large files (>10MB), prefer aria2 if available
    if [ "$file_size" -gt 10485760 ] && tool_available aria2c; then
        echo "aria2"
        return
    fi
    
    # For JSON APIs, prefer httpie if available
    if [[ "$content_type" == *"application/json"* ]] && tool_available httpie; then
        echo "httpie"
        return
    fi
    
    # Default to curl if available, otherwise wget
    if tool_available curl; then
        echo "curl"
    elif tool_available wget; then
        echo "wget"
    else
        echo "none"
    fi
}

# Handle fetch command
handle_fetch() {
    local use_proxy="false"
    local tool=""
    local url=""
    local headers=()
    
    while [ $# -gt 0 ]; do
        case "$1" in
            "--proxy")
                use_proxy="true"
                shift
                ;;
            "--tool")
                tool="$2"
                shift 2
                ;;
            "--header"|"-H")
                headers+=("$2")
                shift 2
                ;;
            *)
                url="$1"
                shift
                ;;
        esac
    done
    
    if [ -z "$url" ]; then
        log_error "URL required"
        exit 1
    fi
    
    # Validate URL format
    if ! [[ "$url" =~ ^https?:// ]]; then
        log_error "Invalid URL format. Must start with http:// or https://"
        exit 1
    fi
    
    # Auto-select tool if not specified
    if [ -z "$tool" ]; then
        tool=$(select_best_tool "$url")
        if [ "$tool" = "none" ]; then
            log_error "No network tools available (curl, wget, or httpie required)"
            exit 1
        fi
        log_info "Auto-selected tool: $tool"
    elif ! tool_available "$tool" && [ "$tool" != "aria2" ]; then
        log_error "Tool '$tool' not available"
        exit 1
    fi
    
    # Handle aria2 separately for downloads
    if [ "$tool" = "aria2" ]; then
        handle_download_aria2 "$url" "$use_proxy"
        return
    fi
    
    fetch_with_tool "$tool" "$url" "$use_proxy"
}

# Handle download command with enhanced features
handle_download() {
    local use_proxy="false"
    local tool=""
    local output_file=""
    local url=""
    local resume=false
    
    while [ $# -gt 0 ]; do
        case "$1" in
            "--proxy")
                use_proxy="true"
                shift
                ;;
            "--tool")
                tool="$2"
                shift 2
                ;;
            "--output"|"-o")
                output_file="$2"
                shift 2
                ;;
            "--resume"|"-c")
                resume=true
                shift
                ;;
            *)
                url="$1"
                shift
                ;;
        esac
    done
    
    if [ -z "$url" ]; then
        log_error "URL required"
        exit 1
    fi
    
    # Validate URL format
    if ! [[ "$url" =~ ^https?:// ]]; then
        log_error "Invalid URL format. Must start with http:// or https://"
        exit 1
    fi
    
    # Generate output filename if not provided
    if [ -z "$output_file" ]; then
        output_file=$(basename "$url" | cut -d'?' -f1 | cut -d'#' -f1)
        if [ -z "$output_file" ] || [ "$output_file" = "." ] || [ "$output_file" = ".." ]; then
            output_file="downloaded-file-$(date +%s)"
        fi
    fi
    
    # Auto-select tool for download
    if [ -z "$tool" ]; then
        if tool_available aria2c; then
            tool="aria2"
        elif tool_available axel; then
            tool="axel"
        elif tool_available wget; then
            tool="wget"
        elif tool_available curl; then
            tool="curl"
        else
            log_error "No download tools available"
            exit 1
        fi
        log_info "Auto-selected download tool: $tool"
    fi
    
    case "$tool" in
        "aria2")
            handle_download_aria2 "$url" "$use_proxy" "$output_file" "$resume"
            ;;
        "axel")
            handle_download_axel "$url" "$use_proxy" "$output_file" "$resume"
            ;;
        "wget")
            handle_download_wget "$url" "$use_proxy" "$output_file" "$resume"
            ;;
        "curl")
            handle_download_curl "$url" "$use_proxy" "$output_file" "$resume"
            ;;
        *)
            log_error "Unsupported download tool: $tool"
            exit 1
            ;;
    esac
    
    log_info "Downloaded to: $output_file"
}

# Aria2 download handler
handle_download_aria2() {
    local url="$1"
    local use_proxy="${2:-false}"
    local output_file="${3:-}"
    local resume="${4:-false}"
    
    local opts=(-x 16 -s 16 --summary-interval=0 --console-log-level=warn)
    
    if [ "$use_proxy" = "true" ]; then
        opts+=(--all-proxy="$PROXY_URL")
        log_info "Using proxy: $PROXY_URL"
    fi
    
    if [ -n "$output_file" ]; then
        opts+=(--out="$output_file")
    fi
    
    if [ "$resume" = "true" ] && [ -f "$output_file" ]; then
        opts+=(--continue=true)
    fi
    
    aria2c "${opts[@]}" "$url"
}

# Axel download handler
handle_download_axel() {
    local url="$1"
    local use_proxy="${2:-false}"
    local output_file="${3:-}"
    local resume="${4:-false}"
    
    local opts=(-n 10 -q)
    
    if [ -n "$output_file" ]; then
        opts+=(-o "$output_file")
    fi
    
    # Note: Axel doesn't support SOCKS proxy directly, so we'll use environment variables
    if [ "$use_proxy" = "true" ]; then
        export http_proxy="$PROXY_URL"
        export https_proxy="$PROXY_URL"
        log_info "Using proxy: $PROXY_URL"
    fi
    
    axel "${opts[@]}" "$url"
    local result=$?
    unset http_proxy https_proxy
    return $result
}

# Wget download handler
handle_download_wget() {
    local url="$1"
    local use_proxy="${2:-false}"
    local output_file="${3:-}"
    local resume="${4:-false}"
    
    local opts=($(get_wget_opts))
    
    if [ "$use_proxy" = "true" ]; then
        export http_proxy="$PROXY_URL"
        export https_proxy="$PROXY_URL"
        log_info "Using proxy: $PROXY_URL"
    fi
    
    if [ -n "$output_file" ]; then
        opts+=(--output-document="$output_file")
    fi
    
    if [ "$resume" = "true" ]; then
        opts+=(--continue)
    fi
    
    wget "${opts[@]}" "$url"
    local result=$?
    unset http_proxy https_proxy
    return $result
}

# Curl download handler
handle_download_curl() {
    local url="$1"
    local use_proxy="${2:-false}"
    local output_file="${3:-}"
    local resume="${4:-false}"
    
    local opts=($(get_curl_opts))
    
    if [ "$use_proxy" = "true" ]; then
        opts+=(--proxy "$PROXY_URL")
        log_info "Using proxy: $PROXY_URL"
    fi
    
    if [ -n "$output_file" ]; then
        opts+=(--output "$output_file")
    fi
    
    if [ "$resume" = "true" ] && [ -f "$output_file" ]; then
        opts+=(--continue-at -)
    fi
    
    curl "${opts[@]}" "$url"
}

# DNS lookup functionality
handle_dns() {
    local record_type="A"
    local domain=""
    
    while [ $# -gt 0 ]; do
        case "$1" in
            "--type"|"-t")
                record_type="$2"
                shift 2
                ;;
            *)
                domain="$1"
                shift
                ;;
        esac
    done
    
    if [ -z "$domain" ]; then
        log_error "Domain required"
        exit 1
    fi
    
    if tool_available dig; then
        dig +short "$record_type" "$domain"
    elif tool_available nslookup; then
        nslookup -type="$record_type" "$domain"
    else
        log_error "No DNS tools available (dig or nslookup required)"
        exit 1
    fi
}

# Ping functionality
handle_ping() {
    local count=4
    local host=""
    
    while [ $# -gt 0 ]; do
        case "$1" in
            "--count"|"-c")
                count="$2"
                shift 2
                ;;
            *)
                host="$1"
                shift
                ;;
        esac
    done
    
    if [ -z "$host" ]; then
        log_error "Host required"
        exit 1
    fi
    
    if tool_available ping; then
        ping -c "$count" "$host"
    else
        log_error "Ping command not available"
        exit 1
    fi
}

# Traceroute functionality
handle_traceroute() {
    local host="$1"
    
    if [ -z "$host" ]; then
        log_error "Host required"
        exit 1
    fi
    
    if tool_available traceroute; then
        traceroute "$host"
    elif tool_available mtr; then
        mtr --report "$host"
    else
        log_error "No traceroute tools available (traceroute or mtr required)"
        exit 1
    fi
}

# Whois functionality
handle_whois() {
    local domain="$1"
    
    if [ -z "$domain" ]; then
        log_error "Domain required"
        exit 1
    fi
    
    if tool_available whois; then
        whois "$domain"
    else
        log_error "Whois command not available"
        exit 1
    fi
}

# IP information
handle_ipinfo() {
    local use_proxy="false"
    
    while [ $# -gt 0 ]; do
        case "$1" in
            "--proxy")
                use_proxy="true"
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    # Try multiple IP info services
    local services=(
        "https://api.ipify.org"
        "https://icanhazip.com"
        "https://ipecho.net/plain"
        "https://ident.me"
    )
    
    for service in "${services[@]}"; do
        if tool_available curl; then
            if fetch_with_tool "curl" "$service" "$use_proxy" >/dev/null 2>&1; then
                fetch_with_tool "curl" "$service" "$use_proxy"
                return 0
            fi
        elif tool_available wget; then
            if fetch_with_tool "wget" "$service" "$use_proxy" >/dev/null 2>&1; then
                fetch_with_tool "wget" "$service" "$use_proxy"
                return 0
            fi
        fi
    done
    
    log_error "Failed to get IP information from all services"
    exit 1
}

# List available tools
handle_tools() {
    echo "Available network tools:"
    echo "  Core HTTP clients:"
    if tool_available curl; then echo "    ✓ curl"; else echo "    ✗ curl"; fi
    if tool_available wget; then echo "    ✓ wget"; else echo "    ✗ wget"; fi
    if tool_available httpie; then echo "    ✓ httpie"; else echo "    ✗ httpie"; fi
    
    echo "  Download accelerators:"
    if tool_available aria2c; then echo "    ✓ aria2"; else echo "    ✗ aria2"; fi
    if tool_available axel; then echo "    ✓ axel"; else echo "    ✗ axel"; fi
    
    echo "  Network diagnostics:"
    if tool_available dig; then echo "    ✓ dig"; else echo "    ✗ dig"; fi
    if tool_available nslookup; then echo "    ✓ nslookup"; else echo "    ✗ nslookup"; fi
    if tool_available ping; then echo "    ✓ ping"; else echo "    ✗ ping"; fi
    if tool_available traceroute; then echo "    ✓ traceroute"; else echo "    ✗ traceroute"; fi
    if tool_available mtr; then echo "    ✓ mtr"; else echo "    ✗ mtr"; fi
    if tool_available whois; then echo "    ✓ whois"; else echo "    ✗ whois"; fi
    
    echo "  Media tools:"
    if tool_available youtube-dl; then echo "    ✓ youtube-dl"; else echo "    ✗ youtube-dl"; fi
    if tool_available ffmpeg; then echo "    ✓ ffmpeg"; else echo "    ✗ ffmpeg"; fi
}

# YouTube/media download
handle_media() {
    local use_proxy="false"
    local output_format=""
    local url=""
    
    while [ $# -gt 0 ]; do
        case "$1" in
            "--proxy")
                use_proxy="true"
                shift
                ;;
            "--format"|"-f")
                output_format="$2"
                shift 2
                ;;
            *)
                url="$1"
                shift
                ;;
        esac
    done
    
    if [ -z "$url" ]; then
        log_error "URL required"
        exit 1
    fi
    
    if ! tool_available youtube-dl; then
        log_error "youtube-dl not available"
        exit 1
    fi
    
    local opts=(--no-warnings --no-playlist)
    
    if [ "$use_proxy" = "true" ]; then
        opts+=(--proxy "$PROXY_URL")
        log_info "Using proxy: $PROXY_URL"
    fi
    
    if [ -n "$output_format" ]; then
        opts+=(--format "$output_format")
    fi
    
    youtube-dl "${opts[@]}" "$url"
}

# Help command
handle_help() {
    cat << EOF
Enhanced Network Tools Skill for AI Agents

Commands:
  fetch [--proxy] [--tool TOOL] [--header HEADER] URL
      Fetch content from URL with intelligent tool selection
  
  download [--proxy] [--tool TOOL] [--output FILE] [--resume] URL
      Download file with resume support and multiple tool options
  
  dns [--type TYPE] DOMAIN
      DNS lookup (A, AAAA, MX, TXT, etc.)
  
  ping [--count NUM] HOST
      Ping a host
  
  traceroute HOST
      Trace network route to host
  
  whois DOMAIN
      Domain registration information
  
  ipinfo [--proxy]
      Get public IP address
  
  media [--proxy] [--format FORMAT] URL
      Download media from supported sites (YouTube, etc.)
  
  tools
      List all available network tools

Available tools: curl, wget, httpie, aria2, axel, dig, nslookup, ping, 
traceroute, mtr, whois, youtube-dl, ffmpeg

Examples:
  network-tools fetch https://api.example.com/data
  network-tools download --proxy -o large-file.zip https://example.com/file.zip
  network-tools dns --type MX google.com
  network-tools ipinfo --proxy
  network-tools media -f mp4 https://youtube.com/watch?v=example

EOF
}

# Main dispatcher
if [ $# -eq 0 ]; then
    handle_help
    exit 0
fi

command="$1"
shift

case "$command" in
    "fetch")
        handle_fetch "$@"
        ;;
    "download")
        handle_download "$@"
        ;;
    "dns")
        handle_dns "$@"
        ;;
    "ping")
        handle_ping "$@"
        ;;
    "traceroute")
        handle_traceroute "$@"
        ;;
    "whois")
        handle_whois "$@"
        ;;
    "ipinfo")
        handle_ipinfo "$@"
        ;;
    "media")
        handle_media "$@"
        ;;
    "tools")
        handle_tools
        ;;
    "help")
        handle_help
        ;;
    *)
        log_error "Unknown command: $command"
        handle_help
        exit 1
        ;;
esac