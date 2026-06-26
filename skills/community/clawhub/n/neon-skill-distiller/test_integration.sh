#!/bin/bash
set -e

# Paths (relative to go-pbd or skills repo)
SKILLS="${SKILLS_PATH:-../skills}"
PBD_SKILLS="$SKILLS/pbd"
AGENTIC_SKILLS="$SKILLS/agentic"
TESTDATA="$SKILLS/skill-distiller/testdata"

# Check Ollama
if ! ollama list 2>/dev/null | grep -qE "(llama|mistral)"; then
  echo "SKIP: Ollama not available or no model installed"
  exit 0
fi

MODEL="${OLLAMA_MODEL:-llama3.2}"

echo "=== Integration Tests (Ollama: $MODEL) ==="
echo "Skills path: $SKILLS"
echo ""
echo "Test Categories:"
echo "  - Tests 1,3,4,7,8,9: Run without skill deployment"
echo "  - Tests 2,5,6: SKIP - require '/skill-distiller' command (post-deployment)"
echo ""

# Test 1: Section Classification (using real skill)
echo "Test 1: Section Classification"
SECTION=$(head -50 "$PBD_SKILLS/essence-distiller/SKILL.md" | grep -A3 "## When to Use")
RESULT=$(ollama run $MODEL "Classify this skill section as TRIGGER, CORE_INSTRUCTION, or EXAMPLE:
$SECTION
Respond with just the type.")
echo "  Input: essence-distiller '## When to Use' section"
echo "  Expected: TRIGGER"
echo "  Got: $RESULT"
[[ "$RESULT" == *"TRIGGER"* ]] && echo "  PASS" || echo "  FAIL"

# Test 2: Full Compression (real skill)
echo "Test 2: Full Compression (essence-distiller, threshold=0.9)"
# Note: This test validates the compression concept, not the skill invocation
# The /skill-distiller command will exist after Stage 1 completion
echo "  [SKIP: Requires skill invocation - manual test after deployment]"

# Test 3: Protected Pattern Detection (real agentic skill)
echo "Test 3: Protected Pattern Detection (failure-memory)"
if [[ -f "$AGENTIC_SKILLS/failure-memory/SKILL.md" ]]; then
  grep -E "(N=1|N=2|N≥3|N-count)" "$AGENTIC_SKILLS/failure-memory/SKILL.md" > /dev/null && \
    echo "  PASS: N-count patterns found in failure-memory" || \
    echo "  FAIL: No N-count patterns found"
else
  echo "  SKIP: failure-memory skill not found"
fi

# Test 4: Advisory Pattern Detection (real agentic skill)
echo "Test 4: Advisory Pattern Detection (workflow-tools)"
if [[ -f "$AGENTIC_SKILLS/workflow-tools/SKILL.md" ]]; then
  grep -E "(SERIAL|parallel|checkpoint)" "$AGENTIC_SKILLS/workflow-tools/SKILL.md" > /dev/null && \
    echo "  PASS: Parallel/serial patterns found in workflow-tools" || \
    echo "  FAIL: No parallel/serial patterns found"
else
  echo "  SKIP: workflow-tools skill not found"
fi

# Test 5: Calibration Persistence
echo "Test 5: Calibration Persistence"
echo "  [SKIP: Requires skill invocation - manual test after deployment]"

# Test 6: One-liner Quality
echo "Test 6: One-liner Mode"
echo "  [SKIP: Requires skill invocation - manual test after deployment]"

# Test 7: Stress Test (largest skill)
echo "Test 7: Stress Test (context-verifier, 419 lines)"
if [[ -f "$AGENTIC_SKILLS/context-verifier/SKILL.md" ]]; then
  LINES=$(wc -l < "$AGENTIC_SKILLS/context-verifier/SKILL.md")
  echo "  Found context-verifier: $LINES lines"
  [[ $LINES -ge 400 ]] && echo "  PASS: Stress test fixture available" || echo "  INFO: File smaller than expected"
else
  echo "  SKIP: context-verifier skill not found"
fi

# Test 8: Error Handling (malformed)
echo "Test 8: Error Handling (malformed)"
if [[ -f "$TESTDATA/malformed.md" ]]; then
  # Verify malformed fixture contains expected issues for error testing
  ISSUES=0
  grep -q "Missing Frontmatter" "$TESTDATA/malformed.md" && ((ISSUES++)) || true
  grep -q "Unclosed code block" "$TESTDATA/malformed.md" && ((ISSUES++)) || true
  grep -q "Broken Header" "$TESTDATA/malformed.md" && ((ISSUES++)) || true
  if [[ $ISSUES -ge 2 ]]; then
    echo "  PASS: malformed.md has $ISSUES/3 expected error patterns"
  else
    echo "  FAIL: malformed.md missing expected error patterns ($ISSUES/3)"
  fi
  # Note: Full error handling validation requires skill invocation (SKIP)
  # Manual test: /skill-distiller testdata/malformed.md should report errors
else
  echo "  FAIL: malformed.md fixture not found"
fi

# Test 9: Minimal Fixture
echo "Test 9: Minimal Fixture"
if [[ -f "$TESTDATA/minimal.md" ]]; then
  LINES=$(wc -l < "$TESTDATA/minimal.md")
  echo "  Found minimal.md: $LINES lines"
  [[ $LINES -le 20 ]] && echo "  PASS: Minimal fixture is small" || echo "  INFO: Fixture larger than expected"
else
  echo "  FAIL: minimal.md fixture not found"
fi

echo "=== Integration Tests Complete ==="
echo ""
echo "Note: Tests marked [SKIP] require skill deployment."
echo "Run full integration after Stage 1 is deployed to Claude Code."
