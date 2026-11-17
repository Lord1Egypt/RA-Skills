#!/bin/bash
# Usage: update.sh [--help] — pull latest skill version from upstream
if [[ "$1" == "--help" ]]; then
    echo "Usage: update.sh [--help]"
    echo "Pulls the latest skill version from upstream Git repository."
    exit 0
fi
cd "$(dirname "$0")/.."
git reset --hard HEAD 2>/dev/null
git clean -fd 2>/dev/null
git pull 2>/dev/null
