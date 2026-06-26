#!/bin/sh
# test-wizard.sh — End-to-end wizard smoke test.
# Runs persona-create.sh with pre-filled answers and validates output.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEST_WORKSPACE="$(mktemp -d)"
TEST_CONFIG="$TEST_WORKSPACE/openclaw.json"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    desc="$1"
    shift
    if "$@" > /dev/null 2>&1; then
        printf "${GREEN}  ✓ %s${NC}\n" "$desc"
        PASS=$((PASS + 1))
    else
        printf "${RED}  ✗ %s${NC}\n" "$desc"
        FAIL=$((FAIL + 1))
    fi
}

check_file_exists() {
    check "File exists: $1" test -f "$TEST_WORKSPACE/$1"
}

check_file_contains() {
    check "File $1 contains '$2'" grep -q "$2" "$TEST_WORKSPACE/$1"
}

cleanup() {
    rm -rf "$TEST_WORKSPACE"
}
trap cleanup EXIT

printf "${BOLD}🧪 Wizard Smoke Test${NC}\n\n"

# Initialize empty config
echo '{}' > "$TEST_CONFIG"

# Run generators directly (non-interactive test)
printf "  Running generators...\n\n"

# Generate SOUL.md from companion archetype
python3 "$ENGINE_DIR/scripts/generate-soul.py" \
    --archetype companion \
    --name "TestBot" \
    --emoji "🤖" \
    --creature "Test AI assistant" \
    --user-name "Tester" \
    --output "$TEST_WORKSPACE/SOUL.md"

# Generate USER.md
python3 "$ENGINE_DIR/scripts/generate-user.py" \
    --name "Tester" \
    --call-names "Tester, buddy" \
    --timezone "America/New_York" \
    --notes "Just a test user" \
    --output "$TEST_WORKSPACE/USER.md"

# Generate IDENTITY.md
python3 "$ENGINE_DIR/scripts/generate-identity.py" \
    --name "TestBot" \
    --emoji "🤖" \
    --creature "Test AI assistant" \
    --vibe "Friendly and reliable" \
    --nickname "TB" \
    --output "$TEST_WORKSPACE/IDENTITY.md"

# Generate memory infrastructure
python3 "$ENGINE_DIR/scripts/generate-memory.py" \
    --name "TestBot" \
    --emoji "🤖" \
    --creature "Test AI assistant" \
    --user-name "Tester" \
    --workspace "$TEST_WORKSPACE"

# Configure voice
python3 "$ENGINE_DIR/scripts/voice-setup.py" \
    --provider builtin \
    --voice nova \
    --config "$TEST_CONFIG" \
    --non-interactive

# Configure image
python3 "$ENGINE_DIR/scripts/image-setup.py" \
    --provider gemini \
    --description "Friendly robot" \
    --config "$TEST_CONFIG" \
    --non-interactive

printf "\n  Validating output...\n\n"

# Check all files exist
check_file_exists "SOUL.md"
check_file_exists "USER.md"
check_file_exists "IDENTITY.md"
check_file_exists "MEMORY.md"
check_file_exists "HEARTBEAT.md"
check_file_exists "AGENTS.md"
check "Memory directory exists" test -d "$TEST_WORKSPACE/memory"

# Check file contents
check_file_contains "SOUL.md" "TestBot"
check_file_contains "SOUL.md" "Core Truths"
check_file_contains "SOUL.md" "Continuity"
check_file_contains "USER.md" "Tester"
check_file_contains "USER.md" "America/New_York"
check_file_contains "IDENTITY.md" "TestBot"
check_file_contains "IDENTITY.md" "TB"
check_file_contains "MEMORY.md" "TestBot"
check_file_contains "HEARTBEAT.md" "MEMORY.md"
check_file_contains "AGENTS.md" "TestBot"

# Check config
check "Config file exists" test -f "$TEST_CONFIG"
check "Config has voice" python3 -c "import json; c=json.load(open('$TEST_CONFIG')); assert c['messages']['tts']['provider'] == 'builtin'"
check "Config has image" python3 -c "import json; c=json.load(open('$TEST_CONFIG')); assert c['persona']['image']['provider'] == 'gemini'"

# Check daily note
TODAY=$(date +%Y-%m-%d)
check "Daily note exists" test -f "$TEST_WORKSPACE/memory/$TODAY.md"

printf "\n${BOLD}Results: ${GREEN}$PASS passed${NC}, "
if [ "$FAIL" -gt 0 ]; then
    printf "${RED}$FAIL failed${NC}\n"
    exit 1
else
    printf "0 failed\n"
fi
printf "${GREEN}✅ All smoke tests passed!${NC}\n"
