#!/bin/bash
# Install dependencies for protein phylogeny analysis

set -e

echo "========================================="
echo "Installing Dependencies"
echo "========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
else
    OS="unknown"
fi

echo "Detected OS: $OS"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check Python
echo "Checking Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "✓ Python $PYTHON_VERSION found"
else
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Install Python packages
echo ""
echo "Installing Python packages..."
pip3 install --user biopython numpy pandas matplotlib seaborn networkx || {
    echo "⚠ pip install failed. Trying with --break-system-packages..."
    pip3 install --user --break-system-packages biopython numpy pandas matplotlib seaborn networkx
}
echo "✓ Python packages installed"

# Check/Install bioinformatics tools
echo ""
echo "Checking bioinformatics tools..."

# CD-HIT
if command_exists cd-hit; then
    echo "✓ CD-HIT found"
else
    echo "⚠ CD-HIT not found"
    if command_exists conda; then
        echo "  Installing via conda..."
        conda install -c bioconda cd-hit -y
    else
        echo "  Please install manually: https://github.com/weizhongli/cdhit"
    fi
fi

# MAFFT
if command_exists mafft; then
    echo "✓ MAFFT found"
else
    echo "⚠ MAFFT not found"
    if command_exists conda; then
        echo "  Installing via conda..."
        conda install -c bioconda mafft -y
    elif [[ "$OS" == "linux" ]] && command_exists apt-get; then
        echo "  Installing via apt..."
        sudo apt-get install -y mafft
    elif [[ "$OS" == "mac" ]] && command_exists brew; then
        echo "  Installing via brew..."
        brew install mafft
    else
        echo "  Please install manually: https://mafft.cbrc.jp/alignment/software/"
    fi
fi

# trimAl
if command_exists trimal; then
    echo "✓ trimAl found"
else
    echo "⚠ trimAl not found"
    if command_exists conda; then
        echo "  Installing via conda..."
        conda install -c bioconda trimal -y
    elif [[ "$OS" == "linux" ]] && command_exists apt-get; then
        echo "  Installing via apt..."
        sudo apt-get install -y trimal
    elif [[ "$OS" == "mac" ]] && command_exists brew; then
        echo "  Installing via brew..."
        brew install brewsci/bio/trimal
    else
        echo "  Please install manually: http://trimal.cgenomics.org/"
    fi
fi

# IQ-TREE
if command_exists iqtree2 || command_exists iqtree; then
    echo "✓ IQ-TREE found"
else
    echo "⚠ IQ-TREE not found"
    if command_exists conda; then
        echo "  Installing via conda..."
        conda install -c bioconda iqtree -y
    else
        echo "  Downloading IQ-TREE..."
        if [[ "$OS" == "linux" ]]; then
            wget -q https://github.com/iqtree/iqtree2/releases/download/v2.2.0/iqtree-2.2.0-Linux.tar.gz
            tar -xzf iqtree-2.2.0-Linux.tar.gz
            sudo cp iqtree-2.2.0-Linux/bin/iqtree2 /usr/local/bin/ || cp iqtree-2.2.0-Linux/bin/iqtree2 ~/.local/bin/
            rm -rf iqtree-2.2.0-Linux*
            echo "  ✓ IQ-TREE installed to /usr/local/bin/ or ~/.local/bin/"
        elif [[ "$OS" == "mac" ]]; then
            wget -q https://github.com/iqtree/iqtree2/releases/download/v2.2.0/iqtree-2.2.0-MacOSX.zip
            unzip -q iqtree-2.2.0-MacOSX.zip
            sudo cp iqtree-2.2.0-MacOSX/bin/iqtree2 /usr/local/bin/ || cp iqtree-2.2.0-MacOSX/bin/iqtree2 ~/.local/bin/
            rm -rf iqtree-2.2.0-MacOSX*
            echo "  ✓ IQ-TREE installed to /usr/local/bin/ or ~/.local/bin/"
        else
            echo "  Please install manually: http://www.iqtree.org/"
        fi
    fi
fi

echo ""
echo "========================================="
echo "Installation Summary"
echo "========================================="

# Check all tools
ALL_OK=true

if command_exists python3; then
    echo "✓ Python 3"
else
    echo "✗ Python 3"
    ALL_OK=false
fi

if python3 -c "import Bio" 2>/dev/null; then
    echo "✓ BioPython"
else
    echo "✗ BioPython"
    ALL_OK=false
fi

if python3 -c "import numpy" 2>/dev/null; then
    echo "✓ NumPy"
else
    echo "✗ NumPy"
    ALL_OK=false
fi

if python3 -c "import pandas" 2>/dev/null; then
    echo "✓ Pandas"
else
    echo "✗ Pandas"
    ALL_OK=false
fi

if python3 -c "import matplotlib" 2>/dev/null; then
    echo "✓ Matplotlib"
else
    echo "✗ Matplotlib"
    ALL_OK=false
fi

if python3 -c "import seaborn" 2>/dev/null; then
    echo "✓ Seaborn"
else
    echo "✗ Seaborn"
    ALL_OK=false
fi

if python3 -c "import networkx" 2>/dev/null; then
    echo "✓ NetworkX"
else
    echo "✗ NetworkX"
    ALL_OK=false
fi

if command_exists cd-hit; then
    echo "✓ CD-HIT"
else
    echo "✗ CD-HIT"
    ALL_OK=false
fi

if command_exists mafft; then
    echo "✓ MAFFT"
else
    echo "✗ MAFFT"
    ALL_OK=false
fi

if command_exists trimal; then
    echo "✓ trimAl"
else
    echo "✗ trimAl"
    ALL_OK=false
fi

if command_exists iqtree2 || command_exists iqtree; then
    echo "✓ IQ-TREE"
else
    echo "✗ IQ-TREE"
    ALL_OK=false
fi

echo ""

if [ "$ALL_OK" = true ]; then
    echo "========================================="
    echo "✓ All dependencies installed!"
    echo "========================================="
    echo ""
    echo "Ready to use. Try:"
    echo "  bash scripts/run_full_workflow.sh input.fasta output/ \"Family Name\""
    echo ""
    echo "Or use Python directly:"
    echo "  cd scripts/python"
    echo "  python3 complete_analysis.py aligned.fasta output/"
else
    echo "========================================="
    echo "⚠ Some dependencies missing"
    echo "========================================="
    echo ""
    echo "Please install missing tools manually."
    echo "See TESTING.md for detailed instructions."
fi
