#!/bin/bash
# check_nvs_status.sh - Check if NVS is installed and report status

echo "=== NVS Installation Status Check ==="

# Check if nvs command exists
if command -v nvs &> /dev/null; then
    echo "✓ NVS is installed"
    echo "  Version: $(nvs --version 2>/dev/null || echo 'Unknown')"
    
    # Check NVS_HOME
    if [ -n "$NVS_HOME" ]; then
        echo "  NVS_HOME: $NVS_HOME"
    else
        echo "  NVS_HOME: Not set (using default)"
    fi
    
    # List installed versions
    echo ""
    echo "Installed Node.js versions:"
    nvs ls 2>/dev/null || echo "  Unable to list versions"
else
    echo "✗ NVS is not installed"
    echo ""
    echo "To install NVS:"
    echo ""
    echo "Windows (PowerShell):"
    echo "  winget install jasongin.nvs"
    echo "  OR"
    echo "  choco install nvs"
    echo ""
    echo "Mac/Linux:"
    echo "  export NVS_HOME=\"\$HOME/.nvs\""
    echo "  git clone https://github.com/jasongin/nvs \"\$NVS_HOME\""
    echo "  . \"\$NVS_HOME/nvs.sh\" install"
fi

echo ""
echo "=== Current Node.js Version ==="
if command -v node &> /dev/null; then
    echo "Node.js: $(node --version)"
    echo "npm: $(npm --version)"
else
    echo "Node.js: Not found"
fi
