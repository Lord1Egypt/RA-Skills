#!/bin/bash

# Proof of Work — Installation Script
# Creates directory structure, copies files, sets permissions

set -e

# Determine home directory
HOME_DIR="${HOME:=$(cd ~ && pwd)}"
POW_DIR="$HOME_DIR/.proof-of-work"

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Proof of Work — Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if script is run from correct directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -f "$SCRIPT_DIR/proof-of-work.sh" ]; then
    echo "Error: proof-of-work.sh not found in $SCRIPT_DIR"
    echo "Please run this installer from the Proof of Work directory"
    exit 2
fi

# Step 1: Create directories
echo -e "${YELLOW}Step 1: Creating directory structure...${NC}"
mkdir -p "$POW_DIR"
mkdir -p "$POW_DIR/reports"
echo -e "${GREEN}✓ Created $POW_DIR${NC}"

# Step 2: Copy proof-of-work script
echo ""
echo -e "${YELLOW}Step 2: Installing proof-of-work script...${NC}"
cp "$SCRIPT_DIR/proof-of-work.sh" "$POW_DIR/proof-of-work.sh"
chmod +x "$POW_DIR/proof-of-work.sh"
echo -e "${GREEN}✓ Installed to $POW_DIR/proof-of-work.sh${NC}"

# Step 3: Copy sample configuration
echo ""
echo -e "${YELLOW}Step 3: Installing sample configuration...${NC}"
if [ -f "$SCRIPT_DIR/sample-config.json" ]; then
    cp "$SCRIPT_DIR/sample-config.json" "$POW_DIR/sample-config.json"

    # Only create config.json if it doesn't exist
    if [ ! -f "$POW_DIR/config.json" ]; then
        cp "$SCRIPT_DIR/sample-config.json" "$POW_DIR/config.json"
        echo -e "${GREEN}✓ Created config.json (customize as needed)${NC}"
    else
        echo -e "${YELLOW}⚠ config.json already exists (keeping existing)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ sample-config.json not found${NC}"
fi

# Step 4: Create empty log file
echo ""
echo -e "${YELLOW}Step 4: Setting up logging...${NC}"
touch "$POW_DIR/checks.log"
echo -e "${GREEN}✓ Created $POW_DIR/checks.log${NC}"

# Step 5: Create symlink in /usr/local/bin if available
echo ""
echo -e "${YELLOW}Step 5: Adding to PATH...${NC}"
if [ -w /usr/local/bin ]; then
    ln -sf "$POW_DIR/proof-of-work.sh" /usr/local/bin/proof-of-work
    echo -e "${GREEN}✓ Created symlink: proof-of-work${NC}"
    echo "You can now run: proof-of-work <command>"
else
    echo -e "${YELLOW}⚠ Cannot write to /usr/local/bin${NC}"
    echo "Add this to your PATH manually:"
    echo "  export PATH=\"$POW_DIR:\$PATH\""
fi

# Step 6: Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Installation directory: $POW_DIR"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Review and customize your configuration:"
echo "   ${BLUE}$POW_DIR/config.json${NC}"
echo ""
echo "2. Try the first check:"
if command -v proof-of-work &> /dev/null; then
    echo "   ${BLUE}proof-of-work init${NC}"
    echo "   ${BLUE}proof-of-work check ~/some-file.md${NC}"
else
    echo "   ${BLUE}$POW_DIR/proof-of-work.sh init${NC}"
    echo "   ${BLUE}$POW_DIR/proof-of-work.sh check ~/some-file.md${NC}"
fi
echo ""
echo "3. Set up cron monitoring (optional):"
echo "   ${BLUE}crontab -e${NC}"
echo "   Add: ${BLUE}0 * * * * $POW_DIR/proof-of-work.sh watch${NC}"
echo ""
echo "4. Read the documentation:"
echo "   ${BLUE}$SCRIPT_DIR/README.md${NC}"
echo ""
