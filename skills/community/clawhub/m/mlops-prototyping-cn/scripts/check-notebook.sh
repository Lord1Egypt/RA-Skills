#!/bin/bash
# Check notebook structure and best practices

NOTEBOOK="${1:-*.ipynb}"

echo "🔍 Checking notebook: $NOTEBOOK"

# Check if notebook exists
if [ ! -f "$NOTEBOOK" ]; then
    echo "❌ Notebook not found"
    exit 1
fi

# Check required sections
python3 << EOF
import json
import sys

with open("$NOTEBOOK") as f:
    nb = json.load(f)

cells = nb['cells']
markdown_cells = [c for c in cells if c['cell_type'] == 'markdown']
code_cells = [c for c in cells if c['cell_type'] == 'code']

# Check structure
checks = {
    'Title (H1)': False,
    'Imports': False,
    'Config/Constants': False,
    'Data Loading': False,
}

for cell in markdown_cells:
    text = ''.join(cell['source'])
    if text.startswith('# '):
        checks['Title (H1)'] = True
    if 'import' in text.lower():
        checks['Imports'] = True

for cell in code_cells:
    text = ''.join(cell['source'])
    if 'import' in text:
        checks['Imports'] = True
    if any(kw in text for kw in ['RANDOM_STATE', 'DATA_PATH', 'CONFIG']):
        checks['Config/Constants'] = True
    if any(kw in text for kw in ['read_csv', 'read_parquet', 'load']):
        checks['Data Loading'] = True

print("\n📊 Structure Check:")
for check, passed in checks.items():
    status = "✅" if passed else "❌"
    print(f"  {status} {check}")

# Check for anti-patterns
anti_patterns = {
    'Magic numbers in code': False,
    'Hardcoded paths': False,
}

for cell in code_cells[1:]:  # Skip first cell (usually imports)
    text = ''.join(cell['source'])
    # Simple heuristics
    if any(char.isdigit() for char in text) and 'RANDOM_STATE' not in text:
        anti_patterns['Magic numbers in code'] = True

print("\n⚠️  Anti-patterns:")
for pattern, found in anti_patterns.items():
    status = "❌" if found else "✅"
    print(f"  {status} {pattern}")

sys.exit(0 if all(checks.values()) else 1)
EOF

echo ""
echo "✅ Notebook check complete"
