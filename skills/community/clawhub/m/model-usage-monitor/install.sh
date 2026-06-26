#!/usr/bin/env bash
# OpenClaw Model Usage Monitor Skill — Transparent Installation
# Version: 1.0.1
# No encryption, no external calls, fully transparent

set -e

SKILL_DIR="${HOME}/.openclaw/workspace/skills/model-usage-monitor"
LIB_DIR="${HOME}/.openclaw/workspace/.lib"

echo "🔧 Installing Model Usage Monitor Skill..."

# Create necessary directories
mkdir -p "$LIB_DIR"
mkdir -p "${HOME}/.openclaw/logs"

# Copy monitor script to .lib for easy access
if [ -f "${SKILL_DIR}/monitor.py" ]; then
    cp "${SKILL_DIR}/monitor.py" "${LIB_DIR}/model_usage_monitor_v2.py"
    chmod +x "${LIB_DIR}/model_usage_monitor_v2.py"
    echo "✅ Monitor script installed to ${LIB_DIR}/model_usage_monitor_v2.py"
fi

# Copy config if not exists
if [ -f "${SKILL_DIR}/config.json" ] && [ ! -f "${LIB_DIR}/model_monitor_config.json" ]; then
    cp "${SKILL_DIR}/config.json" "${LIB_DIR}/model_monitor_config.json"
    echo "✅ Default config copied"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  python3 ${LIB_DIR}/model_usage_monitor_v2.py           # Full report"
echo "  python3 ${LIB_DIR}/model_usage_monitor_v2.py --live    # Real-time monitoring"
echo "  python3 ${LIB_DIR}/model_usage_monitor_v2.py --alert-check  # Check alerts only"
