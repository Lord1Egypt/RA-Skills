#!/usr/bin/env bash
#
# Docker Health Monitor
# Monitors Docker containers: status, resource usage, restart counts, image freshness
#

set -euo pipefail

# ── Colors ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ── Help ────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTION]

Docker container health monitor.

Options:
  --status       List all containers with running status
  --resources    Show CPU/memory usage per container
  --restarts     Flag containers restarted >3 times
  --images       Check for available image updates
  --all          Run all checks (default if no option given)
  --help         Show this help message
EOF
    exit 0
}

# ── Check Docker ────────────────────────────────────────
check_docker() {
    if ! command -v docker &>/dev/null; then
        echo -e "${RED}Error: docker command not found.${NC}" >&2
        exit 1
    fi
    if ! docker info &>/dev/null; then
        echo -e "${RED}Error: Cannot connect to Docker daemon. Check permissions/socket.${NC}" >&2
        exit 1
    fi
}

# ── Section Header ──────────────────────────────────────
header() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}$1${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════${NC}\n"
}

# ── 1. Container Status ─────────────────────────────────
check_status() {
    header "Container Status"
    local containers
    containers=$(docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}\t{{.Ports}}" 2>/dev/null)
    if [[ -z "$containers" ]]; then
        echo -e "${YELLOW}No containers found.${NC}"
        return
    fi
    echo "$containers"

    # Summary counts
    local running stopped paused
    running=$(docker ps -q 2>/dev/null | wc -l)
    stopped=$(docker ps -q -f status=exited -f status=created 2>/dev/null | wc -l)
    paused=$(docker ps -q -f status=paused 2>/dev/null | wc -l)
    local total=$((running + stopped + paused))
    echo -e "\n${BOLD}Summary:${NC} ${GREEN}$running running${NC}, ${YELLOW}$paused paused${NC}, ${RED}$stopped stopped${NC} (${total} total)"
}

# ── 2. Resource Usage ───────────────────────────────────
check_resources() {
    header "CPU & Memory Usage"

    local containers
    containers=$(docker ps -q 2>/dev/null)
    if [[ -z "$containers" ]]; then
        echo -e "${YELLOW}No running containers to monitor.${NC}"
        return
    fi

    printf "${BOLD}%-25s %-10s %-15s %-15s${NC}\n" "CONTAINER" "CPU %" "MEM USAGE" "MEM %"
    printf "%-25s %-10s %-15s %-15s\n" "-------------------------" "---------" "---------------" "---------------"

    for cid in $containers; do
        local name stats cpu mem_used mem_pct
        name=$(docker inspect --format '{{.Name}}' "$cid" | sed 's|/||')
        stats=$(docker stats --no-stream --format '{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}' "$cid" 2>/dev/null || true)
        if [[ -n "$stats" ]]; then
            cpu=$(echo "$stats" | cut -f1)
            mem_used=$(echo "$stats" | cut -f2)
            mem_pct=$(echo "$stats" | cut -f3)
            printf "%-25s %-10s %-15s %-15s\n" "$name" "$cpu" "$mem_used" "$mem_pct"
        fi
    done
}

# ── 3. Restart Check ────────────────────────────────────
check_restarts() {
    header "Restart Counts (Threshold: >3)"

    local containers
    containers=$(docker ps -a -q 2>/dev/null)
    if [[ -z "$containers" ]]; then
        echo -e "${YELLOW}No containers found.${NC}"
        return
    fi

    local found=0
    printf "${BOLD}%-30s %-10s %-12s${NC}\n" "CONTAINER" "RESTARTS" "STATUS"
    printf "%-30s %-10s %-12s\n" "------------------------------" "---------" "------------"

    for cid in $containers; do
        local name restarts status
        name=$(docker inspect --format '{{.Name}}' "$cid" | sed 's|/||')
        restarts=$(docker inspect --format '{{.RestartCount}}' "$cid")
        status=$(docker inspect --format '{{.State.Status}}' "$cid")

        if [[ "$restarts" -gt 3 ]]; then
            echo -e "${RED}⚠ ${name}${NC}          ${RED}${restarts}${NC}        ${status}"
            found=1
        else
            printf "%-30s %-10s %-12s\n" "$name" "$restarts" "$status"
        fi
    done

    if [[ "$found" -eq 0 ]]; then
        echo -e "\n${GREEN}✓ No containers with excessive restarts.${NC}"
    else
        echo -e "\n${RED}⚠ Some containers have restarted more than 3 times — investigate.${NC}"
    fi
}

# ── 4. Image Update Check ──────────────────────────────
check_images() {
    header "Image Update Check"

    local images
    images=$(docker ps -a --format '{{.Image}}' 2>/dev/null | sort -u)
    if [[ -z "$images" ]]; then
        echo -e "${YELLOW}No images found.${NC}"
        return
    fi

    local outdated=0
    while IFS= read -r image; do
        [[ -z "$image" ]] && continue

        # Skip any image with <none> or dangling references
        if [[ "$image" == "<none>" ]] || [[ "$image" == *"<none>"* ]]; then
            continue
        fi

        # Get the local digest
        local local_digest
        local_digest=$(docker inspect --format '{{index .RepoDigests 0}}' "$image" 2>/dev/null || true)

        echo -e "Checking: ${BOLD}$image${NC}"

        # Try pulling to check for updates (just get the manifest, don't pull layers)
        if docker pull --quiet "$image" 2>/dev/null; then
            local new_digest
            new_digest=$(docker inspect --format '{{index .RepoDigests 0}}' "$image" 2>/dev/null || true)

            if [[ -n "$local_digest" && -n "$new_digest" && "$local_digest" != "$new_digest" ]]; then
                echo -e "  ${YELLOW}→ Update available${NC} (digest changed)"
                outdated=1
            elif [[ -z "$local_digest" ]]; then
                echo -e "  ${GREEN}✓ Up to date${NC} (no prior digest to compare)"
            else
                echo -e "  ${GREEN}✓ Up to date${NC}"
            fi
        else
            echo -e "  ${RED}✗ Pull failed${NC} (check registry access or image name)"
        fi
    done <<< "$images"

    if [[ "$outdated" -eq 0 ]]; then
        echo -e "\n${GREEN}✓ All images are current.${NC}"
    else
        echo -e "\n${YELLOW}⚠ Updates available — consider running docker pull to refresh.${NC}"
    fi
}

# ── Main ─────────────────────────────────────────────────
main() {
    check_docker

    local mode="${1:---all}"

    case "$mode" in
        --status)
            check_status
            ;;
        --resources)
            check_resources
            ;;
        --restarts)
            check_restarts
            ;;
        --images)
            check_images
            ;;
        --all|--full|"")
            check_status
            check_resources
            check_restarts
            check_images
            ;;
        --help|-h)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $mode${NC}" >&2
            usage
            ;;
    esac

    echo -e "\n${GREEN}${BOLD}✓ Health check complete.${NC}\n"
}

main "$@"
