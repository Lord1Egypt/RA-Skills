#!/bin/sh
# test-export-import.sh — Round-trip export/import test.
# Creates a persona, exports it, imports into a new workspace, and validates.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Create source and target workspaces
SRC_WORKSPACE="$(mktemp -d)"
TGT_WORKSPACE="$(mktemp -d)"
SRC_CONFIG="$SRC_WORKSPACE/openclaw.json"
TGT_CONFIG="$TGT_WORKSPACE/openclaw.json"
BUNDLE_FILE="$SRC_WORKSPACE/testbot.persona"

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

cleanup() {
    rm -rf "$SRC_WORKSPACE" "$TGT_WORKSPACE"
}
trap cleanup EXIT

printf "${BOLD}🧪 Export/Import Round-Trip Test${NC}\n\n"

# --- Step 1: Create source persona ---
printf "  Step 1: Creating source persona...\n"
echo '{}' > "$SRC_CONFIG"

python3 "$ENGINE_DIR/scripts/generate-soul.py" \
    --archetype mentor \
    --name "Sage" \
    --emoji "📚" \
    --creature "Wise mentor AI" \
    --output "$SRC_WORKSPACE/SOUL.md"

python3 "$ENGINE_DIR/scripts/generate-user.py" \
    --name "Student" \
    --call-names "Student" \
    --timezone "UTC" \
    --output "$SRC_WORKSPACE/USER.md"

python3 "$ENGINE_DIR/scripts/generate-identity.py" \
    --name "Sage" \
    --emoji "📚" \
    --creature "Wise mentor AI" \
    --vibe "Patient and wise" \
    --output "$SRC_WORKSPACE/IDENTITY.md"

python3 "$ENGINE_DIR/scripts/generate-memory.py" \
    --name "Sage" \
    --emoji "📚" \
    --creature "Wise mentor AI" \
    --user-name "Student" \
    --workspace "$SRC_WORKSPACE"

python3 "$ENGINE_DIR/scripts/voice-setup.py" \
    --provider builtin \
    --config "$SRC_CONFIG" \
    --non-interactive

# Write persona config
python3 -c "
import json, sys
sys.path.insert(0, '$ENGINE_DIR/scripts')
from lib.config import merge_config
merge_config({
    'persona': {
        'name': 'Sage',
        'emoji': '📚',
        'identity': {'creature': 'Wise mentor AI'},
        'personality': {'archetype': 'mentor'}
    }
}, '$SRC_CONFIG')
"

printf "  Source persona created.\n\n"

# --- Step 2: Export ---
printf "  Step 2: Exporting persona...\n"
cd "$SRC_WORKSPACE"
OPENCLAW_CONFIG="$SRC_CONFIG" OPENCLAW_WORKSPACE="$SRC_WORKSPACE" \
    sh "$ENGINE_DIR/scripts/persona-export.sh" \
    --name testbot \
    --include-memory \
    --config "$SRC_CONFIG" \
    --workspace "$SRC_WORKSPACE"

check "Bundle file created" test -f "$BUNDLE_FILE"
check "Bundle is valid zip" python3 -c "import zipfile; zipfile.ZipFile('$BUNDLE_FILE')"
check "Bundle contains manifest" python3 -c "
import zipfile
with zipfile.ZipFile('$BUNDLE_FILE') as z:
    assert 'manifest.json' in z.namelist()
"
check "Bundle contains SOUL.md" python3 -c "
import zipfile
with zipfile.ZipFile('$BUNDLE_FILE') as z:
    assert 'workspace/SOUL.md' in z.namelist()
"
printf "\n"

# --- Step 3: Import into new workspace ---
printf "  Step 3: Importing into new workspace...\n"
echo '{}' > "$TGT_CONFIG"
OPENCLAW_CONFIG="$TGT_CONFIG" OPENCLAW_WORKSPACE="$TGT_WORKSPACE" \
    sh "$ENGINE_DIR/scripts/persona-import.sh" \
    "$BUNDLE_FILE" \
    --workspace "$TGT_WORKSPACE" \
    --config "$TGT_CONFIG" \
    --force

printf "\n"

# --- Step 4: Validate ---
printf "  Step 4: Validating imported files...\n"
check "SOUL.md imported" test -f "$TGT_WORKSPACE/SOUL.md"
check "USER.md imported" test -f "$TGT_WORKSPACE/USER.md"
check "IDENTITY.md imported" test -f "$TGT_WORKSPACE/IDENTITY.md"
check "MEMORY.md imported" test -f "$TGT_WORKSPACE/MEMORY.md"
check "HEARTBEAT.md imported" test -f "$TGT_WORKSPACE/HEARTBEAT.md"
check "AGENTS.md imported" test -f "$TGT_WORKSPACE/AGENTS.md"

# Compare content
check "SOUL.md content matches" diff -q "$SRC_WORKSPACE/SOUL.md" "$TGT_WORKSPACE/SOUL.md"
check "USER.md content matches" diff -q "$SRC_WORKSPACE/USER.md" "$TGT_WORKSPACE/USER.md"
check "IDENTITY.md content matches" diff -q "$SRC_WORKSPACE/IDENTITY.md" "$TGT_WORKSPACE/IDENTITY.md"

# Check config was merged
check "Persona config imported" python3 -c "
import json
with open('$TGT_CONFIG') as f:
    c = json.load(f)
assert c['persona']['name'] == 'Sage'
assert c['persona']['personality']['archetype'] == 'mentor'
"

printf "\n${BOLD}Results: ${GREEN}$PASS passed${NC}, "
if [ "$FAIL" -gt 0 ]; then
    printf "${RED}$FAIL failed${NC}\n"
    exit 1
else
    printf "0 failed\n"
fi
printf "${GREEN}✅ Round-trip test passed!${NC}\n"
