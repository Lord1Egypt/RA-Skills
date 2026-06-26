#!/bin/bash

# Get script directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get project path from argument or use current directory
PROJECT_PATH="${1:-$(pwd)}"
PACKAGE_JSON_PATH="$PROJECT_PATH/package.json"

echo "========================================"
echo "  NVM Auto Switch Node Version"
echo "========================================"
echo ""
echo "Script location: $SCRIPT_DIR"
echo "Project path: $PROJECT_PATH"

# Check if package.json exists
if [ ! -f "$PACKAGE_JSON_PATH" ]; then
    echo "Error: package.json not found: $PACKAGE_JSON_PATH"
    exit 1
fi

# Read engines.node from package.json
NODE_VERSION=$(cat "$PACKAGE_JSON_PATH" | grep -o '"node"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)

if [ -z "$NODE_VERSION" ]; then
    echo "Warning: engines.node not specified in package.json, skipping"
    exit 0
fi

echo "Project path: $PROJECT_PATH"
echo "Required Node version: $NODE_VERSION"

# Parse version number
TARGET_VERSION=$(echo "$NODE_VERSION" | sed 's/[^0-9.]//g')
MAJOR_VERSION=$(echo "$TARGET_VERSION" | cut -d'.' -f1)

echo "Target major version: $MAJOR_VERSION.x"
echo ""

# Function to check if nvm is available
check_nvm() {
    type nvm &> /dev/null
    return $?
}

# Check if nvm is installed
if ! check_nvm; then
    echo "nvm command not found, starting auto installation..."
    echo ""
    
    # Download and install nvm
    echo "Downloading nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    
    # Load nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    
    # Check if installation succeeded
    if ! check_nvm; then
        echo "Error: nvm installation failed, please install manually"
        echo "Install command: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash"
        exit 1
    fi
    
    echo "nvm installed successfully"
    echo ""
fi

# Ensure nvm is loaded
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

echo "Installed Node versions:"
nvm list
echo ""

# Get list of installed versions
INSTALLED_VERSIONS=$(nvm list | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | sort -V -r)

# Find matching version
MATCHED_VERSION=$(echo "$INSTALLED_VERSIONS" | grep "^$MAJOR_VERSION\." | head -n 1)

if [ -n "$MATCHED_VERSION" ]; then
    echo "Found matching installed version: $MATCHED_VERSION"
    nvm use "$MATCHED_VERSION"
    echo ""
    echo "Successfully switched to Node $MATCHED_VERSION"
else
    echo "No matching version found, need to download Node $MAJOR_VERSION.x latest version"
    echo ""
    
    # Get available latest version
    LATEST_VERSION=$(nvm list-remote | grep "^v$MAJOR_VERSION\." | tail -n 1 | sed 's/^v//')
    
    if [ -z "$LATEST_VERSION" ]; then
        echo "Error: No available version found for Node $MAJOR_VERSION.x"
        exit 1
    fi
    
    echo "Preparing to download Node $LATEST_VERSION..."
    nvm install "$LATEST_VERSION"
    
    echo "Switching to newly installed version..."
    nvm use "$LATEST_VERSION"
    
    echo ""
    echo "Installed and switched to Node $LATEST_VERSION"
fi

echo ""
echo "Verifying current version:"
echo "   Node: $(node -v)"
echo "   npm:  v$(npm -v)"
