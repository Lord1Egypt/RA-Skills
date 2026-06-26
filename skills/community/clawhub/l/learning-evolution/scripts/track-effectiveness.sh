#!/bin/bash
#
# track-effectiveness.sh - Create a verified-data effectiveness template.
# Usage: ./track-effectiveness.sh --skill <name> [--since YYYY-MM-DD]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${LEARNING_DATA_DIR:-$SKILL_DIR/data}"

SKILL_NAME=""
SINCE="$(date -d '30 days ago' +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d)"

while [[ $# -gt 0 ]]; do
    case $1 in
        --skill)
            SKILL_NAME="$2"
            shift 2
            ;;
        --since)
            SINCE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$SKILL_NAME" ]]; then
    echo "Usage: $0 --skill <name> [--since YYYY-MM-DD]"
    exit 1
fi

if [[ ! "$SKILL_NAME" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,100}$ ]]; then
    echo "Skill name must use only letters, numbers, dot, underscore, or hyphen"
    exit 1
fi

if [[ ! "$SINCE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "Since must use YYYY-MM-DD"
    exit 1
fi

mkdir -p "$DATA_DIR"

REPORT_FILE="$DATA_DIR/EFFECTIVENESS-${SKILL_NAME}-$(date +%Y%m%d).md"
GENERATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TODAY="$(date +%Y-%m-%d)"

{
    printf '# Effectiveness Review Template: %s\n\n' "$SKILL_NAME"
    printf '**Period**: %s to %s\n' "$SINCE" "$TODAY"
    printf '**Generated**: %s\n' "$GENERATED_AT"
    printf '**Data Policy**: This file is a review template. It intentionally leaves metrics blank until verified data is provided.\n\n'
    printf '## Success Metrics\n\n'
    printf '| Metric | Verified Value | Target | Status | Evidence |\n'
    printf '|--------|----------------|--------|--------|----------|\n'
    printf '| Task completion | TODO | TODO | TODO | TODO |\n'
    printf '| User satisfaction | TODO | TODO | TODO | TODO |\n'
    printf '| Return rate | TODO | TODO | TODO | TODO |\n'
    printf '| Error rate | TODO | TODO | TODO | TODO |\n\n'
    printf '## Error Analysis\n\n'
    printf '| Error Type | Count | Severity | Reproduction Notes |\n'
    printf '|------------|-------|----------|--------------------|\n'
    printf '| TODO | TODO | TODO | TODO |\n\n'
    printf '## Evidence-Backed Recommendations\n\n'
    printf '%s\n' '- Recommendation 1: TODO'
    printf '%s\n' '- Recommendation 2: TODO'
    printf '%s\n\n' '- Recommendation 3: TODO'
    printf '## Human Review Gate\n\n'
    printf '%s\n' '- Confirm metrics came from trusted logs or direct feedback.'
    printf '%s\n' '- Confirm no sensitive user data is retained unnecessarily.'
    printf '%s\n' '- Do not change another skill based on this report until evidence is filled in.'
} > "$REPORT_FILE"

echo "Effectiveness review template created: $REPORT_FILE"
