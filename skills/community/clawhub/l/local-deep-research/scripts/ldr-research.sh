#!/bin/bash
#
# LDR Research CLI - Interface with Local Deep Research service
#
# REQUIRED BINARIES: curl, jq (declared in skill manifest requires.bins)
# EXPECTED ENV (declared in skill manifest requires.env / primaryEnv):
#   LDR_BASE_URL    - LDR service URL (default http://127.0.0.1:5000); only use a host you control
#   LDR_SERVICE_USER, LDR_SERVICE_PASSWORD (or LDR_USERNAME/LDR_PASSWORD) - when LDR auth is enabled
#
# Actions: start_research, get_status, get_result, poll_until_complete
#
# Authentication: LDR uses session-cookie auth with CSRF. This script:
#   1. GETs the login page to obtain session cookie and CSRF token
#   2. POSTs login form (username, password, CSRF) to establish session
#   3. Reuses the session cookie (and CSRF token for POSTs) for API calls
# Credentials are for local LDR only; never transmitted elsewhere.
#
# Optional: ~/.config/local_deep_research/config/.env is sourced if present (verify its contents).
#

set -e

# Load LDR's local .env if present (secrets stay local)
LDR_ENV="${LDR_CONFIG_DIR:-$HOME/.config/local_deep_research/config}/.env"
if [[ -f "$LDR_ENV" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "$LDR_ENV"
    set +a
fi

# Config
LDR_BASE_URL="${LDR_BASE_URL:-http://127.0.0.1:5000}"
LDR_USERNAME="${LDR_SERVICE_USER:-${LDR_USERNAME:-}}"
LDR_PASSWORD="${LDR_SERVICE_PASSWORD:-${LDR_PASSWORD:-}}"
LDR_DEFAULT_MODE="${LDR_DEFAULT_MODE:-detailed}"
LDR_DEFAULT_SEARCH_TOOL="${LDR_DEFAULT_SEARCH_TOOL:-auto}"
LDR_DEFAULT_LANGUAGE="${LDR_DEFAULT_LANGUAGE:-}"
# Login page URL (GET for form + CSRF; POST for submit). Adjust if LDR uses different path.
LDR_LOGIN_URL="${LDR_LOGIN_URL:-${LDR_BASE_URL}/auth/login}"

HTTP_TIMEOUT="${HTTP_TIMEOUT:-60}"
RETRY_COUNT="${RETRY_COUNT:-3}"
RETRY_DELAY="${RETRY_DELAY:-2}"

# Cookie jar for session; CSRF token stored after login
COOKIE_JAR=$(mktemp)
trap 'rm -f "$COOKIE_JAR"' EXIT
CSRF_TOKEN=""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
log_info() { echo -e "${GREEN}[INFO]${NC} $1" >&2; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Fetch login page to get session cookie and CSRF token; then POST credentials.
# LDR uses form-based login + CSRF (no HTTP Basic Auth).
login() {
    if [[ -z "$LDR_USERNAME" || -z "$LDR_PASSWORD" ]]; then
        return 0
    fi

    log_info "Logging in to LDR (session + CSRF)..."
    local login_page
    login_page=$(curl -s -c "$COOKIE_JAR" -b "$COOKIE_JAR" -L --max-time "$HTTP_TIMEOUT" "$LDR_LOGIN_URL" 2>/dev/null) || true
    if [[ -z "$login_page" ]]; then
        log_error "Could not fetch login page at $LDR_LOGIN_URL"
        return 1
    fi

    # Extract CSRF token from form (common: name="csrf_token" or "_csrf" or "csrf_token")
    CSRF_TOKEN=$(echo "$login_page" | sed -n 's/.*name="csrf_token"[^>]*value="\([^"]*\)".*/\1/p' | head -1)
    [[ -z "$CSRF_TOKEN" ]] && CSRF_TOKEN=$(echo "$login_page" | sed -n 's/.*name="_csrf"[^>]*value="\([^"]*\)".*/\1/p' | head -1)
    [[ -z "$CSRF_TOKEN" ]] && CSRF_TOKEN=$(echo "$login_page" | sed -n 's/.*value="\([^"]*\)"[^>]*name="csrf_token".*/\1/p' | head -1)
    if [[ -z "$CSRF_TOKEN" ]]; then
        log_warn "No CSRF token found on login page; POST may still work if LDR uses cookie-only CSRF"
    fi

    # POST login form (application/x-www-form-urlencoded)
    local post_data
    post_data="username=$(printf '%s' "$LDR_USERNAME" | jq -sRr @uri)&password=$(printf '%s' "$LDR_PASSWORD" | jq -sRr @uri)"
    [[ -n "$CSRF_TOKEN" ]] && post_data="csrf_token=$(printf '%s' "$CSRF_TOKEN" | jq -sRr @uri)&$post_data"

    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" -c "$COOKIE_JAR" -b "$COOKIE_JAR" -L --max-time "$HTTP_TIMEOUT" \
        -X POST \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "$post_data" \
        "$LDR_LOGIN_URL" 2>/dev/null) || true

    if [[ "$http_code" =~ ^2[0-9][0-9]$ ]] || [[ "$http_code" == "302" ]]; then
        log_info "Login successful (HTTP $http_code)"
        return 0
    fi
    log_error "Login failed (HTTP $http_code). Check URL and credentials."
    return 1
}

# Make authenticated request. Uses session cookie; for POST, sends CSRF if we have it.
http_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    local url="${LDR_BASE_URL}${endpoint}"

    local attempt=0
    while [[ $attempt -lt $RETRY_COUNT ]]; do
        local response http_code
        if [[ "$method" == "GET" ]]; then
            response=$(curl -s -w "\n%{http_code}" -b "$COOKIE_JAR" --max-time "$HTTP_TIMEOUT" "$url" 2>/dev/null)
        else
            if [[ -n "$CSRF_TOKEN" ]]; then
                response=$(curl -s -w "\n%{http_code}" -b "$COOKIE_JAR" -H "X-CSRFToken: $CSRF_TOKEN" --max-time "$HTTP_TIMEOUT" \
                    -H "Content-Type: application/json" -d "$data" -X POST "$url" 2>/dev/null)
            else
                response=$(curl -s -w "\n%{http_code}" -b "$COOKIE_JAR" --max-time "$HTTP_TIMEOUT" \
                    -H "Content-Type: application/json" -d "$data" -X POST "$url" 2>/dev/null)
            fi
        fi

        http_code=$(echo "$response" | tail -n1)
        local body=$(echo "$response" | sed '$d')

        if [[ "$http_code" == "302" ]] || [[ "$http_code" == "401" ]]; then
            log_warn "Session expired or unauthorized (HTTP $http_code), re-login..."
            login || { log_error "Re-login failed"; return 1; }
            attempt=$((attempt + 1))
            continue
        fi

        if [[ "$http_code" =~ ^2[0-9][0-9]$ ]]; then
            echo "$body"
            return 0
        fi
        if [[ "$http_code" =~ ^5[0-9][0-9]$ ]]; then
            attempt=$((attempt + 1))
            if [[ $attempt -lt $RETRY_COUNT ]]; then
                log_warn "Server error (HTTP $http_code), retrying in ${RETRY_DELAY}s..."
                sleep "$RETRY_DELAY"
                continue
            fi
        fi

        log_error "HTTP request failed with status $http_code"
        echo "$body"
        return 1
    done
    return 1
}

start_research() {
    local query="" mode="$LDR_DEFAULT_MODE" search_tool="$LDR_DEFAULT_SEARCH_TOOL" language="$LDR_DEFAULT_LANGUAGE" iterations="" questions_per_iteration=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --query) query="$2"; shift 2 ;;
            --mode) mode="$2"; shift 2 ;;
            --search_tool) search_tool="$2"; shift 2 ;;
            --language) language="$2"; shift 2 ;;
            --iterations) iterations="$2"; shift 2 ;;
            --questions_per_iteration) questions_per_iteration="$2"; shift 2 ;;
            *) log_error "Unknown argument: $1"; exit 1 ;;
        esac
    done

    if [[ -z "$query" ]]; then
        log_error "Missing required argument: --query"
        exit 1
    fi

    login || { log_error "Authentication failed"; exit 1; }

    local payload="{\"query\": \"$(echo "$query" | jq -sRr .)\", \"mode\": \"$mode\", \"search_tool\": \"$search_tool\""
    [[ -n "$language" ]] && payload="$payload, \"language\": \"$(echo "$language" | jq -sRr .)\""
    [[ -n "$iterations" ]] && payload="$payload, \"iterations\": $iterations"
    [[ -n "$questions_per_iteration" ]] && payload="$payload, \"questions_per_iteration\": $questions_per_iteration"
    payload="$payload}"

    log_info "Starting research: $query (mode: $mode, search_tool: $search_tool${language:+, language: $language})"
    local response
    response=$(http_request "POST" "/research/api/start" "$payload")
    if [[ $? -eq 0 ]]; then
        log_info "Research started successfully"
        echo "$response" | jq .
    else
        log_error "Failed to start research"
        echo "$response"
        exit 1
    fi
}

