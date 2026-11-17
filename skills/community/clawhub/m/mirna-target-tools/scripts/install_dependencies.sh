#!/bin/bash
# Install dependencies for bioinformatics skill

set -e

echo "Installing bioinformatics dependencies..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    sudo apt-get update
    sudo apt-get install -y wget tar build-essential python3-pandas python3-numpy
    
    # Python deps for annotation / plotting (optional)
    pip3 install --user mygene matplotlib
    
    # Install miRanda from GitHub mirror (original site down)
    echo "Installing miRanda from GitHub mirror..."
    cd /tmp
    wget https://github.com/miRanda/miRanda/archive/refs/tags/3.3a.tar.gz -O miRanda-3.3a.tar.gz
    tar xzf miRanda-3.3a.tar.gz
    cd miRanda-3.3a
    ./configure
    make
    sudo make install
    cd /tmp
    rm -rf miRanda-3.3a.tar.gz miRanda-3.3a
    
    # Install TargetScan (requires Perl)
    echo "Installing TargetScan (perl libraries)..."
    sudo apt-get install -y perl perl-doc libxml-perl
    echo "Note: You need to download TargetScan database separately from:"
    echo "https://www.targetscan.org/cgi-bin/targetscan/data_download.cgi"
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first from https://brew.sh/"
        exit 1
    fi
    
    brew install python3 wget
    pip3 install pandas numpy mygene matplotlib
    
    echo "Installing miRanda from GitHub mirror..."
    cd /tmp
    curl -LO https://github.com/miRanda/miRanda/archive/refs/tags/3.3a.tar.gz -o miRanda-3.3a.tar.gz
    tar xzf miRanda-3.3a.tar.gz
    cd miRanda-3.3a
    ./configure
    make
    sudo make install
    cd /tmp
    rm -rf miRanda-3.3a.tar.gz miRanda-3.3a
    
    echo "Note: TargetScan database needs to be downloaded separately from:"
    echo "https://www.targetscan.org/cgi-bin/targetscan/data_download.cgi"
    
    echo "For Cytoscape, download from: https://cytoscape.org/download.html"
else
    echo "Unsupported OS. Please install tools manually."
    exit 1
fi

# Install Cytoscape - optional, user can install GUI themselves
echo ""
echo "✅ Basic dependencies installed!"
echo ""
echo "Next steps:"
echo "1. Download TargetScan database from https://www.targetscan.org/"
echo "2. Install Cytoscape from https://cytoscape.org/ for visualization"
echo "3. Run check_env.py again to verify installation"
