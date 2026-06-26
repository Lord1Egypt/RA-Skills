#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

bash scripts/check.sh

VERSION="$(node -p "require('./package.json').version")"
PACKAGE="$(node -p "require('./package.json').name")"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "[dry-run] Would publish ${PACKAGE}@${VERSION}"
else
  echo "Publishing ${PACKAGE}@${VERSION}"
fi
