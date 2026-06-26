#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/scripts/hm4d_installer.py"
echo "If dependencies are missing, install them manually as instructed by the installer output."
