#!/usr/bin/env bash
# install.sh — install all three Job Autopilot skills from ClawHub
#
# Prerequisites: install the bundle first with:
#   openclaw skills install jobautopilot-bundle
#
# Then run this script to install the three sub-skills:
#   bash <path-to-bundle>/install.sh
#
# This script runs `openclaw skills install` for each sub-skill.
# No data is collected or transmitted beyond the ClawHub download process.

echo "==> Installing Job Autopilot skills..."

for SKILL in jobautopilot-search jobautopilot-tailor jobautopilot-submitter; do
  if openclaw skills install "$SKILL" 2>/dev/null; then
    echo "  ✅  $SKILL installed"
  elif openclaw skills update "$SKILL" 2>/dev/null; then
    echo "  ✅  $SKILL updated"
  else
    echo "  ⚠️   $SKILL failed — try manually: openclaw skills install $SKILL"
  fi
done

echo ""
echo "All done."
echo "Verify: openclaw skills check | grep jobautopilot"
