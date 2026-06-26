#!/usr/bin/env bash
# Sync litmus-clawhub from the main litmus repo.
# Run from anywhere: bash path/to/litmus-clawhub/sync.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$SCRIPT_DIR/../litmus" && pwd)"
DST="$SCRIPT_DIR"

if [ ! -d "$SRC" ]; then
  echo "Error: litmus source not found at $SRC"
  exit 1
fi

cp "$SRC/SKILL.md"    "$DST/"
cp "$SRC/package.json" "$DST/"
cp "$SRC/INSTALL.md"  "$DST/"
cp "$SRC/README.md"   "$DST/"

cp "$SRC/configs/default.json" "$DST/configs/"

cp "$SRC/references/onboarding.md" \
   "$SRC/references/program.md" \
   "$SRC/references/director.md" \
   "$SRC/references/leisure.md" \
   "$SRC/references/dawn.md" \
   "$SRC/references/digest.md" \
   "$SRC/references/watchdog.md" \
   "$SRC/references/clawrxiv.md" \
   "$DST/references/"

cp "$SRC/references/templates/architecture.md" \
   "$SRC/references/templates/general.md" \
   "$SRC/references/templates/optimizer.md" \
   "$SRC/references/templates/regularization.md" \
   "$DST/references/templates/"

cp "$SRC/scripts/setup.sh" \
   "$SRC/scripts/prepare-agents.sh" \
   "$SRC/scripts/setup-cron.sh" \
   "$SRC/scripts/status.sh" \
   "$SRC/scripts/results.sh" \
   "$DST/scripts/"

echo "Synced from $SRC"