get_status() {
    local research_id=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --research_id) research_id="$2"; shift 2 ;;
            *) log_error "Unknown argument: $1"; exit 1 ;;
        esac
    done

    if [[ -z "$research_id" ]]; then
        log_error "Missing required argument: --research_id"
        exit 1
    fi

    log_info "Checking status for research: $research_id"
    login || true
    local response
    response=$(http_request "GET" "/research/api/status/${research_id}" "")
    if [[ $? -eq 0 ]]; then
        echo "$response" | jq .
    else
        log_error "Failed to get status"
        echo "$response"
        exit 1
    fi
}

get_result() {
    local research_id=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --research_id) research_id="$2"; shift 2 ;;
            *) log_error "Unknown argument: $1"; exit 1 ;;
        esac
    done

    if [[ -z "$research_id" ]]; then
        log_error "Missing required argument: --research_id"
        exit 1
    fi

    log_info "Fetching result for research: $research_id"
    login || true
    local response
    response=$(http_request "GET" "/research/api/report/${research_id}" "")
    if [[ $? -eq 0 ]]; then
        echo "$response" | jq .
    else
        log_error "Failed to get result"
        echo "$response"
        exit 1
    fi
}

poll_until_complete() {
    local research_id="" interval="${INTERVAL:-15}" max_wait="${MAX_WAIT:-1800}"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --research_id) research_id="$2"; shift 2 ;;
            --interval) interval="$2"; shift 2 ;;
            --max_wait) max_wait="$2"; shift 2 ;;
            *) log_error "Unknown argument: $1"; exit 1 ;;
        esac
    done

    if [[ -z "$research_id" ]]; then
        log_error "Missing required argument: --research_id"
        exit 1
    fi

    log_info "Polling research $research_id (interval: ${interval}s, max_wait: ${max_wait}s)"
    login || true
    local elapsed=0
    while [[ $elapsed -lt $max_wait ]]; do
        local status_response
        status_response=$(http_request "GET" "/research/api/status/${research_id}" "" 2>/dev/null)
        [[ $? -ne 0 ]] && { log_error "Failed to get status"; exit 1; }

        local state message progress
        state=$(echo "$status_response" | jq -r '.state // "unknown"')
        message=$(echo "$status_response" | jq -r '.message // ""')
        progress=$(echo "$status_response" | jq -r '.progress // "N/A"')

        log_info "Status: $state - $message (Progress: $progress%)"

        case "$state" in
            completed) log_info "Research completed!"; echo "$status_response"; return 0 ;;
            failed|timeout) log_error "Research $state"; echo "$status_response"; return 1 ;;
            pending|running) sleep "$interval"; elapsed=$((elapsed + interval)) ;;
            *) log_warn "Unknown state: $state"; sleep "$interval"; elapsed=$((elapsed + interval)) ;;
        esac
    done

    log_error "Max wait time ($max_wait seconds) exceeded"
    echo '{"state": "timeout", "message": "Max wait time exceeded"}' | jq .
    return 1
}

