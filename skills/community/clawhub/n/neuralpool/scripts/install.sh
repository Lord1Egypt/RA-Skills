#!/usr/bin/env bash
set -euo pipefail

# NeuralPool Node Agent Installer
# Auto-detects OS and architecture, downloads the latest binary

REPO="neuralpool/neuralpool-node"
VERSION="${INSTALL_VERSION:-latest}"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"

echo "=== NeuralPool Node Agent Installer ==="
echo ""

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$OS" in
  linux)  OS="linux" ;;
  darwin) OS="darwin" ;;
  mingw*|msys*|cygwin*) OS="windows" ;;
  *) echo "Error: Unsupported OS: $OS"; exit 1 ;;
esac

case "$ARCH" in
  x86_64|amd64)  ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
  *) echo "Error: Unsupported architecture: $ARCH"; exit 1 ;;
esac

if [ "$OS" = "windows" ]; then
  BINARY="npnode-${OS}-${ARCH}.exe"
else
  BINARY="npnode-${OS}-${ARCH}"
fi

if [ "$VERSION" = "latest" ]; then
  URL="https://github.com/${REPO}/releases/latest/download/${BINARY}"
else
  URL="https://github.com/${REPO}/releases/download/${VERSION}/${BINARY}"
fi

echo "  Platform: ${OS}/${ARCH}"
echo "  Binary:   ${BINARY}"
echo "  URL:      ${URL}"
echo "  Install:  ${INSTALL_DIR}/npnode"
echo ""

if command -v npnode &>/dev/null; then
  echo "  Existing npnode found: $(which npnode)"
  echo "  It will be replaced."
  echo ""
fi

TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

echo "  Downloading..."
if command -v curl &>/dev/null; then
  curl -fSL --progress-bar "$URL" -o "$TMPFILE"
elif command -v wget &>/dev/null; then
  wget -q --show-progress -O "$TMPFILE" "$URL"
else
  echo "Error: curl or wget required"; exit 1
fi

chmod +x "$TMPFILE"

echo ""
echo "  Installing to ${INSTALL_DIR}/npnode..."
if [ -w "$INSTALL_DIR" ]; then
  mv "$TMPFILE" "${INSTALL_DIR}/npnode"
else
  echo "  (sudo required for ${INSTALL_DIR})"
  sudo mv "$TMPFILE" "${INSTALL_DIR}/npnode"
fi

echo ""
echo "  ✓ Installed: ${INSTALL_DIR}/npnode"
echo "  Version: $(npnode version 2>/dev/null || echo 'unknown')"
echo ""
echo "  Next steps:"
echo "    1. Register at https://neuralpool.ai and generate an auth token"
echo "    2. Run: npnode setup"
echo "    3. Run: npnode start"
echo ""
echo "  Done! Visit https://neuralpool.ai for more information."
