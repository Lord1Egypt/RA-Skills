#!/bin/bash
set -e
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SANDBOX_DIR=$(mktemp -d)

cd "$SANDBOX_DIR"
git init > /dev/null
git config user.name "Test"
git config user.email "test@example.com"
git commit --allow-empty -m "init"
git checkout -b feature/test
mkdir -p playbooks TEMPLATES scripts
echo "playbook" > playbooks/coder_playbook.md
cp ${PROJECT_ROOT}/scripts/spawn_coder.py scripts/
cp ${PROJECT_ROOT}/scripts/agent_driver.py scripts/

# Create a fake openclaw wrapper to inspect arguments
cat << 'INNER_EOF' > scripts/openclaw
#!/bin/bash
# We write to a file in the parent directory to ensure it survives
LOG_FILE="$(cd "$(dirname "$0")/.." && pwd)/openclaw.log"
echo "OPENCLAW_CALLED_WITH: $*" >> "$LOG_FILE"

# Look for /tmp/sdlc_prompt_ in ANY argument
for arg in "$@"; do
    if [[ "$arg" == *"/tmp/sdlc_prompt_"* ]]; then
        # Capture the full path
        FILE=$(echo "$arg" | grep -oE '/tmp/sdlc_prompt_[^ ]+\.txt')
        if [ -n "$FILE" ]; then
            if [ -f "$FILE" ]; then
                PERMS=$(stat -c "%a" "$FILE")
                echo "FILE:$FILE:PERMS:$PERMS" >> "$LOG_FILE"
            else
                echo "FILE:$FILE:NOT_FOUND" >> "$LOG_FILE"
            fi
        fi
    fi
done
INNER_EOF
chmod +x scripts/openclaw

# Run spawner with PATH override
echo "contract" > pr.md
echo "prd" > prd.md
export PATH="$(pwd)/scripts:$PATH"
python3 scripts/spawn_coder.py --pr-file pr.md --prd-file prd.md --workdir "$(pwd)" --global-dir "$(pwd)" > spawner.log 2>&1 || true

cat spawner.log
echo "--- openclaw.log ---"
cat openclaw.log || echo "openclaw.log not found"

if ! grep -q "PERMS:600" openclaw.log; then
    echo "❌ test_secure_prompt.sh FAILED: Secure prompt not verified in openclaw.log."
    exit 1
fi

# Check for cleanup
if ls /tmp/sdlc_prompt_*.txt > /dev/null 2>&1; then
    echo "❌ test_secure_prompt.sh FAILED: Zombie files found in /tmp."
    ls /tmp/sdlc_prompt_*.txt
    exit 1
fi

echo "✅ test_secure_prompt.sh PASSED"
rm -rf "$SANDBOX_DIR"
