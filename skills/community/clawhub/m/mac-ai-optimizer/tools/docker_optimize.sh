#!/bin/bash
# docker_optimize.sh - Optimize Docker Desktop resource limits
# Prevents Docker from consuming all available memory

set -e

echo "=============================="
echo "  Docker Optimization"
echo "=============================="
echo ""

DOCKER_SETTINGS="$HOME/Library/Group Containers/group.com.docker/settings-store.json"
DOCKER_SETTINGS_ALT="$HOME/Library/Group Containers/group.com.docker/settings.json"

# Detect total RAM
TOTAL_MEM=$(sysctl -n hw.memsize 2>/dev/null)
TOTAL_GB=$(echo "scale=0; $TOTAL_MEM / 1073741824" | bc)

echo "Total system RAM: ${TOTAL_GB}GB"

# Calculate optimal Docker limits based on RAM
if [ "$TOTAL_GB" -le 8 ]; then
    DOCKER_MEM=3072    # 3GB for 8GB systems
    DOCKER_CPU=2
    DOCKER_SWAP=1024   # 1GB swap
    echo "Detected: Low memory system (${TOTAL_GB}GB)"
    echo "Strategy: Conservative Docker limits"
elif [ "$TOTAL_GB" -le 16 ]; then
    DOCKER_MEM=6144    # 6GB for 16GB systems
    DOCKER_CPU=4
    DOCKER_SWAP=2048
    echo "Detected: Standard system (${TOTAL_GB}GB)"
    echo "Strategy: Balanced Docker limits"
else
    DOCKER_MEM=8192    # 8GB for 32GB+ systems
    DOCKER_CPU=4
    DOCKER_SWAP=2048
    echo "Detected: High memory system (${TOTAL_GB}GB)"
    echo "Strategy: Standard Docker limits"
fi

echo ""
echo "Recommended Docker settings:"
echo "  Memory: ${DOCKER_MEM}MB ($((DOCKER_MEM/1024))GB)"
echo "  CPUs: ${DOCKER_CPU}"
echo "  Swap: ${DOCKER_SWAP}MB ($((DOCKER_SWAP/1024))GB)"
echo ""

# Check if Docker is installed
if ! command -v docker &>/dev/null; then
    echo "Docker is not installed. Skipping Docker optimization."
    echo "Install Docker Desktop from https://docker.com and re-run."
    exit 0
fi

# Try to update Docker settings
SETTINGS_FILE=""
if [ -f "$DOCKER_SETTINGS" ]; then
    SETTINGS_FILE="$DOCKER_SETTINGS"
elif [ -f "$DOCKER_SETTINGS_ALT" ]; then
    SETTINGS_FILE="$DOCKER_SETTINGS_ALT"
fi

if [ -n "$SETTINGS_FILE" ]; then
    echo "Found Docker settings: $SETTINGS_FILE"
    echo ""
    echo "NOTE: Docker Desktop settings are best changed via the GUI:"
    echo "  Docker Desktop -> Settings -> Resources"
    echo ""
    echo "  Set Memory to: $((DOCKER_MEM/1024))GB"
    echo "  Set CPUs to: ${DOCKER_CPU}"
    echo "  Set Swap to: $((DOCKER_SWAP/1024))GB"
else
    echo "Docker settings file not found."
    echo "Open Docker Desktop -> Settings -> Resources and apply:"
    echo "  Memory: $((DOCKER_MEM/1024))GB"
    echo "  CPUs: ${DOCKER_CPU}"
    echo "  Swap: $((DOCKER_SWAP/1024))GB"
fi

# Docker system cleanup
echo ""
echo "Cleaning Docker unused resources..."
if docker system prune -f 2>/dev/null; then
    echo "  -> Unused containers, networks, and images removed"
else
    echo "  -> Docker not running or prune failed"
fi

# Show current Docker resource usage
echo ""
echo "Current Docker disk usage:"
docker system df 2>/dev/null || echo "  Docker not running"

echo ""
echo "=============================="
echo "  Docker optimization complete"
echo "=============================="
