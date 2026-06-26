#!/bin/bash
#
# OpenLens Skill Setup Script
# Auto-installs dependencies and configures the environment
#

set -e

echo "========================================"
echo "🎬 OpenLens Skill Setup"
echo "========================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}[1/5]${NC} Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "  ✓ Python $PYTHON_VERSION found"

# Check pip
echo -e "${GREEN}[2/5]${NC} Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 not found${NC}"
    exit 1
fi
echo -e "  ✓ pip found"

# Create virtual environment (optional)
echo -e "${GREEN}[3/5]${NC} Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "  ✓ Created venv"
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo -e "${GREEN}[4/5]${NC} Installing dependencies..."
pip install --upgrade pip -q

# Read requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    echo -e "  ✓ Dependencies installed"
else
    pip install streamlit requests tqdm -q
    echo -e "  ✓ Core packages installed"
fi

# Create output directory
echo -e "${GREEN}[5/5]${NC} Creating directories..."
mkdir -p outputs
echo -e "  ✓ outputs/ directory created"

# Create default config if not exists
if [ ! -f "config.json" ]; then
    cat > config.json << 'EOF'
{
    "video_api_url": "",
    "video_api_key": "",
    "text_api_url": "",
    "text_api_key": "",
    "text_model": "",
    "default_save_path": "./outputs"
}
EOF
    echo -e "  ✓ Default config.json created"
fi

echo ""
echo "========================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "========================================"
echo ""
echo "Usage:"
echo "  GUI Mode:  streamlit run app.py"
echo "  CLI Mode:  python3 cli.py --help"
echo ""
echo "Configuration:"
echo "  Edit config.json or use the GUI to set API keys"
echo ""
echo "First time setup:"
echo "  1. Edit config.json with your API keys"
echo "  2. Run: streamlit run app.py"
echo ""
