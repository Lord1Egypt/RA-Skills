#!/bin/bash
# Step 2: Multiple Sequence Alignment + Phylogenetic Tree
set -e

PROJECT="/root/autodl-tmp/ou_a1d19d5984eecd78f231c50f774eddb0/IRED_phylogeny"
FASTA="$PROJECT/sequences/ired_sequences.fasta"
ALIGN="$PROJECT/alignment"
TREES="$PROJECT/trees"
LOGS="$PROJECT/logs"

echo "============================================================"
echo "Step 2: MSA + Phylogenetic Tree"
echo "============================================================"

# Step 2a: Multiple Sequence Alignment with MAFFT
echo ""
echo "[1] Running MAFFT alignment..."
echo "    Input: $(grep -c '^>' $FASTA) sequences"

mafft --auto --thread $(nproc) "$FASTA" > "$ALIGN/ired_aligned.fasta" 2>&1

echo "    Done! Aligned length: $(head -2 $ALIGN/ired_aligned.fasta | tail -1 | wc -c) characters"

# Step 2b: Trim alignment with trimAl (optional, skip if not installed)
if command -v trimal &> /dev/null; then
    echo "[2] Trimming alignment with trimAl..."
    trimal -automated1 -in "$ALIGN/ired_aligned.fasta" -out "$ALIGN/ired_aligned_trimmed.fasta"
else
    echo "[2] trimAl not installed, skipping trim"
    cp "$ALIGN/ired_aligned.fasta" "$ALIGN/ired_aligned_trimmed.fasta"
fi

# Step 2c: Build tree with FastTree
echo "[3] Building phylogenetic tree (FastTree)..."
echo "    Method: Maximum Likelihood (approximate)"

fasttree -gamma -nt "$ALIGN/ired_aligned_trimmed.fasta" > "$TREES/ired_tree.nwk" 2>"$LOGS/fasttree.log"

echo "    Tree saved: $TREES/ired_tree.nwk"
echo "    Log: $LOGS/fasttree.log"

# Step 2d: Build tree with IQ-TREE if available (better support values)
if command -v iqtree &> /dev/null; then
    echo "[4] Building ML tree with IQ-TREE (with bootstrap)..."
    iqtree -s "$ALIGN/ired_aligned_trimmed.fasta" -m TEST -bb 1000 -nt AUTO -pre "$TREES/ired_iqtree" 2>"$LOGS/iqtree.log"
    echo "    IQ-TREE tree: $TREES/ired_iqtree.treefile"
else
    echo "[4] IQ-TREE not installed, FastTree only"
fi

echo ""
echo "=== Step 2 Complete ==="
