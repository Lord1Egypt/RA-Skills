#!/bin/bash
# Post-install setup script for Memory Garden MCP skill
# Creates necessary directories and validates binary

set -e

DATA_DIR="${MG_DATA_DIR:-$HOME/.memory-garden}"
PATTERN_DIR="${DATA_DIR}/patterns"
LOG_DIR="${DATA_DIR}/logs"

echo "Memory Garden MCP - Post-install setup"
echo "======================================="
echo ""

# Create directories
echo "Creating data directories..."
mkdir -p "$PATTERN_DIR"
mkdir -p "$LOG_DIR"
echo "  Data: $DATA_DIR"
echo "  Patterns: $PATTERN_DIR"
echo "  Logs: $LOG_DIR"
echo ""

# Check for binary
echo "Checking for daemon binary..."
if command -v mg-daemon &> /dev/null; then
    BINARY=$(which mg-daemon)
    VERSION=$(mg-daemon --version 2>/dev/null || echo "unknown")
    echo "  Found: $BINARY (version: $VERSION)"
elif command -v memory-garden &> /dev/null; then
    BINARY=$(which memory-garden)
    VERSION=$(memory-garden --version 2>/dev/null || echo "unknown")
    echo "  Found: $BINARY (version: $VERSION)"
else
    echo "  WARNING: Daemon binary not found in PATH"
    echo ""
    echo "  Install with:"
    echo "    go install github.com/live-neon/memory-garden/cmd/mg-daemon@latest"
    echo ""
    echo "  Or download from:"
    echo "    https://github.com/live-neon/memory-garden/releases"
    echo ""
fi

# Verify port availability
PORT="${MG_PORT:-18790}"
echo ""
echo "Checking port $PORT..."
if lsof -i ":$PORT" &> /dev/null; then
    echo "  WARNING: Port $PORT is in use"
    lsof -i ":$PORT" | head -3
else
    echo "  Port $PORT is available"
fi

echo ""
echo "Setup complete!"
echo ""
echo "To start the daemon manually:"
echo "  mg-daemon --serve --addr 127.0.0.1:$PORT"
echo ""
echo "The skill will auto-start the daemon when needed."
