#!/bin/bash

# Setup colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Claw Browser Skill Setup ===${NC}"

# Check for Node.js
if ! command -v node &> /dev/null
then
    echo "Node.js not found. Please install Node.js first."
    exit 1
fi

# Install puppeteer-core and other libs
echo -e "${GREEN}Installing Puppeteer Core...${NC}"
npm install puppeteer-core

# Check for Chromium
if [ ! -f "/usr/bin/chromium" ]; then
    echo -e "${BLUE}Warning: /usr/bin/chromium not found.${NC}"
    echo -e "To use God of all Browsers on Linux, please install Chromium manually:"
    echo -e "  sudo apt update && sudo apt install -y chromium-browser"
    echo -e "Once installed, ensure it is at /usr/bin/chromium"
fi

echo -e "${GREEN}Setup Complete! You can now use 'node browser.js'${NC}"
