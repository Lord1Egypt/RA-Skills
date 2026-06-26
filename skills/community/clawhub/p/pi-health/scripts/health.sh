#!/bin/bash
# pi-health — Raspberry Pi Health Monitor
# Exit codes: 0 = healthy, 1 = warnings, 2 = critical

EXIT_CODE=0

warn() { [[ $EXIT_CODE -lt 1 ]] && EXIT_CODE=1; }
crit() { EXIT_CODE=2; }
has() { command -v "$1" >/dev/null 2>&1; }

echo "══════════════════════════════════════"
echo "  🍓 Raspberry Pi Health Report"
echo "══════════════════════════════════════"
echo ""

# ── CPU Temperature ──
TEMP_WARN=70
TEMP_CRIT=80
if [[ -f /sys/class/thermal/thermal_zone0/temp ]]; then
  raw=$(cat /sys/class/thermal/thermal_zone0/temp)
  temp=$(awk "BEGIN { printf \"%.1f\", $raw / 1000 }")
  if (( $(echo "$temp > $TEMP_CRIT" | bc -l) )); then
    echo "🔴 CPU Temp:       ${temp}°C (CRITICAL >$TEMP_CRIT)"
    crit
  elif (( $(echo "$temp > $TEMP_WARN" | bc -l) )); then
    echo "⚠️  CPU Temp:       ${temp}°C (WARNING >$TEMP_WARN)"
    warn
  else
    echo "✅ CPU Temp:       ${temp}°C"
  fi
else
  echo "⚠️  CPU Temp:       unavailable"
  warn
fi

# ── Throttling ──
if has vcgencmd; then
  raw_throttle=$(vcgencmd get_throttled | cut -d= -f2)
  # Remove 0x prefix for arithmetic
  throttle_val=$((${raw_throttle}))
  if ((throttle_val != 0)); then
    echo "⚠️  Throttling:     ${raw_throttle}"
    # Decode current flags (bits 0-3)
    ((throttle_val & 0x1))  && echo "   ├─ 🔴 Under-voltage detected!"
    ((throttle_val & 0x2))  && echo "   ├─ ⚠️  ARM frequency capped"
    ((throttle_val & 0x4))  && echo "   ├─ ⚠️  Currently throttled"
    ((throttle_val & 0x8))  && echo "   ├─ ⚠️  Soft temperature limit"
    # Historical flags (bits 16-19)
    ((throttle_val & 0x10000))  && echo "   ├─ 📋 Under-voltage occurred (past)"
    ((throttle_val & 0x20000))  && echo "   ├─ 📋 ARM freq capped (past)"
    ((throttle_val & 0x40000))  && echo "   ├─ 📋 Throttling occurred (past)"
    ((throttle_val & 0x80000))  && echo "   └─ 📋 Soft temp limit (past)"
    # Under-voltage is critical, others are warnings
    ((throttle_val & 0x1)) && crit || warn
  else
    echo "✅ Throttling:     none"
  fi
else
  echo "⚠️  Throttling:     vcgencmd not found"
  warn
fi

# ── Voltage ──
if has vcgencmd; then
  echo "── Voltages ──"
  for domain in core sdram_c sdram_i sdram_p; do
    v=$(vcgencmd measure_volts "$domain" 2>/dev/null | cut -d= -f2 | tr -d 'V')
    if [[ -n "$v" ]]; then
      echo "   $domain: ${v}V"
    fi
  done
fi

# ── Memory ──
if mem=$(free -m 2>/dev/null); then
  ram_used=$(echo "$mem" | awk '/^Mem:/ {print $3}')
  ram_total=$(echo "$mem" | awk '/^Mem:/ {print $2}')
  ram_pct=$((ram_used * 100 / ram_total))
  swap_used=$(echo "$mem" | awk '/^Swap:/ {print $3}')
  swap_total=$(echo "$mem" | awk '/^Swap:/ {print $2}')
  
  if ((ram_pct > 90)); then
    echo "🔴 Memory:         ${ram_used}/${ram_total}MB (${ram_pct}%) CRITICAL"
    crit
  elif ((ram_pct > 75)); then
    echo "⚠️  Memory:         ${ram_used}/${ram_total}MB (${ram_pct}%)"
    warn
  else
    echo "✅ Memory:         ${ram_used}/${ram_total}MB (${ram_pct}%)"
  fi
  
  if ((swap_total > 0 && swap_used > 0)); then
    swap_pct=$((swap_used * 100 / swap_total))
    echo "   Swap:           ${swap_used}/${swap_total}MB (${swap_pct}%)"
  else
    echo "   Swap:           not used"
  fi
fi

