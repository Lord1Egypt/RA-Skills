#!/bin/bash
# Phylogenetic Analysis Script
# Builds maximum likelihood tree with IQ-TREE

set -e

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <aligned.fasta> <output_dir>"
    echo ""
    echo "Example: $0 aligned.fasta output/"
    exit 1
fi

ALIGNED_FASTA=$1
OUTPUT_DIR=$2

# Create output directory
mkdir -p "$OUTPUT_DIR/phylogeny"

echo "========================================="
echo "Phylogenetic Analysis"
echo "========================================="
echo "Input: $ALIGNED_FASTA"
echo "Output: $OUTPUT_DIR/phylogeny/"
echo ""

# Check if input exists
if [ ! -f "$ALIGNED_FASTA" ]; then
    echo "Error: Input file not found: $ALIGNED_FASTA"
    exit 1
fi

# Check if IQ-TREE is installed
if ! command -v iqtree2 &> /dev/null && ! command -v iqtree &> /dev/null; then
    echo "Error: IQ-TREE not found. Please install it first:"
    echo "  conda install -c bioconda iqtree"
    echo "  or download from: http://www.iqtree.org/"
    exit 1
fi

# Determine IQ-TREE command
if command -v iqtree2 &> /dev/null; then
    IQTREE="iqtree2"
else
    IQTREE="iqtree"
fi

echo "Using: $IQTREE"
echo ""

# Copy input to output directory
cp "$ALIGNED_FASTA" "$OUTPUT_DIR/phylogeny/aligned.fasta"

cd "$OUTPUT_DIR/phylogeny"

# Step 1: Model selection
echo "Step 1: Model selection with ModelFinder..."
echo "-------------------------------------------"
$IQTREE -s aligned.fasta -m MFP -nt AUTO --prefix modelfinder -quiet

BEST_MODEL=$(grep "Best-fit model:" modelfinder.iqtree | awk '{print $3}')
echo "✓ Best model: $BEST_MODEL"
echo ""

# Step 2: Maximum likelihood tree with bootstrap
echo "Step 2: Building ML tree with UFBoot2..."
echo "-------------------------------------------"
echo "This may take 10-30 minutes depending on dataset size..."
echo ""

$IQTREE -s aligned.fasta \
    -m "$BEST_MODEL" \
    -bb 1000 \
    -nt AUTO \
    -seed 12345 \
    --prefix tree \
    -wbtl \
    -quiet

echo ""
echo "✓ Tree building complete"
echo ""

# Step 3: Extract statistics
echo "Step 3: Extracting statistics..."
echo "-------------------------------------------"

# Extract log-likelihood
LOG_LIKELIHOOD=$(grep "BEST SCORE FOUND" tree.iqtree | awk '{print $5}')

# Extract tree length
TREE_LENGTH=$(grep "Total tree length" tree.iqtree | awk '{print $4}')

# Extract bootstrap convergence
BOOTSTRAP_CONV=$(grep "Bootstrap convergence" tree.iqtree | awk '{print $4}' || echo "N/A")

# Count sequences
NUM_SEQS=$(grep -c ">" aligned.fasta)

# Get alignment length
ALN_LENGTH=$(head -2 aligned.fasta | tail -1 | tr -d '\n' | wc -c)

# Create summary file
cat > tree_summary.txt << EOF
Phylogenetic Analysis Summary
=============================

Input:
  Sequences: $NUM_SEQS
  Alignment length: $ALN_LENGTH

Model Selection:
  Best model: $BEST_MODEL

Tree Statistics:
  Log-likelihood: $LOG_LIKELIHOOD
  Tree length: $TREE_LENGTH
  Bootstrap convergence: $BOOTSTRAP_CONV

Bootstrap Support:
  (See tree.contree for consensus tree with support values)

Output Files:
  tree.treefile       - ML tree (best tree)
  tree.contree        - Consensus tree with bootstrap support
  tree.iqtree         - Full analysis log
  modelfinder.iqtree  - Model selection log
EOF

echo "✓ Summary saved to: tree_summary.txt"
echo ""

# Step 4: Analyze bootstrap support
echo "Step 4: Analyzing bootstrap support..."
echo "-------------------------------------------"

# Create Python script to analyze bootstrap
cat > analyze_bootstrap.py << 'PYTHON_EOF'
#!/usr/bin/env python3
import sys
from Bio import Phylo

tree_file = "tree.contree"
tree = Phylo.read(tree_file, "newick")

# Extract bootstrap values
bootstrap_values = []
for clade in tree.find_clades():
    if clade.confidence is not None:
        bootstrap_values.append(clade.confidence)

if len(bootstrap_values) == 0:
    print("No bootstrap values found")
    sys.exit(0)

# Calculate statistics
import numpy as np
bootstrap_values = np.array(bootstrap_values)

strong = np.sum(bootstrap_values >= 95)
moderate = np.sum((bootstrap_values >= 70) & (bootstrap_values < 95))
weak = np.sum(bootstrap_values < 70)
total = len(bootstrap_values)

print(f"Bootstrap Support Distribution:")
print(f"  Strong (≥95%): {strong} ({strong/total*100:.1f}%)")
print(f"  Moderate (70-95%): {moderate} ({moderate/total*100:.1f}%)")
print(f"  Weak (<70%): {weak} ({weak/total*100:.1f}%)")
print(f"  Total branches: {total}")
print()
print(f"  Mean: {np.mean(bootstrap_values):.1f}%")
print(f"  Median: {np.median(bootstrap_values):.1f}%")
print(f"  Min: {np.min(bootstrap_values):.1f}%")
print(f"  Max: {np.max(bootstrap_values):.1f}%")

# Save to file
with open("bootstrap_stats.txt", "w") as f:
    f.write("Bootstrap Support Statistics\n")
    f.write("="*60 + "\n")
    f.write(f"Strong (≥95%): {strong} ({strong/total*100:.1f}%)\n")
    f.write(f"Moderate (70-95%): {moderate} ({moderate/total*100:.1f}%)\n")
    f.write(f"Weak (<70%): {weak} ({weak/total*100:.1f}%)\n")
    f.write(f"Total branches: {total}\n")
    f.write(f"\n")
    f.write(f"Mean: {np.mean(bootstrap_values):.1f}%\n")
    f.write(f"Median: {np.median(bootstrap_values):.1f}%\n")
    f.write(f"Min: {np.min(bootstrap_values):.1f}%\n")
    f.write(f"Max: {np.max(bootstrap_values):.1f}%\n")
PYTHON_EOF

python3 analyze_bootstrap.py

echo ""
echo "✓ Bootstrap statistics saved to: bootstrap_stats.txt"
echo ""

cd - > /dev/null

echo "========================================="
echo "Phylogenetic analysis complete!"
echo "========================================="
echo "Output files:"
echo "  - $OUTPUT_DIR/phylogeny/tree.treefile (ML tree)"
echo "  - $OUTPUT_DIR/phylogeny/tree.contree (consensus tree)"
echo "  - $OUTPUT_DIR/phylogeny/tree_summary.txt (summary)"
echo "  - $OUTPUT_DIR/phylogeny/bootstrap_stats.txt (bootstrap stats)"
echo ""
echo "Next steps:"
echo "  1. Visualize tree with FigTree or R"
echo "  2. Check bootstrap support (should be >70% for most branches)"
echo "  3. Verify bootstrap convergence (should be >0.99)"
echo ""
