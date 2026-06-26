#!/bin/bash

set -euo pipefail

echo "print-local-auth-snippet.sh is deprecated."
echo "Use print-browser-auth-setup.sh instead."
echo ""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/print-browser-auth-setup.sh"
