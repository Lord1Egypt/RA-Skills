#!/usr/bin/env bash
# hermes-verify-mapforge.sh — ad-hoc verification of a MapForge clean load.
#
# AngelScript for ManiaPlanet has NO offline compiler/linter. The only real
# check is the in-game script engine compiling the plugin at load. This script
# greps Openplanet.log for the load line + errors and confirms all module files
# are present and registered. It does NOT exercise button runtime behavior.
#
# Usage: bash hermes-verify-mapforge.sh
# NOTE: `grep -c` exits 1 on zero matches, so DO NOT append `|| echo 0` — it
# would double the count. Capture stdout and default to 0 instead.
set -u
GAMEDIR="/c/Users/tomekdot/Openplanet4"
LOG="$GAMEDIR/Openplanet.log"
MODDIR="$GAMEDIR/Plugins/MapForge/src/Modules"
MAIN="$GAMEDIR/Plugins/MapForge/src/Main.as"

echo "=== MapForge ad-hoc verification ==="
if tasklist 2>/dev/null | grep -qi maniaplanet; then echo "Game process: running"; else echo "Game process: NOT running"; fi

LOADED=$(grep -c "Loaded plugin 'MapForge'" "$LOG" 2>/dev/null); LOADED=${LOADED:-0}
FAILED=$(grep -c "Script compilation failed" "$LOG" 2>/dev/null); FAILED=${FAILED:-0}
ERRS=$(grep -c "ERR :" "$LOG" 2>/dev/null); ERRS=${ERRS:-0}
echo "Plugin loaded count : $LOADED"
echo "Compilation failed  : $FAILED"
echo "ERR : lines         : $ERRS"

PRESENT=$(ls "$MODDIR"/*.as 2>/dev/null | wc -l); PRESENT=${PRESENT:-0}
REG=$(grep -c "g_modules.Register(" "$MAIN" 2>/dev/null); REG=${REG:-0}
echo "Module files        : $PRESENT / 18"
echo "Registered          : $REG / 18"

if [ "$LOADED" -ge 1 ] && [ "$FAILED" -eq 0 ] && [ "$ERRS" -eq 0 ] && [ "$PRESENT" -eq 18 ] && [ "$REG" -eq 18 ]; then
  echo "RESULT: PASS (clean load, 18/18 modules present & registered)"
  exit 0
else
  echo "RESULT: FAIL"
  exit 1
fi
