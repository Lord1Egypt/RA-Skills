#!/bin/bash
# Combined system stats - outputs clean format for quick health checks
# Usage: ./system-stats.sh

PLATFORM=$(uname -s)

echo "=== System Stats ==="
echo "Time: $(date)"
echo "Platform: $PLATFORM"
echo ""

if [ "$PLATFORM" = "Darwin" ]; then
    echo "--- CPU ---"
    top -l 1 -n 0 -s 0 | grep "CPU usage"
    echo ""
    
    echo "--- Memory ---"
    top -l 1 -n 0 | grep "PhysMem"
    vm_stat | head -5
    echo ""
    
    echo "--- Disk ---"
    df -h / | tail -1
    echo ""
    
    echo "--- Load Average ---"
    uptime
else
    echo "--- CPU ---"
    top -bn1 | head -5
    echo ""
    
    echo "--- Memory ---"
    free -h
    echo ""
    
    echo "--- Disk ---"
    df -h / | tail -1
    echo ""
    
    echo "--- Load Average ---"
    uptime
fi
