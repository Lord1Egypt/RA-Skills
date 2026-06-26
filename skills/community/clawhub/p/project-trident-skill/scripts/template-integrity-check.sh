#!/usr/bin/env bash
# =============================================================================
# Project Trident — Template Integrity Check
# Version: 2.0.0
#
# PURPOSE:
#   Verify that memory/layer0/AGENT-PROMPT.md has not been tampered with.
#   Computes SHA256 hash of the installed prompt and compares it against:
#     1. The canonical hash of the original template (from this script)
#     2. A user-approved hash stored in memory/layer0/.approved-hash
#
# USAGE:
#   chmod +x template-integrity-check.sh
#   ./template-integrity-check.sh [--workspace PATH] [--approve] [--silent]
#
# OPTIONS:
#   --workspace PATH   Override workspace path
#   --approve          Approve current hash (use when intentionally modifying template)
#   --silent           Suppress output (exit code 0=ok, 1=tampered, 2=error)
#
# INTEGRATION:
#   Add to Layer 0.5 cron payload as a pre-check:
#   "Run template-integrity-check.sh before executing signal routing.
#    If it exits with code 1, halt and log to memory/layer0/audit-log.md"
# =============================================================================

set -euo pipefail

# ─── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'
BOLD='\033[1m'

log()     { $SILENT || echo -e "${BLUE}[integrity]${RESET} $*"; }
success() { $SILENT || echo -e "${GREEN}[✓]${RESET} $*"; }
warn()    { $SILENT || echo -e "${YELLOW}[!]${RESET} $*"; }
error()   { $SILENT || echo -e "${RED}[✗]${RESET} $*"; }

# ─── Parse arguments ──────────────────────────────────────────────────────────
WORKSPACE="${HOME}/.openclaw/workspace"
APPROVE=false
SILENT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace) WORKSPACE="$2"; shift 2 ;;
    --approve)   APPROVE=true; shift ;;
    --silent)    SILENT=true; shift ;;
    *) shift ;;
  esac
done

WORKSPACE="${WORKSPACE%/}"

# ─── Paths ────────────────────────────────────────────────────────────────────
PROMPT_FILE="$WORKSPACE/memory/layer0/AGENT-PROMPT.md"
APPROVED_HASH_FILE="$WORKSPACE/memory/layer0/.approved-hash"
AUDIT_LOG="$WORKSPACE/memory/layer0/audit-log.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL_TEMPLATE="$SCRIPT_DIR/layer0-agent-prompt-template.md"

# ─── Preflight ────────────────────────────────────────────────────────────────
if [[ ! -f "$PROMPT_FILE" ]]; then
  error "AGENT-PROMPT.md not found at: $PROMPT_FILE"
  error "Install Trident first: see references/trident-lite.md"
  exit 2
fi

# ─── Compute hash ─────────────────────────────────────────────────────────────
if command -v sha256sum &>/dev/null; then
  CURRENT_HASH=$(sha256sum "$PROMPT_FILE" | awk '{print $1}')
elif command -v shasum &>/dev/null; then
  CURRENT_HASH=$(shasum -a 256 "$PROMPT_FILE" | awk '{print $1}')
else
  error "No SHA256 tool found (sha256sum or shasum required)"
  exit 2
fi

TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# ─── Approve mode ─────────────────────────────────────────────────────────────
if $APPROVE; then
  echo "$CURRENT_HASH" > "$APPROVED_HASH_FILE"
  success "Approved hash: $CURRENT_HASH"
  success "Stored at: $APPROVED_HASH_FILE"

  # Log approval
  mkdir -p "$(dirname "$AUDIT_LOG")"
  echo "## [$TIMESTAMP] HASH APPROVED" >> "$AUDIT_LOG"
  echo "- Hash: \`$CURRENT_HASH\`" >> "$AUDIT_LOG"
  echo "- File: $PROMPT_FILE" >> "$AUDIT_LOG"
  echo "- Action: User explicitly approved this template version" >> "$AUDIT_LOG"
  echo "" >> "$AUDIT_LOG"

  exit 0
