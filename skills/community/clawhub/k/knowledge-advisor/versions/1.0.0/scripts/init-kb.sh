#!/usr/bin/env bash
# Initialize a new knowledge-advisor knowledge base directory.
# Usage: init-kb.sh [target-directory]
# Default target: ./knowledge-base

set -euo pipefail

TARGET="${1:-./knowledge-base}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(dirname "$SCRIPT_DIR")/templates"

if [ -d "$TARGET" ] && [ -f "$TARGET/_index.md" ]; then
    echo "Knowledge base already exists at $TARGET"
    echo "Books: $(find "$TARGET" -maxdepth 1 -mindepth 1 -type d | wc -l)"
    exit 0
fi

echo "Initializing knowledge base at $TARGET..."

mkdir -p "$TARGET"

TODAY=$(date +%Y-%m-%d)

# Create _index.md from template
sed "s/\[DATE\]/$TODAY/" "$TEMPLATE_DIR/_index.md" > "$TARGET/_index.md"

# Create _health.json from template
sed "s/\"last_check\": \"\"/\"last_check\": \"$TODAY\"/" "$TEMPLATE_DIR/_health.json" > "$TARGET/_health.json"

# Create _domains.json from template
cp "$TEMPLATE_DIR/_domains.json" "$TARGET/_domains.json"

# Create _cross-references.md
cat > "$TARGET/_cross-references.md" << 'EOF'
# Cross-References

Connections between frameworks across different books.

<!-- Entries added automatically after each ingestion -->
<!-- Format: -->
<!-- ## [Topic] -->
<!-- ### [Framework A] ([Book A]) ↔ [Framework B] ([Book B]) -->
<!-- **Relationship:** [complementary | overlapping | contrasting] -->
<!-- **How they connect:** [description] -->
EOF

echo "Knowledge base initialized:"
echo "  $TARGET/_index.md"
echo "  $TARGET/_health.json"
echo "  $TARGET/_domains.json"
echo "  $TARGET/_cross-references.md"
echo ""
echo "Ready to ingest your first book."