# ── SD Card / Disk ──
root_line=$(df -h / 2>/dev/null | tail -1)
if [[ -n "$root_line" ]]; then
  disk_size=$(echo "$root_line" | awk '{print $2}')
  disk_used=$(echo "$root_line" | awk '{print $3}')
  disk_pct=$(echo "$root_line" | awk '{print $5}' | tr -d '%')
  
  if ((disk_pct > 90)); then
    echo "🔴 Disk:           ${disk_used}/${disk_size} (${disk_pct}%) CRITICAL"
    crit
  elif ((disk_pct > 75)); then
    echo "⚠️  Disk:           ${disk_used}/${disk_size} (${disk_pct}%)"
    warn
  else
    echo "✅ Disk:           ${disk_used}/${disk_size} (${disk_pct}%)"
  fi
fi

# ── CPU Frequency ──
cur_path="/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
max_path="/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"
if [[ -f "$cur_path" ]]; then
  cur_mhz=$(awk "BEGIN { printf \"%.0f\", $(cat "$cur_path") / 1000 }")
  if [[ -f "$max_path" ]]; then
    max_mhz=$(awk "BEGIN { printf \"%.0f\", $(cat "$max_path") / 1000 }")
    echo "✅ CPU Freq:       ${cur_mhz}/${max_mhz} MHz"
  else
    echo "✅ CPU Freq:       ${cur_mhz} MHz"
  fi
fi

# ── Uptime & Load ──
if [[ -f /proc/uptime ]]; then
  up_secs=$(cut -d. -f1 /proc/uptime)
  days=$((up_secs / 86400))
  hours=$(((up_secs % 86400) / 3600))
  mins=$(((up_secs % 3600) / 60))
  load=$(cat /proc/loadavg | cut -d' ' -f1-3)
  ncpu=$(nproc 2>/dev/null || echo 4)
  load1=$(echo "$load" | cut -d' ' -f1)
  
  uptime_str=""
  ((days > 0)) && uptime_str="${days}d "
  uptime_str="${uptime_str}${hours}h ${mins}m"
  
  if (( $(echo "$load1 > $ncpu * 2" | bc -l) )); then
    echo "🔴 Uptime:         ${uptime_str} | Load: ${load} (HIGH)"
    crit
  elif (( $(echo "$load1 > $ncpu" | bc -l) )); then
    echo "⚠️  Uptime:         ${uptime_str} | Load: ${load}"
    warn
  else
    echo "✅ Uptime:         ${uptime_str} | Load: ${load}"
  fi
fi

# ── Fan ──
fan_input=$(find /sys/class/hwmon/*/fan1_input 2>/dev/null | head -1)
if [[ -n "$fan_input" && -f "$fan_input" ]]; then
  rpm=$(cat "$fan_input" 2>/dev/null)
  if ((rpm > 0)); then
    echo "✅ Fan:            ${rpm} RPM"
  else
    echo "✅ Fan:            off (passive cooling)"
  fi
elif [[ -d /sys/class/thermal/cooling_device0 ]]; then
  state=$(cat /sys/class/thermal/cooling_device0/cur_state 2>/dev/null || echo "?")
  echo "✅ Fan:            cooling state $state"
else
  echo "✅ Fan:            no fan detected"
fi

# ── Overclock ──
config_file="/boot/firmware/config.txt"
[[ ! -f "$config_file" ]] && config_file="/boot/config.txt"
if [[ -f "$config_file" ]]; then
  oc_lines=$(grep -E "^(over_voltage|arm_freq|gpu_freq|force_turbo)" "$config_file" 2>/dev/null)
  if [[ -n "$oc_lines" ]]; then
    echo "⚠️  Overclock:      detected"
    while IFS= read -r line; do
      echo "   └─ $line"
    done <<< "$oc_lines"
    warn
  else
    echo "✅ Overclock:      stock settings"
  fi
else
  echo "✅ Overclock:      config not found"
fi

# ── Power Issues (dmesg) ──
if uv_count=$(dmesg 2>/dev/null | grep -ci "under.voltage"); then
  if ((uv_count > 0)); then
    echo "🔴 Power:          $uv_count under-voltage events in dmesg!"
    crit
  else
    echo "✅ Power:          no issues"
  fi
else
  echo "✅ Power:          dmesg not accessible"
fi

echo ""
echo "══════════════════════════════════════"
case $EXIT_CODE in
  0) echo "  Status: ✅ HEALTHY" ;;
  1) echo "  Status: ⚠️  WARNINGS" ;;
  2) echo "  Status: 🔴 CRITICAL" ;;
esac
echo "══════════════════════════════════════"

exit $EXIT_CODE
