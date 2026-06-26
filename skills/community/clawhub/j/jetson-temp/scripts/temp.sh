#!/bin/bash
echo "=== Jetson Temperature ==="
for zone in /sys/class/thermal/thermal_zone*/temp; do
    temp=$(cat $zone 2>/dev/null)
    if [ -n "$temp" ]; then
        echo "Temperature: $((temp/1000))°C"
    fi
done
