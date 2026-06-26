#!/bin/bash
set -e

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Sandbox created at $TEMP_DIR"
cd "$TEMP_DIR"

# Paths
SPAWN_REVIEWER="/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_reviewer.py"
MOCK_GLOBAL="/tmp/mock_global_reviewer"
RUN_DIR="$MOCK_GLOBAL/.sdlc_runs/dummy_prd"
mkdir -p "$TEMP_DIR/TEMPLATES"
touch "$TEMP_DIR/TEMPLATES/review_report.json.template"

echo "mock pr" > pr.md
echo "mock diff" > diff.txt

# We need to mock openclaw binary
mkdir -p "$TEMP_DIR/bin"
mkdir -p "$RUN_DIR"
export PATH="$TEMP_DIR/bin:$PATH"

echo "=== T1: Agent misses artifact (Fail-Fast) ==="
# Mock openclaw to do nothing
cat << 'EOF' > "$TEMP_DIR/bin/openclaw"
#!/bin/bash
echo "Agent executed but did not write file"
exit 0
EOF
chmod +x "$TEMP_DIR/bin/openclaw"

if python3 "$SPAWN_REVIEWER" --pr-file pr.md --diff-target HEAD --workdir . --override-diff-file diff.txt --run-dir "$RUN_DIR" --out-file "$RUN_DIR/review_report.json" --global-dir "$MOCK_GLOBAL" 2>stderr.log; then
    echo "❌ T1 Failed: python script should have exited with 1"
    exit 1
fi

if grep -q "\[FATAL\].*review_report.json" stderr.log; then
    echo "✅ T1 Passed: Caught missing artifact"
else
    echo "❌ T1 Failed: Did not print FATAL error"
    cat stderr.log
    exit 1
fi

echo "=== T2: Agent creates artifact ==="
# Mock openclaw to create the file
cat << EOF > "$TEMP_DIR/bin/openclaw"
#!/bin/bash
echo "Agent executed and wrote file"
# We parse the workdir from args? No, the working directory is already lock to workdir.
touch "$RUN_DIR/review_report.json"
exit 0
EOF
chmod +x "$TEMP_DIR/bin/openclaw"

if ! python3 "$SPAWN_REVIEWER" --pr-file pr.md --diff-target HEAD --workdir . --override-diff-file diff.txt --run-dir "$RUN_DIR" --out-file "$RUN_DIR/review_report.json" --global-dir "$MOCK_GLOBAL"; then
    echo "❌ T2 Failed: python script should have exited with 0"
    exit 1
fi
echo "✅ T2 Passed: Allowed successful run"