fi

# ─── Check approved hash ──────────────────────────────────────────────────────
APPROVED_HASH=""
CANONICAL_HASH=""

if [[ -f "$APPROVED_HASH_FILE" ]]; then
  APPROVED_HASH=$(cat "$APPROVED_HASH_FILE" | tr -d '[:space:]')
fi

if [[ -f "$CANONICAL_TEMPLATE" ]]; then
  if command -v sha256sum &>/dev/null; then
    CANONICAL_HASH=$(sha256sum "$CANONICAL_TEMPLATE" | awk '{print $1}')
  else
    CANONICAL_HASH=$(shasum -a 256 "$CANONICAL_TEMPLATE" | awk '{print $1}')
  fi
fi

# ─── Evaluate integrity ───────────────────────────────────────────────────────
STATUS="unknown"
VERDICT=""

if [[ -n "$APPROVED_HASH" && "$CURRENT_HASH" == "$APPROVED_HASH" ]]; then
  STATUS="approved"
  VERDICT="PASS — Matches user-approved hash"
elif [[ -n "$CANONICAL_HASH" && "$CURRENT_HASH" == "$CANONICAL_HASH" ]]; then
  STATUS="canonical"
  VERDICT="PASS — Matches canonical template (unmodified)"
elif [[ -z "$APPROVED_HASH" && -z "$CANONICAL_HASH" ]]; then
  STATUS="unverified"
  VERDICT="WARN — No baseline hash available. Run --approve to register current template."
else
  STATUS="mismatch"
  VERDICT="FAIL — Hash mismatch detected. Template may have been tampered with."
fi

# ─── Output ───────────────────────────────────────────────────────────────────
log "File:     $PROMPT_FILE"
log "Hash:     $CURRENT_HASH"
log "Status:   $STATUS"
log "Verdict:  $VERDICT"

# ─── Audit log ────────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$AUDIT_LOG")"

case "$STATUS" in
  approved|canonical)
    success "$VERDICT"
    echo "## [$TIMESTAMP] INTEGRITY CHECK: PASS" >> "$AUDIT_LOG"
    echo "- Status: $STATUS" >> "$AUDIT_LOG"
    echo "- Hash: \`$CURRENT_HASH\`" >> "$AUDIT_LOG"
    echo "" >> "$AUDIT_LOG"
    exit 0
    ;;
  unverified)
    warn "$VERDICT"
    echo "## [$TIMESTAMP] INTEGRITY CHECK: UNVERIFIED" >> "$AUDIT_LOG"
    echo "- Status: unverified (no baseline hash)" >> "$AUDIT_LOG"
    echo "- Hash: \`$CURRENT_HASH\`" >> "$AUDIT_LOG"
    echo "- Action required: Run \`template-integrity-check.sh --approve\` to register" >> "$AUDIT_LOG"
    echo "" >> "$AUDIT_LOG"
    exit 0  # Don't block on first run
    ;;
  mismatch)
    error "$VERDICT"
    echo "" >> "$AUDIT_LOG"
    echo "## [$TIMESTAMP] ⚠️ INTEGRITY CHECK: FAIL" >> "$AUDIT_LOG"
    echo "- Status: TAMPERED" >> "$AUDIT_LOG"
    echo "- Expected hash: \`${APPROVED_HASH:-${CANONICAL_HASH:-none}}\`" >> "$AUDIT_LOG"
    echo "- Current hash:  \`$CURRENT_HASH\`" >> "$AUDIT_LOG"
    echo "- File: $PROMPT_FILE" >> "$AUDIT_LOG"
    echo "- ⛔ Layer 0.5 signal routing HALTED" >> "$AUDIT_LOG"
    echo "" >> "$AUDIT_LOG"
    error "Layer 0.5 routing halted. Review $PROMPT_FILE before proceeding."
    error "If you intentionally modified the template, run: --approve"
    exit 1
    ;;
esac
