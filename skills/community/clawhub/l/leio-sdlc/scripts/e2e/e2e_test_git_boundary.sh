#!/bin/bash
export SDLC_TEST_MODE=true
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SANDBOX_DIR=$(mktemp -d)
mkdir -p "$SANDBOX_DIR/bin"
cat << 'INNER_EOF' > "$SANDBOX_DIR/bin/openclaw"
#!/bin/bash
exit 0
INNER_EOF
chmod +x "$SANDBOX_DIR/bin/openclaw"
export PATH="$SANDBOX_DIR/bin:$PATH"
echo "Sandbox: $SANDBOX_DIR"

cd "$SANDBOX_DIR"
# No git init here

if python3 "${PROJECT_ROOT}/scripts/orchestrator.py" --enable-exec-from-workspace --workdir "$(pwd)" --prd-file prd.md --channel "valid:id" --global-dir "$(pwd)" 2>&1 | grep -q "Git Boundary Enforcement"; then
    echo "✅ test_git_boundary.sh PASSED"
else
    echo "❌ test_git_boundary.sh FAILED: Did not enforce git boundary."
    exit 1
fi
rm -rf "$SANDBOX_DIR"
