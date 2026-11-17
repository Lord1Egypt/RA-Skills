#!/bin/bash
# update.sh — Self-update ocas-imagine from GitHub
# Usage: bash update.sh [--help]
# --help: Show this help message

if [[ "${1:-}" == "--help" ]]; then
    echo "Usage: bash update.sh [--help]"
    echo "  Pulls latest ocas-imagine from GitHub, preserving local data."
    exit 0
fi

cd "$(dirname "$0")/.."
git reset --hard HEAD 2>/dev/null
git clean -fd 2>/dev/null
git pull 2>/dev/null
