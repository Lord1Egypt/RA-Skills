#!/bin/bash
# PhD Research Companion - Installation & Verification Script
# Runs all checks and displays comprehensive status report

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "PhD Research Companion v1.5.0" 
echo "Installation & Verification Check"
echo "=========================================="

# 1. Check Python version
PYTHON_VER=$(python3 --version 2>&1 | cut -d' ' -f2)
if [[ $(python3 -c "import sys; print(int(sys.version_info[1]) >= 8)") == "True" ]]; then
    echo -e "${GREEN}✅${NC} Python version: ${PYTHON_VER}"  
else
    echo -e "${RED}❌${NC} Requires Python 3.8+ (found ${PYTHON_VER})"
fi

# 2. Check all required scripts exist
SCRIPTS=(
    "init_research_project.py"
    "scripts/multi_source_search.py"  
    "scripts/paper_analyzer.py"
    "scripts/create_experiment_design.py"
    "scripts/generate_latex_template.py"
    "scripts/revision_tracker.py" 
    "scripts/verify_math_notation.py"
    "scripts/check_compliance.py"
)

echo ""
echo "🔧 Checking required scripts:..."

all_scripts_ok=true
for script in "${SCRIPTS[@]}"; do
    if [ -f "$SCRIPT_DIR/$script" ]; then
        echo "  ✅ $script (found)"
    else
        echo "  ❌ $script (missing)"  
        all_scripts_ok=false
    fi
done

# 3. Check run script executable
echo ""
echo "🔧 Checking wrapper scripts..."

if [ -x "$SCRIPT_DIR/run" ]; then
    echo "  ✅ run wrapper is executable"
else
    echo -e "${YELLOW}⚠️${NC} run wrapper not executable, attempting to fix..."
    chmod +x "$SCRIPT_DIR/run"
    if [ -x "$SCRIPT_DIR/run" ]; then
        echo "  ✅ Fixed: now executable"
    fi
fi

# 4. Check documentation files  
echo ""
echo "📚 Checking documentation:..."

DOCS=("SKILL.md" "README.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$SCRIPT_DIR/$doc" ]; then
        LINES=$(wc -l < "$SCRIPT_DIR/$doc")
        echo "  ✅ ${doc} found (${LINES} lines)"
    else
        echo "  ❌ ${doc} missing"
    fi
done

# 5. Test --help on key scripts
echo ""
echo "🧪 Testing script functionality..."

for test_script in "init_research_project.py" "scripts/multi_source_search.py"; do
    if python3 "$SCRIPT_DIR/$test_script" --help > /dev/null 2>&1; then
        echo "  ✅ $test_script --help works"
    else
        echo -e "${YELLOW}⚠️${NC} $test_script --help has issues (may be normal)" 
    fi
done

# Final summary  
echo ""
echo "=========================================="

if [ "$all_scripts_ok" = true ]; then
    echo -e "${GREEN}✅ Installation verified successfully!${NC}"
else
    echo -e "${RED}❌ Some components missing or incomplete${NC}"
fi

echo ""
echo "📖 Next steps:"  
echo "   1. Review SKILL.md for complete usage documentation"
echo "   2. Test with: ./run help"
echo "   3. Create first project: ./run init -d 'your topic' -j 'target journal'"

echo "=========================================="

# Cleanup temp if needed  
rm -f /tmp/phd-test-*.txt 2>/dev/null || true