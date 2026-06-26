#!/bin/bash
set -e

# Detect OS
OS="$(uname -s)"
ARCH="$(uname -m)"

CMD_NAME="qq-map-cli"
ZIP_FILE="qq-map-cli.zip"
DOWNLOAD_URL=""

if [ "$OS" = "Darwin" ]; then
    DOWNLOAD_URL="https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-darwin-arm64.zip"
    CMD_NAME="qq-map-cli"
elif [ "$OS" = "Linux" ]; then
    DOWNLOAD_URL="https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-linux-x86_64.zip"
    CMD_NAME="qq-map-cli"
elif echo "$OS" | grep -iq 'mingw\|cygwin\|msys\|windows_nt'; then
    DOWNLOAD_URL="https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-windows-x86_64.zip"
    CMD_NAME="qq-map-cli.exe"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR="$DIR/bin"
CMD_PATH="$BIN_DIR/$CMD_NAME"

if [ ! -x "$CMD_PATH" ] && [ ! -f "$CMD_PATH" ]; then
    echo "Downloading $CMD_NAME..." >&2
    mkdir -p "$BIN_DIR"
    curl -L -s "$DOWNLOAD_URL" -o "$BIN_DIR/$ZIP_FILE"
    unzip -q -o "$BIN_DIR/$ZIP_FILE" -d "$BIN_DIR"
    if [ "$CMD_NAME" = "qq-map-cli" ]; then
        chmod +x "$CMD_PATH"
    fi
    rm -f "$BIN_DIR/$ZIP_FILE"
    echo "Download complete: $CMD_PATH" >&2
else
    echo "$CMD_NAME is already downloaded at $CMD_PATH" >&2
fi
