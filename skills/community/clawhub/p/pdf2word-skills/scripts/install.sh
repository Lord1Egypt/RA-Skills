#!/bin/bash

# Define the version to download
VERSION="v1.0.0"

# Detect OS
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
EXT=""
if [[ "$OS" == *"mingw"* ]] || [[ "$OS" == *"msys"* ]] || [[ "$OS" == *"cygwin"* ]]; then
    OS="windows"
    EXT=".exe"
elif [ "$OS" != "darwin" ] && [ "$OS" != "linux" ]; then
    echo "Unsupported OS: $OS"
    exit 1
fi

# Detect Architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    ARCH="amd64"
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    ARCH="arm64"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

# Construct filename and URL
FILENAME="docr-$OS-$ARCH$EXT"
DOWNLOAD_URL="https://github.com/scottkiss/doc-ocr/releases/download/$VERSION/$FILENAME"

# Set target directory relative to the script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$SCRIPT_DIR/docr"
TARGET_FILE="$TARGET_DIR/docr$EXT"

echo "Downloading docr $VERSION for $OS ($ARCH)..."

# Ensure the target directory exists
mkdir -p "$TARGET_DIR"

# Download the binary
curl -L -o "$TARGET_FILE" "$DOWNLOAD_URL"

if [ $? -eq 0 ]; then
    # Make it executable
    chmod +x "$TARGET_FILE"
    echo "Successfully downloaded and installed to $TARGET_FILE"
else
    echo "Failed to download $FILENAME from $DOWNLOAD_URL"
    exit 1
fi