show_usage() {
    cat << EOF
LDR Research CLI - Local Deep Research service (session + CSRF auth)

Usage: $0 <action> [options]

Actions:
  start_research      Start a new research job
  get_status          Check status of a research job
  get_result          Fetch completed research report
  poll_until_complete Poll until research completes (blocking)

Options for start_research:
  --query <text>              Research query (required)
  --mode <quick|detailed>     quick = Quick Summary, detailed = Detailed Report (default: $LDR_DEFAULT_MODE)
  --search_tool <tool>        Search tool (default: $LDR_DEFAULT_SEARCH_TOOL)
  --language <code>           Output language, e.g. en, es, fr, de, zh, ja (default: $LDR_DEFAULT_LANGUAGE)
  --iterations <n>            Number of research cycles
  --questions_per_iteration <n> Questions per cycle

Options for get_status/get_result:
  --research_id <uuid>       Research job ID (required)

Options for poll_until_complete:
  --research_id <uuid>       Research job ID (required)
  --interval <seconds>        Polling interval (default: 15)
  --max_wait <seconds>       Maximum wait time (default: 1800)

Environment (credentials for local LDR only; session cookie + CSRF):
  LDR_BASE_URL              LDR service URL (default: http://127.0.0.1:5000)
  LDR_LOGIN_URL             Login page URL (default: \$LDR_BASE_URL/auth/login)
  LDR_SERVICE_USER          LDR account username (or LDR_USERNAME)
  LDR_SERVICE_PASSWORD      LDR account password (or LDR_PASSWORD)
  LDR_CONFIG_DIR            Dir containing .env (default: ~/.config/local_deep_research/config)
  LDR_DEFAULT_MODE          Default mode: quick | detailed
  LDR_DEFAULT_LANGUAGE       Default output language code (e.g. en, es, fr)

Examples:
  $0 start_research --query "quantum computing" --mode quick
  $0 start_research --query "AI trends" --mode detailed --language es
  $0 get_status --research_id abc-123
  $0 poll_until_complete --research_id abc-123 --interval 10
EOF
}

main() {
    [[ $# -lt 1 ]] && { show_usage; exit 1; }
    local action="$1"; shift
    case "$action" in
        start_research) start_research "$@" ;;
        get_status) get_status "$@" ;;
        get_result) get_result "$@" ;;
        poll_until_complete) poll_until_complete "$@" ;;
        help|--help|-h) show_usage ;;
        *) log_error "Unknown action: $action"; show_usage; exit 1 ;;
    esac
}

main "$@"
