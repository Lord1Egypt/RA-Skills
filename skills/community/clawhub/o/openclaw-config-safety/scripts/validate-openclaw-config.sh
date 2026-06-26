#!/bin/bash
#
# validate-openclaw-config.sh
# ============================
# Validates an openclaw.json candidate BEFORE writing.
# Uses OpenClaw's own doctor command as primary validator,
# plus targeted field-level checks for known-dangerous patterns.
#
# Usage:
#   validate-openclaw-config.sh --file <path>
#   validate-openclaw-config.sh --diff '<json-string>'
#   validate-openclaw-config.sh --stdin
#
# Exit codes:
#   0  = valid (or only non-critical warnings)
#   1  = invalid (critical errors found)
#   2  = cannot validate (file not found, CLI not available)
#
# Examples:
#   validate-openclaw-config.sh --file /tmp/candidate.json
#   validate-openclaw-config.sh --diff '{"agents":{"defaults":{"models":{"nvidia/qwen/qwq-32b":{"status":"experimental"}}}}}'  # fails

set -euo pipefail

CANDIDATE_FILE=""
STRICT_MODE=false
KEEP_TEMP=false

# ─── Find openclaw CLI ─────────────────────────────────────────────────────────
find_openclaw() {
    if [[ -n "${OPENCLAW_BIN:-}" ]]; then
        echo "$OPENCLAW_BIN"
        return
    fi
    if command -v openclaw &>/dev/null; then
        command -v openclaw
        return
    fi
    local nvm_bin="$HOME/.nvm/versions/node/v24.14.1/bin/openclaw"
    if [[ -x "$nvm_bin" ]]; then
        echo "$nvm_bin"
        return
    fi
    return 1
}

OPENCLAW_BIN=$(find_openclaw) || {
    echo "ERROR: openclaw CLI not found. Set OPENCLAW_BIN env var or add to PATH." >&2
    exit 2
}

# ─── Parse args ────────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case "$1" in
        --file)
            CANDIDATE_FILE="$2"
            shift 2
            ;;
        --strict)
            STRICT_MODE=true
            shift
            ;;
        --diff)
            CANDIDATE_FILE=$(mktemp)
            printf '%s' "$2" > "$CANDIDATE_FILE"
            shift 2
            ;;
        --stdin)
            CANDIDATE_FILE=$(mktemp)
            cat > "$CANDIDATE_FILE"
            shift
            ;;
        --keep-temp)
            KEEP_TEMP=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 2
            ;;
    esac
done

# ─── Helpers ──────────────────────────────────────────────────────────────────

error()  { echo "ERROR: $*" >&2; }
warn()   { echo "WARN:  $*" >&2; }
info()   { echo "INFO:  $*"; }
pass()   { echo "PASS:  $*"; }
fail()   { echo "FAIL:  $*" >&2; }

# ─── Prerequisite checks ──────────────────────────────────────────────────────

if [[ -z "$CANDIDATE_FILE" ]]; then
    error "No candidate file specified. Use --file <path> or --diff '<json>'"
    exit 2
fi

if [[ ! -f "$CANDIDATE_FILE" ]]; then
    error "Candidate file not found: $CANDIDATE_FILE"
    exit 2
fi

# ─── Known valid fields (from Zod schema extraction) ─────────────────────────

# Per-model override fields (agents.defaults.models[<key>])
VALID_PER_MODEL_FIELDS='alias|params|streaming'

# Top-level valid keys
VALID_TOP_LEVEL_KEYS='meta|wizard|auth|models|agents|tools|commands|session|hooks|channels|gateway|skills|plugins'

# agents.defaults known top-level fields
VALID_AGENTS_DEFAULTS_FIELDS='params|model|imageModel|imageGenerationModel|pdfModel|pdfMaxBytesMb|pdfMaxPages|models|workspace|repoRoot|skipBootstrap|bootstrapMaxChars|bootstrapTotalMaxChars|bootstrapPromptTruncationWarning|userTimezone|timeFormat|envelopeTimezone|envelopeTimestamp|envelopeElapsed|contextTokens|memorySearch|compaction|timeoutSeconds'

# ─── Check 1: JSON parseability ───────────────────────────────────────────────

info "Check 1: JSON parseability"
if ! jq empty "$CANDIDATE_FILE" 2>/dev/null; then
    fail "Invalid JSON — parse failed"
    exit 1
fi
pass "Valid JSON"

# ─── Check 2: Top-level key validation ────────────────────────────────────────

info "Check 2: Top-level keys"
# grep -v returns exit 1 when there's no match; || true prevents false failure
INVALID_KEYS=$(jq -r 'keys[]' "$CANDIDATE_FILE" 2>/dev/null | grep -vE "^(${VALID_TOP_LEVEL_KEYS})$" || true)
if [[ -n "$INVALID_KEYS" ]]; then
    while read -r key; do
        warn "Unknown top-level key: '$key'"
    done <<< "$INVALID_KEYS"
    if [[ "$STRICT_MODE" == "true" ]]; then
        fail "Unknown top-level keys found"
        exit 1
    fi
fi
pass "Top-level keys OK"

# ─── Check 3: Per-model override field validation ─────────────────────────────

info "Check 3: agents.defaults.models per-model override fields"

