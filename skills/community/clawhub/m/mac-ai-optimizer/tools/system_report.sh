#!/bin/bash
# system_report.sh - Show current system resource usage
# Safe to run anytime, read-only

echo "=============================="
echo "  Mac AI Optimizer - System Report"
echo "=============================="
echo ""

# Memory info
echo "--- Memory ---"
memory_pressure=$(memory_pressure 2>/dev/null | grep "System-wide memory free percentage" || echo "N/A")
vm_stat_output=$(vm_stat 2>/dev/null)

total_mem=$(sysctl -n hw.memsize 2>/dev/null)
if [ -n "$total_mem" ]; then
    total_gb=$(echo "scale=1; $total_mem / 1073741824" | bc)
    echo "Total RAM: ${total_gb}GB"
fi

# Parse vm_stat for used memory
if [ -n "$vm_stat_output" ]; then
    page_size=$(vm_stat | head -1 | grep -o '[0-9]*')
    pages_active=$(echo "$vm_stat_output" | grep "Pages active" | awk '{print $3}' | tr -d '.')
    pages_wired=$(echo "$vm_stat_output" | grep "Pages wired" | awk '{print $4}' | tr -d '.')
    pages_compressed=$(echo "$vm_stat_output" | grep "Pages occupied by compressor" | awk '{print $5}' | tr -d '.')

    if [ -n "$pages_active" ] && [ -n "$pages_wired" ]; then
        used_bytes=$(( (pages_active + pages_wired + pages_compressed) * page_size ))
        used_gb=$(echo "scale=2; $used_bytes / 1073741824" | bc)
        echo "Used RAM: ${used_gb}GB"
        if [ -n "$total_mem" ]; then
            free_gb=$(echo "scale=2; $total_gb - $used_gb" | bc)
            echo "Available: ~${free_gb}GB"
        fi
    fi
fi
echo "$memory_pressure"

echo ""
echo "--- CPU ---"
sysctl -n machdep.cpu.brand_string 2>/dev/null
echo "CPU cores: $(sysctl -n hw.ncpu 2>/dev/null)"
echo "Load average: $(sysctl -n vm.loadavg 2>/dev/null)"

echo ""
echo "--- Swap ---"
sysctl -n vm.swapusage 2>/dev/null

echo ""
echo "--- Disk ---"
df -h / 2>/dev/null | tail -1 | awk '{print "Disk used: "$3" / "$2" ("$5" used)"}'

echo ""
echo "--- Background Services ---"
agent_count=$(launchctl list 2>/dev/null | wc -l | tr -d ' ')
echo "LaunchAgent/Daemon count: $agent_count"

echo ""
echo "--- Key Services Status ---"
# Spotlight
mdutil_status=$(mdutil -s / 2>/dev/null | grep "Indexing" || echo "Unknown")
echo "Spotlight: $mdutil_status"

# Docker
if pgrep -x "Docker" > /dev/null 2>&1; then
    echo "Docker: Running"
    docker_mem=$(ps aux | grep -i "[D]ocker" | awk '{sum+=$6} END {printf "%.0fMB", sum/1024}')
    echo "Docker memory: $docker_mem"
else
    echo "Docker: Not running"
fi

echo ""
echo "--- Top Memory Consumers ---"
ps aux --sort=-%mem 2>/dev/null | head -11 || ps aux | sort -nrk 4 | head -10
echo ""
echo "=============================="
echo "Run 'full_optimize' to optimize this Mac for AI workloads"
echo "=============================="
