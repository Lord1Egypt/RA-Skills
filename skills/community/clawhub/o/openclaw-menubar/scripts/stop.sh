#!/bin/bash

echo "🛑 Stopping OpenClaw Menu Bar..."

# Find and kill the process
if pgrep -f "openclaw-menubar.*electron" > /dev/null; then
    pkill -f "openclaw-menubar.*electron"
    sleep 1
    
    if pgrep -f "openclaw-menubar.*electron" > /dev/null; then
        echo "⚠️  Process still running, forcing kill..."
        pkill -9 -f "openclaw-menubar.*electron"
    fi
    
    echo "✅ OpenClaw Menu Bar stopped"
else
    echo "ℹ️  OpenClaw Menu Bar is not running"
fi
