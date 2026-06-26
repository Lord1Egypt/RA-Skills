#!/bin/bash
# quickstart.sh — local-safe onboarding flow (no persistence install, no remote fetch)
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/proactive-claw"

if [ ! -d "$SKILL_DIR" ]; then
  echo "ERROR: Skill directory not found: $SKILL_DIR"
  echo "Install proactive-claw first, then run this script again."
  exit 1
fi

cd "$SKILL_DIR"

echo "Quickstart: doctor check"
doctor_failed=0
if ! bash scripts/setup.sh --doctor; then
  echo ""
  echo "Doctor reported missing prerequisites."
  echo "Continuing with local-safe defaults and simulation."
  doctor_failed=1
fi

echo ""
if [ -f "$SKILL_DIR/config.json" ]; then
  echo "Quickstart: config.json already exists (leaving it unchanged)"
else
  echo "Quickstart: writing safe defaults (max_autonomy_level=confirm)"
  python3 scripts/config_wizard.py --defaults --autonomy confirm
fi

echo ""
echo "Quickstart: running dry simulation"
python3 scripts/daemon.py --simulate --days 3

echo ""
if [ "$doctor_failed" -eq 1 ]; then
  echo "Quickstart complete with warnings."
  echo "Fix doctor findings, then rerun: bash scripts/setup.sh --doctor"
else
  echo "Quickstart complete."
fi
echo "Review the simulation output, then run: python3 scripts/daemon.py"
