#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--dry-run] [ignored-gotchi-id]

Batch-only mode: always routes to pet-all.sh (owned + delegated gotchis).
USAGE
}

DRY_RUN=0
POSITIONAL=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [ "$#" -gt 0 ]; do
        POSITIONAL+=("$1")
        shift
      done
      break
      ;;
    -* )
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      POSITIONAL+=("$1")
      ;;
  esac
  shift
done

if [ "${#POSITIONAL[@]}" -gt 0 ]; then
  echo "Note: single gotchi argument ignored; batch mode always pets all discovered gotchis."
fi

if [ "$DRY_RUN" -eq 1 ]; then
  exec "$SCRIPT_DIR/pet-all.sh" --dry-run
fi

exec "$SCRIPT_DIR/pet-all.sh"
