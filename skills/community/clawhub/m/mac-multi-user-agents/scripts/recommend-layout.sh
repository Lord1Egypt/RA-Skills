#!/usr/bin/env bash
set -euo pipefail

cpus="$(sysctl -n hw.ncpu)"
mem_bytes="$(sysctl -n hw.memsize)"
mem_gb="$((mem_bytes / 1024 / 1024 / 1024))"

browser_heavy=$(( mem_gb / 8 ))
mixed=$(( mem_gb / 6 ))
light=$(( mem_gb / 4 ))

if (( browser_heavy < 1 )); then browser_heavy=1; fi
if (( mixed < 1 )); then mixed=1; fi
if (( light < 1 )); then light=1; fi

cpu_browser_cap=$(( cpus / 4 ))
cpu_mixed_cap=$(( cpus / 2 ))
cpu_light_cap=$cpus

if (( cpu_browser_cap < 1 )); then cpu_browser_cap=1; fi
if (( cpu_mixed_cap < 1 )); then cpu_mixed_cap=1; fi
if (( cpu_light_cap < 1 )); then cpu_light_cap=1; fi

if (( browser_heavy > cpu_browser_cap )); then browser_heavy=$cpu_browser_cap; fi
if (( mixed > cpu_mixed_cap )); then mixed=$cpu_mixed_cap; fi
if (( light > cpu_light_cap )); then light=$cpu_light_cap; fi

echo "=== hardware ==="
echo "cpus: $cpus"
echo "memory_gb: $mem_gb"
echo
echo "=== recommended concurrent agent users ==="
echo "browser_heavy: $browser_heavy"
echo "mixed: $mixed"
echo "light: $light"
echo
echo "=== planning note ==="
echo "Count browser-heavy users conservatively. Managed browsers and Fast User Switching eat RAM before CPU becomes the limit."
