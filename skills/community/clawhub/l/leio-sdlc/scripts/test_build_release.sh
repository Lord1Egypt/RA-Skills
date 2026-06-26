#!/bin/bash
set -eo pipefail

echo "Running test_build_release.sh..."

TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

BUILD_SCRIPT="$(pwd)/scripts/build_release.sh"

cd "$TEST_DIR"

# Create dummy .release_ignore
cat <<EOF > .release_ignore
tests/
docs/
EOF

# Create dummy files
touch .gitignore
mkdir -p scripts docs tests
touch SKILL.md scripts/main.py docs/PRD.md tests/test.sh

# Run the build script
bash "$BUILD_SCRIPT" > /dev/null

# Assertions
if [ ! -f ".dist/SKILL.md" ]; then
    echo "❌ Error: .dist/SKILL.md not found!"
    exit 1
fi

if [ ! -f ".dist/scripts/main.py" ]; then
    echo "❌ Error: .dist/scripts/main.py not found!"
    exit 1
fi

if [ -d ".dist/docs" ] || [ -f ".dist/docs/PRD.md" ]; then
    echo "❌ Error: .dist/docs/ should not exist!"
    exit 1
fi

if [ -d ".dist/tests" ] || [ -f ".dist/tests/test.sh" ]; then
    echo "❌ Error: .dist/tests/ should not exist!"
    exit 1
fi

echo "✅ test_build_release.sh works as expected."
