#!/bin/bash
#
# Job Status Query Script (Bash version)
# Queries HPC/AI computing job status by jobId
#

set -euo pipefail

# Configuration
BASE_URL="http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28"
TIMEOUT=30
VERBOSE=false

# Help information
usage() {
    cat << EOF
Job Status Query Script

Usage: $0 [options] <jobId>

Options:
    -j, --job-id ID     Specify job ID (required)
    -t, --timeout SEC   Request timeout in seconds (default: 30)
    -v, --verbose       Verbose output mode
    -h, --help         Show this help message

Examples:
    $0 --job-id 15000
    $0 -j 15000 -v
EOF
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -j|--job-id)
                JOB_ID="$2"
                shift 2
                ;;
            -t|--timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                if [[ -z "${JOB_ID:-}" ]]; then
                    JOB_ID="$1"
                    shift
                else
                    echo "Error: Unknown argument '$1'"
                    usage
                    exit 1
                fi
                ;;
        esac
    done
    
    # Validate required arguments
    if [[ -z "${JOB_ID:-}" ]]; then
        echo "Error: Job ID must be specified"
        usage
        exit 1
    fi
}

# Check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: Command '$1' not found, please install it first"
        exit 1
    fi
}

# Get job status
get_job_status() {
    local job_id="$1"
    local url="${BASE_URL}/${job_id}"
    local response_file
    local http_code
    local response
    
    response_file=$(mktemp)
    
    # Send HTTP request
    http_code=$(curl -s -w "%{http_code}" \
        -H "User-Agent: OpenClaw-JobStatus/1.0.0" \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        --max-time "$TIMEOUT" \
        -o "$response_file" \
        "$url")
    
    # Check HTTP status code
    if [[ "$http_code" != "200" ]]; then
        case "$http_code" in
            404)
                error_message="Job not found"
                ;;
            400)
                error_message="Bad request parameters"
                ;;
            500|502|503|504)
                error_message="Server error"
                ;;
            *)
                error_message="HTTP error: $http_code"
                ;;
        esac
        echo "{\"success\":false,\"jobId\":\"$job_id\",\"error\":\"$error_message\"}"
        rm -f "$response_file"
        return 1
    fi
    
    # Read response
    response=$(cat "$response_file")
    rm -f "$response_file"
    
    # Parse JSON (using jq)
    local code
    local message
    local data
    local job_state
    
    code=$(echo "$response" | jq -r '.code // empty')
    message=$(echo "$response" | jq -r '.message // empty')
    data=$(echo "$response" | jq -r '.data // {}')
    
    # Check return code
    if [[ "$code" != "0" ]]; then
        echo "{\"success\":false,\"jobId\":\"$job_id\",\"error\":\"API error: ${message:-unknown error}\"}"
        return 1
    fi
    
    # Extract jobState
    job_state=$(echo "$data" | jq -r '.jobState // empty')
    
    if [[ -z "$job_state" ]]; then
        echo "{\"success\":false,\"jobId\":\"$job_id\",\"error\":\"Job state field not found\"}"
        return 1
    fi
    
    # Build success response
    echo "$response" | jq -c \
        --arg jobId "$job_id" \
        --arg status "$job_state" \
        '{
            success: true,
            jobId: $jobId,
            status: $status,
            details: .data,
            message: (if $status == "COMPLETED" then "Job completed successfully"
                     elif $status == "RUNNING" then "Job is currently running"
                     elif $status == "FAILED" then "Job execution failed"
                     elif $status == "PENDING" then "Job is queued"
                     else "Job status: \($status)" end),
            timestamp: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
        }'
}

# Main function
main() {
    # Check required commands
    check_command curl
    check_command jq
    
    # Parse arguments
    parse_args "$@"
    
    # Get job status
    result=$(get_job_status "$JOB_ID" 2>/dev/null || true)
    
    # Output result
    if [[ "$VERBOSE" == true ]]; then
        echo "$result" | jq .
    else
        success=$(echo "$result" | jq -r '.success // false')
        
        if [[ "$success" == "true" ]]; then
            status=$(echo "$result" | jq -r '.status // "UNKNOWN"')
            message=$(echo "$result" | jq -r '.message // ""')
            echo "Job $JOB_ID Status: $status"
            echo "$message"
            
            # Show end time if available
            end_time=$(echo "$result" | jq -r '.details.endTime // empty')
            if [[ -n "$end_time" ]]; then
                echo "End Time: $end_time"
            fi
        else
            error=$(echo "$result" | jq -r '.error // "Unknown error"')
            echo "Error: $error"
            exit 1
        fi
    fi
}

# Run main function
main "$@"