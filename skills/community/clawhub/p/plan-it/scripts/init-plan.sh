#!/usr/bin/env bash
# init-plan.sh — scaffold plan.html from a chosen template.
#
# Usage:
#   init-plan.sh                              # interactive prompt for template
#   init-plan.sh <template-name>              # named template
#   init-plan.sh <template-name> --slug NAME  # parallel-plan mode under .planning/NAME/
#
# Templates: implementation-plan three-approaches ticket-triage feature-flag-editor
#            module-map annotated-pr living-design-system animation-sandbox
#            weekly-status incident-timeline

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Resolve templates dir: top-level templates/ first, then skill-bundled, then CLAUDE_PLUGIN_ROOT
RESOLVED_TEMPLATES=""
for candidate in \
  "${SCRIPT_DIR}/../templates" \
  "${CLAUDE_PLUGIN_ROOT:-}/templates" \
  "${HOME}/.claude/skills/plan-it/templates" \
  "${HOME}/.claude/plugins/marketplaces/plan-it/templates"
do
  if [ -d "$candidate" ]; then
    RESOLVED_TEMPLATES="$candidate"
    break
  fi
done

if [ -z "$RESOLVED_TEMPLATES" ]; then
  echo "[plan-it] templates/ dir not found. Reinstall the skill." >&2
  exit 1
fi

TEMPLATE="${1:-}"
SLUG=""
shift || true
while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2 ;;
    *) echo "[plan-it] unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$TEMPLATE" ]; then
  echo "Available templates:"
  ls -1 "$RESOLVED_TEMPLATES" | sed 's/\.html$//' | sed 's/^/  /'
  echo
  read -r -p "Choose template: " TEMPLATE
fi

SRC="${RESOLVED_TEMPLATES}/${TEMPLATE}.html"
if [ ! -f "$SRC" ]; then
  echo "[plan-it] template not found: $TEMPLATE" >&2
  echo "Try one of:" >&2
  ls -1 "$RESOLVED_TEMPLATES" | sed 's/\.html$//' | sed 's/^/  /' >&2
  exit 3
fi

if [ -n "$SLUG" ]; then
  DEST_DIR=".planning/${SLUG}"
  mkdir -p "$DEST_DIR"
  DEST="${DEST_DIR}/plan.html"
  mkdir -p ".planning"
  echo "$SLUG" > ".planning/.active_plan"
else
  DEST="plan.html"
fi

if [ -f "$DEST" ]; then
  TS=$(date +%Y%m%d-%H%M%S)
  cp "$DEST" "${DEST}.backup.${TS}"
  echo "[plan-it] existing $DEST backed up to ${DEST}.backup.${TS}"
fi

cp "$SRC" "$DEST"
echo "[plan-it] created $DEST from template $TEMPLATE"
echo "[plan-it] open it: bash scripts/render-plan.sh"
