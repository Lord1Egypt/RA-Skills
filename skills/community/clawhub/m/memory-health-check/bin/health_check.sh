#!/usr/bin/env bash
set -euo pipefail
# memory-health-check main entry point

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="$SKILL_DIR/bin"
SCRIPT_DIR="$SKILL_DIR/scripts"

# Parse arguments
AUTO_REPAIR=""
DIMS=""

usage() {
    cat <<EOF
🩺 memory-health-check

Usage: $(basename "$0") [OPTIONS]

Options:
  --auto-repair       Run auto-repair after diagnostics
  --dims DIMS         Run specific dimensions only (comma-separated)
                       Available: integrity, bloat, orphans, dedup, freshness, score
  --help              Show this help message

Examples:
  $(basename "$0")                        # Full health check
  $(basename "$0") --auto-repair          # Full check + auto-repair
  $(basename "$0") --dims bloat,freshness # Only run bloat and freshness
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --auto-repair)
            AUTO_REPAIR=1
            shift
            ;;
        --dims)
            DIMS="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

run_dim() {
    local dim="$1"
    local script="$2"
    echo ""
    echo "━━━ [$dim] ━━━"
    python3 "$BIN_DIR/$script"
}

run_all() {
    echo "🩺 memory-health-check Starting health diagnostics..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    run_dim "Integrity"  "integrity_scan.py"
    run_dim "Bloat"       "bloat_detector.py"
    run_dim "Orphans"     "orphan_finder.py"
    run_dim "Dedup"       "dedup_scanner.py"
    run_dim "Freshness"   "freshness_report.py"
    run_dim "Health Score" "health_score.py"

    echo ""
    echo "━━━ [Report] ━━━"
    python3 "$SCRIPT_DIR/generate_report.py"

    if [[ -n "$AUTO_REPAIR" ]]; then
        echo ""
        echo "━━━ [Auto-Repair] ━━━"
        echo "⚠️  Running auto-repair..."
        python3 "$SCRIPT_DIR/auto_repair.py"
    fi

    echo ""
    echo "✅ memory-health-check complete."
}

run_specific() {
    local dims_param="$1"
    echo "🩺 memory-health-check Running dimensions: $dims_param"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    IFS=',' read -ra DIMS_ARRAY <<< "$dims_param"
    for dim in "${DIMS_ARRAY[@]}"; do
        dim=$(echo "$dim" | xargs)  # trim whitespace
        case "$dim" in
            integrity)   run_dim "Integrity"  "integrity_scan.py" ;;
            bloat)       run_dim "Bloat"       "bloat_detector.py" ;;
            orphans)     run_dim "Orphans"     "orphan_finder.py" ;;
            dedup)       run_dim "Dedup"       "dedup_scanner.py" ;;
            freshness)   run_dim "Freshness"   "freshness_report.py" ;;
            score|health) run_dim "Health Score" "health_score.py" ;;
            *)           echo "Unknown dimension: $dim" ;;
        esac
    done
    echo ""
    echo "✅ Done."
}

if [[ -n "$DIMS" ]]; then
    run_specific "$DIMS"
else
    run_all
fi
