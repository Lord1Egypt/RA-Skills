#!/bin/bash
# Invoice Extractor Skill Installation Script

echo "=================================="
echo "Invoice Extractor Skill Installer"
echo "=================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo ""
echo "Creating directories..."
mkdir -p fp output .temp

# Copy config template
echo ""
echo "Setting up configuration..."
if [ ! -f "config.txt" ]; then
    cp config.template.txt config.txt
    echo "Created config.txt from template"
    echo "Please edit config.txt with your Baidu OCR credentials"
else
    echo "config.txt already exists, skipping"
fi

echo ""
echo "=================================="
echo "Installation complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Get Baidu OCR API credentials from https://cloud.baidu.com/product/ocr"
echo "2. Edit config.txt with your API Key and Secret Key"
echo "3. Place invoice files in fp/ directory"
echo "4. Run: python src/main_baidu.py"
echo ""
