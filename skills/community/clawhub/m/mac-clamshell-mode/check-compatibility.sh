#!/bin/bash
# Mac Clamshell Mode Compatibility Checker
# Checks if the current Mac model and macOS version support clamshell mode

set -e

echo "🔍 Checking Mac compatibility for clamshell mode..."

# Get macOS version (this should always work)
MACOS_VERSION=$(sw_vers -productVersion)

# Try to get Mac model using multiple methods
if command -v system_profiler &> /dev/null; then
    MAC_MODEL=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Model Identifier" | awk '{print $3}' | head -1)
elif [ -f "/usr/sbin/sysctl" ]; then
    # Fallback method using sysctl
    MAC_MODEL=$(sysctl -n hw.model 2>/dev/null || echo "Unknown")
else
    MAC_MODEL="Unknown"
fi

echo "💻 Mac Model: $MAC_MODEL"
echo "🍎 macOS Version: $MACOS_VERSION"

# Check if it's a MacBook (laptop) - look for common MacBook identifiers
if [[ "$MAC_MODEL" == *"MacBook"* ]] || [[ "$MAC_MODEL" == *"MBP"* ]] || [[ "$MAC_MODEL" == *"MB"* ]]; then
    echo "✅ Device is a MacBook - compatible with clamshell mode"
    
    # Check macOS version compatibility (macOS Catalina 10.15+ recommended)
    MAJOR_VERSION=$(echo "$MACOS_VERSION" | cut -d. -f1)
    MINOR_VERSION=$(echo "$MACOS_VERSION" | cut -d. -f2)
    
    if [ "$MAJOR_VERSION" -ge 11 ] || ([ "$MAJOR_VERSION" -eq 10 ] && [ "$MINOR_VERSION" -ge 15 ]); then
        echo "✅ macOS version supports clamshell mode"
        exit 0
    else
        echo "⚠️  Older macOS version may have limited clamshell support"
        exit 1
    fi
else
    echo "❌ Device appears to be not a MacBook - clamshell mode not applicable"
    echo "💡 Note: This tool is designed for MacBook laptops only"
    exit 1
fi