#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "IdleClaw Skill Installer"
echo "========================"

# Check required binaries
missing=()
for bin in python3 ollama; do
    if ! command -v "$bin" &>/dev/null; then
        missing+=("$bin")
    fi
done

if [ ${#missing[@]} -gt 0 ]; then
    echo "Error: Missing required binaries: ${missing[*]}"
    echo ""
    echo "Install the missing dependencies:"
    for bin in "${missing[@]}"; do
        case "$bin" in
            python3) echo "  - python3: https://www.python.org/downloads/" ;;
            ollama)  echo "  - ollama: https://ollama.com/download" ;;
        esac
    done
    exit 1
fi

echo "Installing Python dependencies..."
pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "  Contribute: python scripts/contribute.py"
echo "  Consume:    python scripts/consume.py --model <name> --prompt \"<message>\""
echo "  Status:     python scripts/status.py"
