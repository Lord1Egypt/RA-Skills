#!/bin/bash
# update.sh — Local update helper for ocas-forge.
#
# Usage:
#   ./update.sh            Pull latest ocas-forge from its GitHub source via
#                          the shared skill_update.py helper.
#   ./update.sh --help     Show this usage text and exit.
#   ./update.sh -h         Same as --help.
#
# The helper preserves journals/ and data/ directories; it updates only the
# skill's SKILL.md, references/, scripts/, and templates/.

case "$1" in
  --help|-h)
    sed -n '2,11p' "$0"
    exit 0
    ;;
  "")
    python3 <hermes-home>/scripts/skill_update.py ocas-forge
    ;;
  *)
    echo "Unknown argument: $1" >&2
    echo "Usage: ./update.sh [--help]" >&2
    exit 2
    ;;
esac