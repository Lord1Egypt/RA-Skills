#!/usr/bin/env bash
set -euo pipefail

# Mobile Security: Auto-start Frida Server
# This script automatically checks connected devices, starts frida-server,
# forwards the required port, and verifies frida-server is running.

echo "=== Mobile Security: Auto-start Frida Server ==="

# Step 1: Check if device is connected
echo "Step 1: Checking for connected devices..."
DEVICES=$(adb devices | grep -v "List of devices" | grep -v "daemon" | grep "device" | awk '{print $1}')
DEVICE_COUNT=$(echo "$DEVICES" | grep -c . || true)

if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "❌ No devices connected. Please connect your device and enable USB debugging."
    exit 1
elif [ "$DEVICE_COUNT" -gt 1 ]; then
    echo "⚠️  Multiple devices connected:"
    echo "$DEVICES"
    echo "Please use only one device."
    exit 1
else
    echo "✓ Device connected: $DEVICES"
fi

DEVICE_ID="$DEVICES"

# Step 2: Start frida-server
echo ""
echo "Step 2: Starting frida-server..."
adb -s "$DEVICE_ID" shell "su -c '/data/local/tmp/frida-server &'"

# Wait a moment for frida-server to start
sleep 2

# Step 3: Forward port 27042
echo ""
echo "Step 3: Forwarding port 27042..."
adb -s "$DEVICE_ID" forward tcp:27042 tcp:27042
echo "✓ Port forwarded: localhost:27042 -> device:27042"

# Step 4: Verify frida-server is running
echo ""
echo "Step 4: Verifying frida-server is running..."
FRIDA_OUTPUT=$(frida-ps -Uai 2>&1 || true)

if echo "$FRIDA_OUTPUT" | grep -q "Frida"; then
    echo "✓ Frida-server is running successfully!"
    echo ""
    echo "=== Running Applications ==="
    frida-ps -Uai
else
    echo "⚠️  Could not verify frida-server status. You may need to:"
    echo "  1. Ensure frida-server is pushed to /data/local/tmp/"
    echo "  2. Run: adb shell chmod 755 /data/local/tmp/frida-server"
    echo "  3. Check if your device is rooted"
fi

echo ""
echo "=== Done ==="