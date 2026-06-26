#!/bin/bash
# audit-export.sh -- Export Jean-Claw Van Damme audit logs
# Exports audit data for compliance review or incident response
#
# Usage: ./audit-export.sh [--format csv|json] [--since YYYY-MM-DD] [--output path]

set -euo pipefail

FORMAT="json"
SINCE=""
OUTPUT=""
AUDIT_FILE="${JCVD_DATA_DIR:-$HOME/.openclaw/skills/jean-claw-van-damme/data}/audit.json"

while [[ $# -gt 0 ]]; do
    case $1 in
        --format) FORMAT="$2"; shift 2 ;;
        --since) SINCE="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ ! -f "${AUDIT_FILE}" ]; then
    echo "No audit log found at ${AUDIT_FILE}"
    echo "Jean-Claw may not have been activated yet."
    exit 1
fi

EXPORT_TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
DEFAULT_OUTPUT="jcvd-audit-export-${EXPORT_TIMESTAMP}.${FORMAT}"
OUTPUT="${OUTPUT:-${DEFAULT_OUTPUT}}"

echo "Jean-Claw Van Damme -- Audit Export"
echo "===================================="
echo "Source: ${AUDIT_FILE}"
echo "Format: ${FORMAT}"
echo "Output: ${OUTPUT}"
[ -n "${SINCE}" ] && echo "Since: ${SINCE}"
echo ""

if [ "${FORMAT}" = "json" ]; then
    if [ -n "${SINCE}" ]; then
        # Filter by date (requires jq)
        if command -v jq &> /dev/null; then
            jq --arg since "${SINCE}" '[.[] | select(.timestamp >= $since)]' "${AUDIT_FILE}" > "${OUTPUT}"
        else
            echo "jq not found -- exporting full log"
            cp "${AUDIT_FILE}" "${OUTPUT}"
        fi
    else
        cp "${AUDIT_FILE}" "${OUTPUT}"
    fi
elif [ "${FORMAT}" = "csv" ]; then
    if command -v jq &> /dev/null; then
        echo "timestamp,action,tier,decision,grant_id,reason" > "${OUTPUT}"
        jq -r '.[] | [.timestamp, .action, .tier, .decision, (.grant_id // "none"), .reason] | @csv' "${AUDIT_FILE}" >> "${OUTPUT}"
    else
        echo "CSV export requires jq. Install with: apt-get install jq"
        exit 1
    fi
else
    echo "Unsupported format: ${FORMAT}. Use 'json' or 'csv'."
    exit 1
fi

ENTRY_COUNT=$(wc -l < "${OUTPUT}" 2>/dev/null || echo "unknown")
echo "Export complete: ${OUTPUT}"
echo "Entries: ${ENTRY_COUNT}"
