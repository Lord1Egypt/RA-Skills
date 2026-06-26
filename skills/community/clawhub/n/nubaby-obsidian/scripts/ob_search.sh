#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-}"
QUERY="${2:-}"

case "$MODE" in
  path)
    obsidian-cli print-default --path-only
    ;;
  name)
    if [[ -z "$QUERY" ]]; then
      echo "usage: ob_search.sh name <query>" >&2
      exit 1
    fi
    obsidian-cli search "$QUERY"
    ;;
  content)
    if [[ -z "$QUERY" ]]; then
      echo "usage: ob_search.sh content <query>" >&2
      exit 1
    fi
    obsidian-cli search-content "$QUERY"
    ;;
  skill)
    if [[ -z "$QUERY" ]]; then
      echo "usage: ob_search.sh skill <query>" >&2
      exit 1
    fi
    VAULT="$(obsidian-cli print-default --path-only)"
    rg -n -S "$QUERY" "$VAULT/Skills" --glob '*.md'
    ;;
  *)
    cat >&2 <<'EOF'
usage:
  ob_search.sh path
  ob_search.sh name <query>
  ob_search.sh content <query>
  ob_search.sh skill <query>
EOF
    exit 1
    ;;
esac
