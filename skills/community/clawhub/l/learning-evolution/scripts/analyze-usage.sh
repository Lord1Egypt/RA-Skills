#!/bin/bash
#
# analyze-usage.sh - Create a verified-data usage analysis template.
# Usage: ./analyze-usage.sh --skill <name> [--period 30d]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${LEARNING_DATA_DIR:-$SKILL_DIR/data}"

SKILL_NAME=""
PERIOD="30d"

while [[ $# -gt 0 ]]; do
    case $1 in
        --skill)
            SKILL_NAME="$2"
            shift 2
            ;;
        --period)
            PERIOD="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$SKILL_NAME" ]]; then
    echo "Usage: $0 --skill <name> [--period 30d]"
    exit 1
fi

if [[ ! "$SKILL_NAME" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,100}$ ]]; then
    echo "Skill name must use only letters, numbers, dot, underscore, or hyphen"
    exit 1
fi

if [[ ! "$PERIOD" =~ ^[0-9]{1,4}[dwmy]$ ]]; then
    echo "Period must look like 30d, 12w, 6m, or 1y"
    exit 1
fi

mkdir -p "$DATA_DIR"

REPORT_FILE="$DATA_DIR/USAGE-${SKILL_NAME}-$(date +%Y%m%d).md"
GENERATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
    printf '# Usage Analysis Template: %s\n\n' "$SKILL_NAME"
    printf '**Analysis Period**: Last %s\n' "$PERIOD"
    printf '**Generated**: %s\n' "$GENERATED_AT"
    printf '**Data Policy**: Fill each metric only from verified logs, user feedback, or observed outcomes.\n\n'
    printf '## Verified Inputs\n\n'
    printf '| Input | Source | Value | Notes |\n'
    printf '|-------|--------|-------|-------|\n'
    printf '| Total uses | TODO: verified usage log | TODO | Do not estimate without data |\n'
    printf '| Unique users | TODO: verified usage log | TODO | Use anonymized counts only |\n'
    printf '| Completion rate | TODO: task/outcome log | TODO | Define completion before measuring |\n'
    printf '| Error rate | TODO: error log | TODO | Group by reproducible failure mode |\n\n'
    printf '## Observed Usage Patterns\n\n'
    printf '%s\n' '- Frequency: TODO'
    printf '%s\n' '- Timing: TODO'
    printf '%s\n' '- Entry points: TODO'
    printf '%s\n' '- Repeated workflows: TODO'
    printf '%s\n\n' '- Drop-off points: TODO'
    printf '## Evidence-Backed Insights\n\n'
    printf '%s\n' '- Insight 1: TODO'
    printf '%s\n' '- Insight 2: TODO'
    printf '%s\n\n' '- Insight 3: TODO'
    printf '## Follow-Up Questions\n\n'
    printf '%s\n' '- What data is missing before making a product decision?'
    printf '%s\n' '- Which user segment should be reviewed first?'
    printf '%s\n' '- Which metric should be rechecked after the next release?'
} > "$REPORT_FILE"

echo "Usage analysis template created: $REPORT_FILE"
