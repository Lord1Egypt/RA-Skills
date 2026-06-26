#!/bin/bash
set -e

echo "Starting E2E Manager Queue Polling Test..."

SANDBOX="$(pwd)/tests/manager_sandbox_$$"
GLOBAL_MOCK="/tmp/mock_sdlc_global_$$"
trap 'cd / && [[ -n "$SANDBOX" ]] && rm -rf "$SANDBOX" && rm -rf "$GLOBAL_MOCK"' EXIT
mkdir -p "$SANDBOX"
cd "$SANDBOX"

JOB_DIR="$GLOBAL_MOCK/.sdlc_runs/Feature_X"
mkdir -p "$JOB_DIR"
echo "status: open" > "$JOB_DIR/PR_001_DB.md"
echo "status: open" > "$JOB_DIR/PR_002_API.md"
echo "status: open" > "$JOB_DIR/PR_003_UI.md"

mkdir -p docs/PRDs
touch docs/PRDs/PRD_Feature_X.md

mkdir -p scripts
cat << 'MOCK' > scripts/spawn_coder.py
#!/usr/bin/env python3
print("[CODER_DONE] Preflight passed.")
MOCK

cat << 'MOCK' > scripts/spawn_reviewer.py
#!/usr/bin/env python3
print("{\"status\": \"APPROVED\", \"comments\": \"Review passed.\"}")
MOCK

cat << 'MOCK' > scripts/merge_code.py
#!/usr/bin/env python3
print("[MERGED] Code merged successfully.")
MOCK

chmod +x scripts/*.py

cp /root/.openclaw/workspace/projects/leio-sdlc/scripts/get_next_pr.py scripts/
cp /root/.openclaw/workspace/projects/leio-sdlc/scripts/update_pr_status.py scripts/

# Start Manager LLM
export SDLC_TEST_MODE=true
python3 /root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_manager.py --job-dir "$JOB_DIR" --workdir "$(pwd)"

# Assert all PRs are closed
for pr in PR_001_DB.md PR_002_API.md PR_003_UI.md; do
    if ! grep -q "status: closed" "$JOB_DIR/$pr"; then
        echo "❌ FAILED: $pr is not closed!"
        rm -rf "$SANDBOX"
        exit 1
    fi
done

echo "✅ ALL MANAGER E2E MOCK TESTS PASSED!"
exit 0
