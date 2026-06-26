#!/bin/bash
# Test script for Mermaid skill

set -e

echo "🎨 Testing Mermaid diagram generation..."

# Create test directory
TEST_DIR=$(mktemp -d)
echo "📁 Test directory: $TEST_DIR"

# Create sample flowchart
cat > "$TEST_DIR/test.mmd" << 'EOF'
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Success!]
    B -->|No| D[Debug]
    D --> A
    C --> E[End]
EOF

echo "📝 Created test diagram definition"

# Generate PNG
mmdc -i "$TEST_DIR/test.mmd" -o "$TEST_DIR/test.png" -t dark -b transparent -s 2

# Check if output exists
if [ -f "$TEST_DIR/test.png" ]; then
    echo "✅ Diagram generated successfully!"
    echo "📍 Output: $TEST_DIR/test.png"
    ls -lh "$TEST_DIR/test.png"
    exit 0
else
    echo "❌ Failed to generate diagram"
    exit 1
fi
