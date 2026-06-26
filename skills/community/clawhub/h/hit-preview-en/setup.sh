#!/bin/bash
# Hit Preview EN - setup script
# Post-install: make run script executable
DIR="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$DIR/run-hit-preview-en.sh"
echo "✅ Hit Preview EN installed. Use: ./run-hit-preview-en.sh analyze -f <script.txt>"
