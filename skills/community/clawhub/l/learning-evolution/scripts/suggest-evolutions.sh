#!/bin/bash
#
# suggest-evolutions.sh - Create an evidence-first evolution planning template.
# Usage: ./suggest-evolutions.sh --skill <name> [--min-confidence 0.7]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${LEARNING_DATA_DIR:-$SKILL_DIR/data}"

SKILL_NAME=""
MIN_CONFIDENCE=0.7

while [[ $# -gt 0 ]]; do
    case $1 in
        --skill)
            SKILL_NAME="$2"
            shift 2
            ;;
        --min-confidence)
            MIN_CONFIDENCE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$SKILL_NAME" ]]; then
    echo "Usage: $0 --skill <name> [--min-confidence 0.7]"
    exit 1
fi

if [[ ! "$SKILL_NAME" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,100}$ ]]; then
    echo "Skill name must use only letters, numbers, dot, underscore, or hyphen"
    exit 1
fi

if [[ ! "$MIN_CONFIDENCE" =~ ^(0(\.[0-9]+)?|1(\.0+)?)$ ]]; then
    echo "Minimum confidence must be between 0 and 1"
    exit 1
fi

mkdir -p "$DATA_DIR"

REPORT_FILE="$DATA_DIR/EVOLUTIONS-${SKILL_NAME}-$(date +%Y%m%d).md"
GENERATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
    printf '# Evolution Planning Template: %s\n\n' "$SKILL_NAME"
    printf '**Generated**: %s\n' "$GENERATED_AT"
    printf '**Minimum Confidence Threshold**: %s\n' "$MIN_CONFIDENCE"
    printf '**Data Policy**: This template does not invent recommendations or confidence scores. Add only evidence-backed candidates.\n\n'
    printf '## Candidate Evolutions\n\n'
    printf '| Candidate | Type | Evidence | Confidence | Effort | Decision |\n'
    printf '|-----------|------|----------|------------|--------|----------|\n'
    printf '| TODO | incremental/breakthrough/pivot/sunset | TODO | TODO | TODO | TODO |\n\n'
    printf '## Evidence Checklist\n\n'
    printf '%s\n' '- Usage pattern verified from logs: TODO'
    printf '%s\n' '- User feedback theme verified from comments/interviews: TODO'
    printf '%s\n' '- Error or failure mode reproduced: TODO'
    printf '%s\n\n' '- Expected impact tied to a measured baseline: TODO'
    printf '## Prioritization Notes\n\n'
    printf '%s\n' '- Prefer fixes tied to repeated user friction.'
    printf '%s\n' '- Prefer small changes when confidence is below the threshold.'
    printf '%s\n' '- Require human review before modifying published skills.'
} > "$REPORT_FILE"

echo "Evolution planning template created: $REPORT_FILE"