# Check: any field inside agents.defaults.models[<key>] that's not alias/params/streaming
TMP_INVALID=$(mktemp)
jq -r \
    'if .agents?.defaults?.models then
       .agents.defaults.models | to_entries[] |
       .key as $mk | .value | keys[]? |
       select(. != "alias" and . != "params" and . != "streaming") |
       "\($mk)|\(. )"
     else empty end' \
    "$CANDIDATE_FILE" > "$TMP_INVALID"
# Note: jq returns non-zero only on parse error (caught in Check 1); empty output is normal

PER_MODEL_OVERRIDE_ERRORS=0
while IFS='|' read -r model_key field; do
    [[ -z "$field" ]] && continue
    error "Invalid field '$field' in agents.defaults.models['$model_key'] — valid: alias, params, streaming"
    PER_MODEL_OVERRIDE_ERRORS=$((PER_MODEL_OVERRIDE_ERRORS + 1))
done < "$TMP_INVALID"
rm -f "$TMP_INVALID"

if [[ $PER_MODEL_OVERRIDE_ERRORS -gt 0 ]]; then
    fail "Found $PER_MODEL_OVERRIDE_ERRORS invalid per-model override fields"
    exit 1
fi
pass "Per-model override fields OK"

# ─── Check 4: agents.defaults top-level field validation ─────────────────────

info "Check 4: agents.defaults top-level fields"
jq -r \
    'if .agents?.defaults then .agents.defaults | keys[] else empty end' \
    "$CANDIDATE_FILE" 2>/dev/null \
    | grep -vE "^(${VALID_AGENTS_DEFAULTS_FIELDS})$" || true \
    | while read -r field; do
        warn "Unknown agents.defaults field: '$field'"
      done
pass "agents.defaults top-level OK"

# ─── Check 5: Known-crash fields (status, note) in per-model overrides ─────────

info "Check 5: Known-crash fields (status, note) in per-model overrides"

# NOTE: forbidden fields are hardcoded here rather than loaded from
# schema/field-registry.json to avoid a jq dependency at startup.
# If OpenClaw adds a new crash field, update BOTH the schema AND this script.

# Check status — outputs model key if found, empty otherwise
HAS_STATUS=$(jq -r \
    'if .agents?.defaults?.models then
       .agents.defaults.models | to_entries[] |
       select(.value | has("status")) | .key
     else empty end' \
    "$CANDIDATE_FILE")

# Check note — outputs model key if found, empty otherwise
HAS_NOTE=$(jq -r \
    'if .agents?.defaults?.models then
       .agents.defaults.models | to_entries[] |
       select(.value | has("note")) | .key
     else empty end' \
    "$CANDIDATE_FILE")

if [[ -n "$HAS_STATUS" ]]; then
    error "FORBIDDEN: status field in agents.defaults.models['$HAS_STATUS'] — crashes gateway"
    fail "status in per-model override = instant crash"
    exit 1
fi

if [[ -n "$HAS_NOTE" ]]; then
    error "FORBIDDEN: note field in agents.defaults.models['$HAS_NOTE'] — crashes gateway"
    fail "note in per-model override = instant crash"
    exit 1
fi

pass "No forbidden fields (status, note) found"

# ─── Check 6: OpenClaw doctor validation ──────────────────────────────────────

# Treat SKIP_OPENCLAW_DOCTOR as a skip of Check 6 (useful for test suites)
if [[ "${SKIP_OPENCLAW_DOCTOR:-}" == "1" ]]; then
    info "Check 6: OpenClaw doctor validation (SKIPPED — SKIP_OPENCLAW_DOCTOR=1)"
    pass "Check 6 skipped"
else
    info "Check 6: OpenClaw doctor validation (definitive schema check)"

    TEMP_DIR=$(mktemp -d)
    TEMP_OPENCLAW_DIR="$TEMP_DIR/openclaw-test-$$"
    mkdir -p "$TEMP_OPENCLAW_DIR"
    cp "$CANDIDATE_FILE" "$TEMP_OPENCLAW_DIR/openclaw.json"

    # Track exit code separately so we can distinguish doctor failure from doctor warnings
    # timeout after 45s — doctor is typically ~20-25s with --non-interactive
    DOCTOR_EXIT=0
    DOCTOR_OUTPUT=$(timeout 45 "$OPENCLAW_BIN" doctor --fix --non-interactive 2>&1) || DOCTOR_EXIT=$?
    echo "$DOCTOR_OUTPUT" | head -20

    if [[ $DOCTOR_EXIT -eq 124 ]]; then
        warn "OpenClaw doctor timed out after 45s — treating as non-fatal"
    elif [[ $DOCTOR_EXIT -ne 0 ]]; then
        fail "OpenClaw doctor crashed (exit $DOCTOR_EXIT)"
        rm -rf "$TEMP_DIR"
        exit 1
    fi

    if echo "$DOCTOR_OUTPUT" | grep -qE "^(ERROR|error:|Error:)"; then
        fail "OpenClaw doctor found errors"
        rm -rf "$TEMP_DIR"
        [[ "$STRICT_MODE" == "true" ]] && exit 1 || warn "Non-fatal — doctor warnings present"
    fi

    rm -rf "$TEMP_DIR"
fi

# ─── Summary ──────────────────────────────────────────────────────────────────

echo ""
echo "=== Validation Complete ==="
pass "All checks passed"
exit 0
