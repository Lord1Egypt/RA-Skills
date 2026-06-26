#!/usr/bin/env bash
set -euo pipefail

NEBULA_CLAW_DEVELOPER_API_BASE="${NEBULA_CLAW_DEVELOPER_API_BASE:-http://127.0.0.1:8080}"

usage() {
  cat <<'EOF'
Usage:
  vm_api.sh health
  vm_api.sh list
  vm_api.sh create <template_name> <vm_name>
  vm_api.sh delete <vm_name_or_id>

Environment:
  NEBULA_CLAW_DEVELOPER_API_BASE   Base URL of the restricted OpenNebula control plane API
EOF
}

cmd="${1:-}"

case "$cmd" in
  health)
    curl -s "$NEBULA_CLAW_DEVELOPER_API_BASE/health"
    ;;
  list)
    curl -s "$NEBULA_CLAW_DEVELOPER_API_BASE/vms"
    ;;
  create)
    template_name="${2:-}"
    vm_name="${3:-}"
    if [[ -z "$template_name" || -z "$vm_name" ]]; then
      usage
      exit 1
    fi
    curl -s -X POST "$NEBULA_CLAW_DEVELOPER_API_BASE/vms" \
      -H "Content-Type: application/json" \
      -d "{\"template_name\":\"$template_name\",\"name\":\"$vm_name\"}"
    ;;
  delete)
    vm_ref="${2:-}"
    if [[ -z "$vm_ref" ]]; then
      usage
      exit 1
    fi
    curl -s -X DELETE "$NEBULA_CLAW_DEVELOPER_API_BASE/vms/$vm_ref"
    ;;
  *)
    usage
    exit 1
    ;;
esac
