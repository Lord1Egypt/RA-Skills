#!/usr/bin/env bash
# planning-with-files: check-complete.sh
# Verifies all phases in task_plan.md are marked complete before the agent stops.
# Exit 0 = all done. Exit 1 = incomplete phases remain.

set -euo pipefail

WORKDIR="${OPENCLAW_WORKDIR:-$(pwd)}"
PLAN="$WORKDIR/task_plan.md"

if [ ! -f "$PLAN" ]; then
  echo "[planning-with-files] ⚠️  No task_plan.md found in $WORKDIR"
  echo "  → Was this a simple task that didn't need planning? If so, OK to stop."
  exit 0
fi

# Count phases
TOTAL=$(grep -c "^\- \[" "$PLAN" 2>/dev/null || echo 0)
DONE=$(grep -c "^\- \[x\]" "$PLAN" 2>/dev/null || echo 0)
INCOMPLETE=$(grep -c "^\- \[ \]" "$PLAN" 2>/dev/null || echo 0)

echo ""
echo "[planning-with-files] Completion check"
echo "  Total phases : $TOTAL"
echo "  Complete     : $DONE"
echo "  Incomplete   : $INCOMPLETE"
echo ""

if [ "$INCOMPLETE" -gt 0 ]; then
  echo "⛔ STOP — incomplete phases remain:"
  grep "^\- \[ \]" "$PLAN" | sed 's/^/  /'
  echo ""
  echo "  → Continue working until all phases are marked [x]."
  exit 1
else
  if [ "$TOTAL" -eq 0 ]; then
    echo "⚠️  No phase checkboxes found in task_plan.md."
    echo "  → Add phases as '- [ ] Phase name' and check them off."
    exit 1
  fi
  echo "✅ All $DONE phases complete. Safe to deliver results."
  exit 0
fi
