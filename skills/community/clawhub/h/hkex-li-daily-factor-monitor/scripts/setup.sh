#!/bin/bash
# HKEX L&I Monitor Setup Utility

echo "Checking requirements..."
command -v curl >/dev/null 2>&1 || { echo >&2 "curl required but not installed."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo >&2 "jq required but not installed."; exit 1; }
command -v pdftotext >/dev/null 2>&1 || { echo >&2 "pdftotext required (poppler-utils)."; exit 1; }

echo "Creating config directory..."
mkdir -p "$HOME/.config/hkex-li-daily-factor-monitor"

echo "Setup complete. Please copy config.example.json to ~/.config/hkex-li-daily-factor-monitor/config.json"
