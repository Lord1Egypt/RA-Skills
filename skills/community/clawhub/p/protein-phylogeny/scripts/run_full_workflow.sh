#!/bin/bash
# Complete protein family phylogenetic analysis workflow
# Usage: bash run_full_workflow.sh input.fasta output_dir/ "Family Name"

set -e  # Exit on error

INPUT=$1
OUTPUT_DIR=$2
FAMILY_NAME=$3

if [ -z "$INPUT" ] || [ -z "$OUTPUT_DIR" ] || [ -z "$FAMILY_NAME" ]; then
    echo "Usage: bash run_full_workflow.sh input.fasta output_dir/ \"Family Name\""
    exit 1
fi

mkdir -p $OUTPUT_DIR

echo "========================================="
echo "Protein Family Phylogenetic Analysis"
echo "Family: $FAMILY_NAME"
echo "Input: $INPUT"
echo "Output: $OUTPUT_DIR"
echo "========================================="

# Stage 1: Quality Control
echo ""
echo "[1/6] Quality Control..."
bash $(dirname $0)/01_quality_control.sh $INPUT $OUTPUT_DIR/qc/
QC_FASTA=$OUTPUT_DIR/qc/final.fasta

# Stage 2: Conservation Analysis
echo ""
echo "[2/6] Conservation Analysis..."
bash $(dirname $0)/02_conservation.sh $QC_FASTA $OUTPUT_DIR/conservation/

# Stage 3: Coevolution Analysis
echo ""
echo "[3/6] Coevolution Analysis..."
bash $(dirname $0)/03_coevolution.sh $QC_FASTA $OUTPUT_DIR/coevolution/

# Stage 4: Phylogenetic Analysis
echo ""
echo "[4/6] Phylogenetic Analysis..."
bash $(dirname $0)/04_phylogeny.sh $QC_FASTA $OUTPUT_DIR/phylogeny/

# Stage 5: Visualization
echo ""
echo "[5/6] Generating Figures..."
bash $(dirname $0)/05_visualize.sh $OUTPUT_DIR $OUTPUT_DIR/figures/

# Stage 6: Report Generation
echo ""
echo "[6/6] Creating Report..."
bash $(dirname $0)/06_report.sh $OUTPUT_DIR "$FAMILY_NAME" $OUTPUT_DIR/report.md

echo ""
echo "========================================="
echo "Analysis Complete!"
echo "========================================="
echo "Results:"
echo "  - Quality control: $OUTPUT_DIR/qc/"
echo "  - Conservation: $OUTPUT_DIR/conservation/"
echo "  - Coevolution: $OUTPUT_DIR/coevolution/"
echo "  - Phylogeny: $OUTPUT_DIR/phylogeny/"
echo "  - Figures: $OUTPUT_DIR/figures/"
echo "  - Report: $OUTPUT_DIR/report.md"
echo ""
echo "Next steps:"
echo "  1. Review report: cat $OUTPUT_DIR/report.md"
echo "  2. View figures: ls $OUTPUT_DIR/figures/"
echo "  3. Upload to Feishu: lark-cli docs +create --title \"$FAMILY_NAME Analysis\" --markdown \"@$OUTPUT_DIR/report.md\""
