#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="/usr/local/bin"

# Detect architecture
ARCH=$(uname -m)
case "$ARCH" in
    arm64) ;;
    *)
        echo "Unsupported architecture: $ARCH"
        echo "AgentGuard currently supports arm64 only. x86_64 support is coming soon."
        echo "Request support at: https://www.agentguard.site"
        exit 1
        ;;
esac

BINARY="$SCRIPT_DIR/bin/agentguard-$ARCH"

if [ ! -f "$BINARY" ]; then
    echo "Error: binary not found for $ARCH at $BINARY"
    echo "This platform is not yet supported. Please request support at https://www.agentguard.site"
    exit 1
fi

# Verify checksum
echo "Verifying checksum..."
cd "$SCRIPT_DIR/bin"
EXPECTED=$(grep "agentguard-$ARCH" checksums.txt | awk '{print $1}')
ACTUAL=$(shasum -a 256 "agentguard-$ARCH" | awk '{print $1}')
cd - > /dev/null

if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "Error: checksum verification failed!"
    echo "Expected: $EXPECTED"
    echo "Actual:   $ACTUAL"
    exit 1
fi
echo "Checksum OK"

# Install binary
echo "Installing agentguard to $INSTALL_DIR..."
cp "$BINARY" "$INSTALL_DIR/agentguard"
chmod +x "$INSTALL_DIR/agentguard"

# Verify installation
if command -v agentguard &> /dev/null; then
    echo "AgentGuard installed successfully (v$(agentguard --version 2>/dev/null || echo 'unknown'))"
else
    echo "Error: installation verification failed"
    exit 1
fi

# Start daemon
echo "Starting AgentGuard daemon..."
agentguard daemon start

echo ""
echo "Installation complete. Dashboard: http://127.0.0.1:19821"
