#!/usr/bin/env bash
# render-plan.sh — open plan.html in the default browser.
#
# Resolves the active plan via PLAN_ID / .active_plan / legacy chain (mirrors plan-hook.py).

set -euo pipefail

resolve_plan() {
  if [ -n "${PLAN_ID:-}" ]; then
    if [ -f ".planning/${PLAN_ID}/plan.html" ]; then
      echo ".planning/${PLAN_ID}/plan.html"
      return
    fi
  fi
  if [ -f ".planning/.active_plan" ]; then
    local ap
    ap=$(tr -d '[:space:]' < .planning/.active_plan 2>/dev/null || true)
    if [ -n "$ap" ] && [ -f ".planning/${ap}/plan.html" ]; then
      echo ".planning/${ap}/plan.html"
      return
    fi
  fi
  if [ -f "plan.html" ]; then
    echo "plan.html"
    return
  fi
}

PLAN_PATH=$(resolve_plan || true)
if [ -z "${PLAN_PATH:-}" ]; then
  echo "[plan-it] no plan.html found. Run: bash scripts/init-plan.sh <template>" >&2
  exit 1
fi

ABS=$(cd "$(dirname "$PLAN_PATH")" && pwd)/$(basename "$PLAN_PATH")

OS_NAME=$(uname -s 2>/dev/null || echo unknown)
case "$OS_NAME" in
  Linux*)
    if command -v wslview >/dev/null 2>&1; then
      wslview "$ABS"
    elif command -v xdg-open >/dev/null 2>&1; then
      xdg-open "$ABS"
    else
      echo "[plan-it] no xdg-open / wslview. Open manually: $ABS" >&2
      exit 2
    fi
    ;;
  Darwin*)
    open "$ABS"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    start "" "$ABS"
    ;;
  *)
    echo "[plan-it] unknown OS. Open manually: $ABS" >&2
    exit 2
    ;;
esac

echo "[plan-it] opened $ABS"
