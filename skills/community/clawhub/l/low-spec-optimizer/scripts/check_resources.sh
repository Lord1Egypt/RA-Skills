#!/bin/bash
# check_resources.sh — Quick system resource check for low-spec machines
# Output: JSON with RAM, CPU, disk, swap status

set -euo pipefail

# RAM
read -r total used free <<< "$(free -m | awk '/^Mem:/ {print $2, $3, $7}')"
ram_pct=$(( used * 100 / total ))

# Swap
swap_total=0; swap_used=0
read -r swap_total swap_used <<< "$(free -m | awk '/^Swap:/ {print $2, $3}')"
swap_total=${swap_total:-0}
swap_used=${swap_used:-0}
if [ "$swap_total" -gt 0 ]; then
  swap_pct=$(( swap_used * 100 / swap_total ))
else
  swap_pct=0
fi

# CPU load (1-min avg / cores)
cores=$(nproc)
load_1m=$(awk '{print $1}' /proc/loadavg)
cpu_pct=$(awk -v l="$load_1m" -v c="$cores" 'BEGIN {p=(l/c)*100; if(p<0)p=0; if(p>100)p=100; printf "%.0f", p}')

# Disk (root partition)
read -r disk_total disk_used disk_pct <<< "$(df -h / | awk 'NR==2 {gsub(/%/,""); print $2, $3, $5}')"

# Top 5 memory consumers
top_procs=$(ps aux --sort=-%mem | awk 'NR<=6 && NR>1 {printf "%s:%.1f%% ", $11, $4}')

# Alert level
if [ "$ram_pct" -ge 90 ]; then
  alert="CRITICAL"
elif [ "$ram_pct" -ge 75 ]; then
  alert="WARNING"
elif [ "$ram_pct" -ge 60 ]; then
  alert="ELEVATED"
else
  alert="OK"
fi

cat <<EOF
{
  "alert": "$alert",
  "ram": {"total_mb": $total, "used_mb": $used, "free_mb": $free, "pct": $ram_pct},
  "swap": {"total_mb": $swap_total, "used_mb": $swap_used, "pct": $swap_pct},
  "cpu": {"cores": $cores, "load_1m": "$load_1m", "pct": $cpu_pct},
  "disk": {"total": "$disk_total", "used": "$disk_used", "pct": "$disk_pct"},
  "top_procs": "$top_procs"
}
EOF
