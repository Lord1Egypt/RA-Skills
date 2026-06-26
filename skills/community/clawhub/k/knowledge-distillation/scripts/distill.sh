#!/bin/bash
#
# distill.sh - Run knowledge distillation on memory files
# Usage: ./distill.sh [memory-dir] [output-dir]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="${1:-${KNOWLEDGE_DISTILLATION_MEMORY_DIR:-$PWD}}"
OUTPUT_DIR="${2:-${KNOWLEDGE_DISTILLATION_OUTPUT_DIR:-$SKILL_DIR/dist}}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔬 Knowledge Distillation${NC}"
echo "=========================="
echo "Memory source: $MEMORY_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate dated filename
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/knowledge-distillation-$DATE.md"

# Check for existing files and increment if needed
if [[ -f "$OUTPUT_FILE" ]]; then
    COUNTER=1
    while [[ -f "${OUTPUT_FILE%.md}-$(printf "%02d" $COUNTER).md" ]]; do
        COUNTER=$((COUNTER + 1))
    done
    OUTPUT_FILE="${OUTPUT_FILE%.md}-$(printf "%02d" $COUNTER).md"
fi

echo -e "${GREEN}📄 Output file: $(basename "$OUTPUT_FILE")${NC}"
echo ""
cat > "$OUTPUT_FILE" <<EOF
# Knowledge Distillation - $DATE

## Input Summary
- Memory files: TODO
- Session/log sources: TODO
- Report files: TODO

## New Knowledge Points
### 1. TODO
- Conclusion:
- Basis:
- Value:
- Scope:

## Knowledge Leads Worth Deepening
### 1. TODO
- Current observation:
- Why worth deepening:
- Current gaps:
- Next step suggestions:

## Distillation Conclusions This Round
- Most worth retaining (1-3 points):
- Most worth tracking (1-3 leads):
EOF

echo "Draft created. To complete distillation:"
echo "1. Review source files in: $MEMORY_DIR"
echo "2. Replace TODO entries with evidence-backed knowledge points and leads"
echo "3. Keep weak signals in the leads section rather than promoting them"
echo ""
echo "Template location: $SKILL_DIR/references/output-templates.md"
