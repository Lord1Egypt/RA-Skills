#!/usr/bin/env bash
# planning-with-files: init-session.sh
# Creates task_plan.md, findings.md, and progress.md in the current workdir.
# Usage: init-session.sh ["task description"]

set -euo pipefail

TASK="${1:-}"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"
WORKDIR="${OPENCLAW_WORKDIR:-$(pwd)}"

echo "[planning-with-files] Initializing session in: $WORKDIR"

# ── task_plan.md ──────────────────────────────────────────────────────────────
if [ ! -f "$WORKDIR/task_plan.md" ]; then
  cat "$TEMPLATES_DIR/task_plan.md" \
    | sed "s|{{TASK}}|${TASK}|g" \
    | sed "s|{{TIMESTAMP}}|${TIMESTAMP}|g" \
    > "$WORKDIR/task_plan.md"
  echo "  ✓ Created task_plan.md"
else
  echo "  ↩ task_plan.md already exists — skipping"
fi

# ── findings.md ───────────────────────────────────────────────────────────────
if [ ! -f "$WORKDIR/findings.md" ]; then
  cat "$TEMPLATES_DIR/findings.md" \
    | sed "s|{{TASK}}|${TASK}|g" \
    | sed "s|{{TIMESTAMP}}|${TIMESTAMP}|g" \
    > "$WORKDIR/findings.md"
  echo "  ✓ Created findings.md"
else
  echo "  ↩ findings.md already exists — skipping"
fi

# ── progress.md ───────────────────────────────────────────────────────────────
if [ ! -f "$WORKDIR/progress.md" ]; then
  cat "$TEMPLATES_DIR/progress.md" \
    | sed "s|{{TASK}}|${TASK}|g" \
    | sed "s|{{TIMESTAMP}}|${TIMESTAMP}|g" \
    > "$WORKDIR/progress.md"
  echo "  ✓ Created progress.md"
else
  echo "  ↩ progress.md already exists — skipping"
fi

echo ""
echo "[planning-with-files] Session ready. Files in: $WORKDIR"
echo "  → Fill in task_plan.md Goal + Phases before starting work."
