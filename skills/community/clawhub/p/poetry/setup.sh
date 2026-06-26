#!/bin/bash
# Poetry Skill - Data Setup Script
# Downloads the chinese-poetry dataset into the data/ directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/data"

if [ -d "$DATA_DIR" ] && [ "$(ls -A $DATA_DIR 2>/dev/null)" ]; then
    echo "✅ Data directory already exists and is not empty: $DATA_DIR"
    echo "   To re-download, remove the data/ directory first and run this script again."
    exit 0
fi

echo "📥 Downloading chinese-poetry dataset..."
echo "   Source: https://github.com/chinese-poetry/chinese-poetry"
echo ""

git clone --depth 1 https://github.com/chinese-poetry/chinese-poetry.git "$DATA_DIR"

# Clean up unnecessary files
echo "🧹 Cleaning up unnecessary files..."
rm -rf "$DATA_DIR/.git" \
       "$DATA_DIR/.github" \
       "$DATA_DIR/.gitignore" \
       "$DATA_DIR/.travis.yml" \
       "$DATA_DIR/_config.yml" \
       "$DATA_DIR/images" \
       "$DATA_DIR/loader" \
       "$DATA_DIR/rank" \
       "$DATA_DIR/test_poetry.py" \
       "$DATA_DIR/requirements.txt"

echo ""
echo "✅ Data setup complete!"
echo "   Location: $DATA_DIR"
echo "   Size: $(du -sh "$DATA_DIR" | cut -f1)"
echo "   Files: $(find "$DATA_DIR" -type f -name '*.json' | wc -l | tr -d ' ') JSON files"
