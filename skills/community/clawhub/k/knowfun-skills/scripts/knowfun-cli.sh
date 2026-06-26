#!/bin/bash
# Knowfun.io CLI Helper Script
# A standalone CLI tool for interacting with the Knowfun.io API
#
# Copyright (c) 2026 Knowfun.io
# Licensed under the MIT License

set -e

# Configuration
BASE_URL="https://api.knowfun.io"
API_KEY="${KNOWFUN_API_KEY}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_error() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

check_api_key() {
    if [ -z "$API_KEY" ]; then
        print_error "KNOWFUN_API_KEY environment variable is not set"
        echo "Please set it with: export KNOWFUN_API_KEY='kf_your_api_key'"
        exit 1
    fi
}

check_jq() {
    if ! command -v jq &> /dev/null; then
        print_warning "jq is not installed. Output will be raw JSON."
        print_info "Install jq for better formatting: brew install jq"
    fi
}

format_json() {
    if command -v jq &> /dev/null; then
        jq '.'
    else
        cat
    fi
}

# Command: create
cmd_create() {
    local task_type="$1"
    shift
    local material="$*"

    if [ -z "$task_type" ] || [ -z "$material" ]; then
        print_error "Usage: knowfun-cli.sh create <course|poster|game|film> <text or url>"
        exit 1
    fi

    # Generate unique request ID
    local request_id="req_$(date +%s)_$(uuidgen | head -c 8)"

    # Determine if material is URL or text
    local material_type="text"
    local material_field="text"
    if [[ "$material" =~ ^https?:// ]]; then
        material_type="url"
        material_field="url"
    fi

    print_info "Creating $task_type task..."
    print_info "Request ID: $request_id"

    local response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/openapi/v1/tasks" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"requestId\": \"$request_id\",
            \"taskType\": \"$task_type\",
            \"material\": {
                \"$material_field\": \"$material\",
                \"type\": \"$material_type\"
            }
        }")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "Task created successfully!"
        echo "$body" | format_json

        if command -v jq &> /dev/null; then
            local task_id=$(echo "$body" | jq -r '.data.taskId')
            echo ""
            print_info "Check status with: $0 status $task_id"
        fi
    else
        print_error "Failed to create task (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: status
cmd_status() {
    local task_id="$1"

    if [ -z "$task_id" ]; then
        print_error "Usage: knowfun-cli.sh status <taskId>"
        exit 1
    fi

    print_info "Fetching task status..."

    local response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/openapi/v1/tasks/$task_id" \
        -H "Authorization: Bearer $API_KEY")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        if command -v jq &> /dev/null; then
            local status=$(echo "$body" | jq -r '.data.status')
            local progress=$(echo "$body" | jq -r '.data.progress')

            echo "📊 Task Status"
            echo "=============="
            echo "Task ID: $task_id"
            echo "Status: $status"
            echo "Progress: $progress%"
            echo ""

            if [ "$status" = "completed" ] || [ "$status" = "success" ]; then
                print_success "Task completed!"
                print_info "Get details with: $0 detail $task_id"
            elif [ "$status" = "failed" ]; then
                print_error "Task failed"
            else
                print_info "Task is still processing..."
            fi
        else
            echo "$body"
        fi
    else
        print_error "Failed to fetch task status (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: detail
cmd_detail() {
    local task_id="$1"
    local verbose="${2:-false}"

    if [ -z "$task_id" ]; then
        print_error "Usage: knowfun-cli.sh detail <taskId> [verbose]"
        exit 1
    fi

    print_info "Fetching task details..."

    local url="$BASE_URL/api/openapi/v1/tasks/$task_id/detail"
    if [ "$verbose" = "verbose" ]; then
        url="$url?verbose=true"
    fi

    local response=$(curl -s -w "\n%{http_code}" -X GET "$url" \
        -H "Authorization: Bearer $API_KEY")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        if command -v jq &> /dev/null; then
            local status=$(echo "$body" | jq -r '.data.status')
            local task_type=$(echo "$body" | jq -r '.data.taskType')

            echo "📄 Task Details"
            echo "==============="
            echo "$body" | jq '.data'
        else
            echo "$body"
        fi
    else
        print_error "Failed to fetch task details (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: list
cmd_list() {
    local limit="${1:-20}"
    local offset="${2:-0}"

    print_info "Fetching task list..."

    local response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/openapi/v1/tasks?limit=$limit&offset=$offset" \
        -H "Authorization: Bearer $API_KEY")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "Task list retrieved"
        echo "$body" | format_json
    else
        print_error "Failed to fetch task list (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: credits
cmd_credits() {
    print_info "Fetching credit balance..."

    local response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/openapi/v1/credits/balance" \
        -H "Authorization: Bearer $API_KEY")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        if command -v jq &> /dev/null; then
            local available=$(echo "$body" | jq -r '.data.available')
            local earned=$(echo "$body" | jq -r '.data.earned')
            local used=$(echo "$body" | jq -r '.data.used')
            local locked=$(echo "$body" | jq -r '.data.locked')

            echo "💰 Credit Balance"
            echo "================="
            echo "Available: $available credits"
            echo "Earned: $earned credits"
            echo "Used: $used credits"
            echo "Locked: $locked credits"
        else
            echo "$body"
        fi
    else
        print_error "Failed to fetch credit balance (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: pricing
cmd_pricing() {
    print_info "Fetching pricing information..."

    local response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/openapi/v1/credits/pricing" \
        -H "Authorization: Bearer $API_KEY")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "Pricing information"
        echo "$body" | format_json
    else
        print_error "Failed to fetch pricing (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: schema
cmd_schema() {
    print_info "Fetching configuration schema..."

    local response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/openapi/v1/schema")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "Configuration schema"
        echo "$body" | format_json
    else
        print_error "Failed to fetch schema (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: usage
cmd_usage() {
    local page="${1:-1}"
    local page_size="${2:-10}"

    print_info "Fetching usage statistics..."

    local response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/openapi/usage?page=$page&pageSize=$page_size" \
        -H "Authorization: Bearer $API_KEY")

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 200 ]; then
        print_success "Usage statistics"
        echo "$body" | format_json
    else
        print_error "Failed to fetch usage (HTTP $http_code)"
        echo "$body" | format_json
        exit 1
    fi
}

# Command: help
cmd_help() {
    cat << EOF
Knowfun.io CLI Tool

Usage:
    $0 <command> [arguments]

Commands:
    create <type> <text|url>   Create a new task
                                Types: course, poster, game, film
    status <taskId>             Check task status
    detail <taskId> [verbose]   Get detailed task information
    list [limit] [offset]       List tasks (default: 20 tasks, offset 0)
    credits                     Check credit balance
    pricing                     Get pricing information
    schema                      Get configuration schema
    usage [page] [pageSize]     Get usage statistics
    help                        Show this help message

Examples:
    $0 create course "Introduction to Python"
    $0 create poster https://example.com/document.pdf
    $0 status c3199fb3-350b-4981-858d-09b949bfae88
    $0 detail c3199fb3-350b-4981-858d-09b949bfae88
    $0 list 10
    $0 credits
    $0 pricing
    $0 schema

Environment:
    KNOWFUN_API_KEY    Your Knowfun.io API key (required)

Get your API key at: https://knowfun.io/api-platform
EOF
}

# Main script
main() {
    local command="$1"
    shift || true

    # Special case: no arguments or help
    if [ -z "$command" ] || [ "$command" = "help" ] || [ "$command" = "-h" ] || [ "$command" = "--help" ]; then
        cmd_help
        exit 0
    fi

    # Schema command doesn't require API key
    if [ "$command" = "schema" ]; then
        check_jq
        cmd_schema
        exit 0
    fi

    # All other commands require API key
    check_api_key
    check_jq

    case "$command" in
        create)
            cmd_create "$@"
            ;;
        status)
            cmd_status "$@"
            ;;
        detail)
            cmd_detail "$@"
            ;;
        list)
            cmd_list "$@"
            ;;
        credits)
            cmd_credits "$@"
            ;;
        pricing)
            cmd_pricing "$@"
            ;;
        usage)
            cmd_usage "$@"
            ;;
        *)
            print_error "Unknown command: $command"
            echo ""
            cmd_help
            exit 1
            ;;
    esac
}

main "$@"
