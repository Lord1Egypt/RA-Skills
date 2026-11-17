#!/bin/bash
set -euo pipefail

show_help() {
  cat << EOF
Usage: $(basename "$0") [--check|--sync]

Check or refresh skill-local copies of canonical automation scripts.

OPTIONS:
  --check   Verify mirrored scripts match the root scripts directory (default)
  --sync    Copy root canonical scripts into skill-local script directories
  -h, --help
            Show this help message
EOF
}

MODE="check"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)
      MODE="check"
      shift
      ;;
    --sync)
      MODE="sync"
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "❌ Unknown option: $1"
      echo "Run with --help for usage"
      exit 1
      ;;
  esac
done

PAIRS=(
  "scripts/create-branch-for-mr.sh:planetscale-cli-skills/scripts/create-branch-for-mr.sh"
  "scripts/create-branch-for-mr.sh:pscale-branch/scripts/create-branch-for-mr.sh"
  "scripts/deploy-schema-change.sh:planetscale-cli-skills/scripts/deploy-schema-change.sh"
  "scripts/deploy-schema-change.sh:pscale-deploy-request/scripts/deploy-schema-change.sh"
  "scripts/sync-branch-with-main.sh:planetscale-cli-skills/scripts/sync-branch-with-main.sh"
)

status=0
for pair in "${PAIRS[@]}"; do
  source_path="${pair%%:*}"
  target_path="${pair#*:}"

  if [[ "$MODE" == "sync" ]]; then
    cp "$source_path" "$target_path"
    chmod --reference="$source_path" "$target_path" 2>/dev/null || chmod +x "$target_path"
    echo "synced $target_path"
  elif ! cmp -s "$source_path" "$target_path"; then
    echo "drift: $target_path differs from $source_path"
    status=1
  fi
done

if [[ "$MODE" == "check" ]] && [[ "$status" -eq 0 ]]; then
  echo "all mirrored scripts match canonical root scripts"
fi

exit "$status"
