#!/usr/bin/env bash
# Build the Paragon MLS MCP server from source
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="${SCRIPT_DIR}/.."

echo "Installing dependencies..."
cd "$SERVER_DIR" && npm install --production

echo "Building TypeScript..."
cd "$SERVER_DIR" && npm run build

echo "Paragon MLS MCP server built successfully."
echo "Server entrypoint: ${SERVER_DIR}/dist/index.js"