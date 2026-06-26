#!/bin/bash
# Setup script for McDonald's China MCP Token
# This script helps you configure the MCDCN_MCP_TOKEN environment variable

echo "🍟 McDonald's China MCP Token Setup"
echo "====================================="
echo ""
echo "Step 1: Get your token from https://open.mcd.cn/mcp"
echo "  1. Login with your phone number (must match McDonald's app)"
echo "  2. Click '控制台' (Console)"
echo "  3. Click '激活' (Activate) to generate MCP Token"
echo "  4. Copy the token"
echo ""
read -p "Paste your MCP Token here: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ Error: Token cannot be empty"
    exit 1
fi

# Detect shell profile
SHELL_PROFILE=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

# Check if token already exists in profile
if [ -n "$SHELL_PROFILE" ] && grep -q "MCDCN_MCP_TOKEN" "$SHELL_PROFILE" 2>/dev/null; then
    echo ""
    echo "⚠️  Token already configured in $SHELL_PROFILE"
    echo "Updating existing entry..."
    sed -i '' "s|export MCDCN_MCP_TOKEN=.*|export MCDCN_MCP_TOKEN=\"$TOKEN\"|" "$SHELL_PROFILE"
else
    # Add to profile
    if [ -n "$SHELL_PROFILE" ]; then
        echo "" >> "$SHELL_PROFILE"
        echo "# McDonald's China MCP Token" >> "$SHELL_PROFILE"
        echo "export MCDCN_MCP_TOKEN=\"$TOKEN\"" >> "$SHELL_PROFILE"
        echo "✅ Token added to $SHELL_PROFILE"
    fi
fi

# Also export for current session
export MCDCN_MCP_TOKEN="$TOKEN"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use immediately in current terminal:"
echo "  export MCDCN_MCP_TOKEN=\"$TOKEN\""
echo ""
echo "Or restart your terminal to load from profile."
echo ""
echo "Test with: mcd-cn now-time-info"
