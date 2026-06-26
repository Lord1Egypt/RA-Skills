#!/bin/bash
# Test script for PhyloTree v2.0
# Tests all components and generates a small example

set -e  # Exit on error

echo "========================================================================"
echo "PhyloTree v2.0 - Component Test"
echo "========================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR="/root/autodl-tmp/phylo-tree-test"
mkdir -p "$TEST_DIR"

echo "Test directory: $TEST_DIR"
echo ""

# ============================================================================
# Test 1: Environment Check
# ============================================================================

echo "Test 1: Checking environment..."

# Activate conda environment
source /root/miniconda3/etc/profile.d/conda.sh
conda activate r43

# Check tools
TOOLS=("iqtree" "mafft" "trimal" "cd-hit")
ALL_OK=true

for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo -e "  ${GREEN}✓${NC} $tool found"
    else
        echo -e "  ${RED}✗${NC} $tool NOT found"
        ALL_OK=false
    fi
done

# Check R packages
echo "  Checking R packages..."
R --quiet --no-save -e '
packages <- c("ape", "ggtree", "ggplot2", "patchwork", "dplyr")
missing <- packages[!sapply(packages, requireNamespace, quietly=TRUE)]
if (length(missing) > 0) {
    cat("Missing R packages:", paste(missing, collapse=", "), "\n")
    quit(status=1)
} else {
    cat("  ✓ All R packages available\n")
}
' 2>&1 | grep -v "^>" | grep -v "^+"

if [ $? -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} R packages OK"
else
    echo -e "  ${RED}✗${NC} R packages missing"
    ALL_OK=false
fi

if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}✓ Environment check passed${NC}"
else
    echo -e "${RED}✗ Environment check failed${NC}"
    exit 1
fi

echo ""

# ============================================================================
# Test 2: Create Test Dataset
# ============================================================================

echo "Test 2: Creating test dataset..."

# Create a small test FASTA file (10 sequences)
cat > "$TEST_DIR/test_sequences.fasta" << 'EOF'
>P12345|Escherichia_coli|Test_enzyme_1
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>Q98765|Pseudomonas_aeruginosa|Test_enzyme_2
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>A12345|Bacillus_subtilis|Test_enzyme_3
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>B67890|Staphylococcus_aureus|Test_enzyme_4
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>C11111|Salmonella_enterica|Test_enzyme_5
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>D22222|Klebsiella_pneumoniae|Test_enzyme_6
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>E33333|Vibrio_cholerae|Test_enzyme_7
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>F44444|Streptomyces_coelicolor|Test_enzyme_8
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>G55555|Mycobacterium_tuberculosis|Test_enzyme_9
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
>H66666|Clostridium_difficile|Test_enzyme_10
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
EOF

echo -e "${GREEN}✓ Test dataset created (10 sequences)${NC}"
echo ""

# ============================================================================
# Test 3: Run Pipeline (Fast Mode)
# ============================================================================

echo "Test 3: Running pipeline (fast mode for testing)..."

cd /root/.agents/skills/phylo-tree

python3 scripts/run_v2.py \
    --fasta "$TEST_DIR/test_sequences.fasta" \
    --output "$TEST_DIR/output" \
    --threads 4 \
    --bootstrap 1000 \
    --skip-dedup \
    2>&1 | tee "$TEST_DIR/pipeline.log"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pipeline completed successfully${NC}"
else
    echo -e "${RED}✗ Pipeline failed${NC}"
    exit 1
fi

echo ""

# ============================================================================
# Test 4: Verify Outputs
# ============================================================================

echo "Test 4: Verifying outputs..."

OUTPUT_DIR="$TEST_DIR/output"
REQUIRED_FILES=(
    "trees/phylo.treefile"
    "trees/phylo_rooted.nwk"
    "figures/fig1_main_tree.pdf"
    "alignment/aligned.fasta"
    "alignment/trimmed.fasta"
)

ALL_OK=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$OUTPUT_DIR/$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file NOT found"
        ALL_OK=false
    fi
done

if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}✓ All required files generated${NC}"
else
    echo -e "${RED}✗ Some files missing${NC}"
    exit 1
fi

echo ""

# ============================================================================
# Summary
# ============================================================================

echo "========================================================================"
echo "Test Summary"
echo "========================================================================"
echo ""
echo -e "${GREEN}✓ All tests passed!${NC}"
echo ""
echo "Test outputs:"
echo "  - Test directory: $TEST_DIR"
echo "  - Pipeline output: $OUTPUT_DIR"
echo "  - Tree file: $OUTPUT_DIR/trees/phylo_rooted.nwk"
echo "  - Figures: $OUTPUT_DIR/figures/"
echo ""
echo "You can now:"
echo "  1. View tree: cat $OUTPUT_DIR/trees/phylo_rooted.nwk"
echo "  2. Check figures: ls $OUTPUT_DIR/figures/"
echo "  3. Review logs: cat $TEST_DIR/pipeline.log"
echo ""
echo "========================================================================"
