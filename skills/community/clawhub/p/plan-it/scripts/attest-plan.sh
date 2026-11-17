#!/usr/bin/env bash
# attest-plan.sh — compute SHA-256 of active plan.html and store it.
#
# Usage:
#   attest-plan.sh           # compute and store
#   attest-plan.sh --show    # print stored hash
#   attest-plan.sh --clear   # delete attestation

set -euo pipefail

ACTION="store"
if [ "${1:-}" = "--show" ]; then ACTION="show"; fi
if [ "${1:-}" = "--clear" ]; then ACTION="clear"; fi

resolve_plan_and_attest() {
  if [ -n "${PLAN_ID:-}" ] && [ -f ".planning/${PLAN_ID}/plan.html" ]; then
    PLAN_PATH=".planning/${PLAN_ID}/plan.html"
    ATTEST_PATH=".planning/${PLAN_ID}/.attestation"
    return
  fi
  if [ -f ".planning/.active_plan" ]; then
    local ap
    ap=$(tr -d '[:space:]' < .planning/.active_plan 2>/dev/null || true)
    if [ -n "$ap" ] && [ -f ".planning/${ap}/plan.html" ]; then
      PLAN_PATH=".planning/${ap}/plan.html"
      ATTEST_PATH=".planning/${ap}/.attestation"
      return
    fi
  fi
  if [ -f "plan.html" ]; then
    PLAN_PATH="plan.html"
    ATTEST_PATH=".plan-attestation"
    return
  fi
  PLAN_PATH=""
  ATTEST_PATH=""
}

resolve_plan_and_attest

if [ -z "$PLAN_PATH" ]; then
  echo "[plan-it] no plan.html found. Run: bash scripts/init-plan.sh <template>" >&2
  exit 1
fi

compute_hash() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    echo "[plan-it] no sha256sum or shasum found" >&2
    return 1
  fi
}

case "$ACTION" in
  show)
    if [ -f "$ATTEST_PATH" ]; then
      tr -d '[:space:]' < "$ATTEST_PATH"
      echo
    else
      echo "[plan-it] no attestation found at $ATTEST_PATH" >&2
      exit 2
    fi
    ;;
  clear)
    if [ -f "$ATTEST_PATH" ]; then
      rm -f "$ATTEST_PATH"
      echo "[plan-it] attestation cleared at $ATTEST_PATH"
    else
      echo "[plan-it] no attestation to clear at $ATTEST_PATH"
    fi
    ;;
  store)
    # v0.2.0: write the browser-verifiable content seal into the plan-data JSON
    # BEFORE hashing, so the whole-file attestation covers the sealed file. Best
    # effort: if Python or the helper is missing, fall back to whole-file-only
    # attestation (pre-0.2.0 behavior) rather than failing the lock.
    # Probe-execute each candidate so a non-working shim (e.g. the Windows
    # Store python3 alias on Git Bash) is rejected in favor of a real one.
    PY=""
    for cand in python3 python; do
      if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import sys" >/dev/null 2>&1; then
        PY="$cand"; break
      fi
    done
    HELPER="$(dirname "$0")/plan-hook.py"
    if [ -n "$PY" ] && [ -f "$HELPER" ]; then
      "$PY" "$HELPER" seal || echo "[plan-it] content-seal step skipped; continuing with whole-file attestation" >&2
    else
      echo "[plan-it] no working Python found for content-seal; whole-file attestation only" >&2
    fi
    HASH=$(compute_hash "$PLAN_PATH")
    if [ -z "$HASH" ]; then
      exit 3
    fi
    if [ "$ATTEST_PATH" = ".plan-attestation" ]; then
      :
    else
      mkdir -p "$(dirname "$ATTEST_PATH")"
    fi
    printf "%s" "$HASH" > "$ATTEST_PATH"
    echo "[plan-it] attestation stored at $ATTEST_PATH"
    echo "[plan-it] sha256: $HASH"
    ;;
esac
