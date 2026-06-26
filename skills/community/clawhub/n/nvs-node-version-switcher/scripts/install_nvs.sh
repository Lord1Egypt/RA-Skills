#!/bin/bash
# install_nvs.sh - Automatically install NVS if not present

echo "=== NVS Auto-Installation Script ==="

# Check if NVS is already installed
if command -v nvs &> /dev/null; then
    echo "✓ NVS is already installed"
    echo "  Version: $(nvs --version 2>/dev/null || echo 'Unknown')"
    exit 0
fi

echo "NVS is not installed. Starting installation..."

# Detect operating system
OS="$(uname -s)"
case "$OS" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Windows;;
    MINGW*)     MACHINE=Windows;;
    MSYS*)      MACHINE=Windows;;
    *)          MACHINE="Unknown"
esac

echo "Detected OS: $MACHINE"

if [ "$MACHINE" = "Windows" ]; then
    echo "Note: For Windows, please use PowerShell or Command Prompt:"
    echo "  winget install jasongin.nvs"
    echo "  OR"
    echo "  choco install nvs"
    exit 1
elif [ "$MACHINE" = "Mac" ] || [ "$MACHINE" = "Linux" ]; then
    echo "Installing NVS for $MACHINE..."
    
    # Set NVS_HOME
    export NVS_HOME="$HOME/.nvs"
    
    # Clone NVS repository
    if [ -d "$NVS_HOME" ]; then
        echo "NVS directory already exists. Updating..."
        cd "$NVS_HOME" && git pull
    else
        echo "Cloning NVS repository..."
        git clone https://github.com/jasongin/nvs "$NVS_HOME"
    fi
    
    # Source the install script
    echo "Initializing NVS..."
    . "$NVS_HOME/nvs.sh" install
    
    echo ""
    echo "✓ NVS installation completed!"
    echo ""
    echo "To start using NVS, either:"
    echo "  1. Restart your terminal, or"
    echo "  2. Run: source ~/.bashrc (or ~/.zshrc)"
    echo ""
    echo "Quick start commands:"
    echo "  nvs add latest    # Install latest Node.js"
    echo "  nvs use latest    # Use latest version"
    echo "  nvs ls            # List installed versions"
else
    echo "Unsupported operating system: $MACHINE"
    exit 1
fi
