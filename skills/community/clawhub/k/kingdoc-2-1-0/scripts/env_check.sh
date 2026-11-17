#!/usr/bin/env bash
# KingDoc 环境检查脚本

set -e

echo "KingDoc Environment Check"
echo "========================="

ERRORS=0

# Check Python
if command -v python3 &>/dev/null; then
    echo "[OK] Python: $(python3 --version)"
elif command -v python &>/dev/null; then
    echo "[OK] Python: $(python --version)"
else
    echo "[FAIL] Python not found"
    ERRORS=$((ERRORS + 1))
fi

# Check pip
if command -v pip3 &>/dev/null || command -v pip &>/dev/null; then
    echo "[OK] pip: available"
else
    echo "[FAIL] pip not found"
    ERRORS=$((ERRORS + 1))
fi

# Check virtual env
if [ -d ".venv" ]; then
    echo "[OK] .venv exists"
else
    echo "[WARN] .venv not found - run setup.sh first"
fi

# Check config
if [ -f "config.json" ]; then
    echo "[OK] config.json exists"
else
    echo "[FAIL] config.json not found - run setup.sh first"
    ERRORS=$((ERRORS + 1))
fi

# Check dependencies
python3 -c "import requests" 2>/dev/null && echo "[OK] requests" || { echo "[FAIL] requests"; ERRORS=$((ERRORS + 1)); }
python3 -c "import docx" 2>/dev/null && echo "[OK] python-docx" || { echo "[FAIL] python-docx"; ERRORS=$((ERRORS + 1)); }
python3 -c "import pptx" 2>/dev/null && echo "[OK] python-pptx" || { echo "[FAIL] python-pptx"; ERRORS=$((ERRORS + 1)); }
python3 -c "import yaml" 2>/dev/null && echo "[OK] pyyaml" || { echo "[FAIL] pyyaml"; ERRORS=$((ERRORS + 1)); }

echo ""
echo "========================="
if [ $ERRORS -eq 0 ]; then
    echo "ALL CHECKS PASSED"
    exit 0
else
    echo "FAILED CHECKS: $ERRORS"
    exit 1
fi
