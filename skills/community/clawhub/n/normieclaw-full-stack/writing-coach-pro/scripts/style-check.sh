#!/usr/bin/env bash
set -euo pipefail

# Writing Coach Pro — Style Consistency Check
# Quick scan for common style inconsistencies in a text file

usage() {
    echo "Usage: style-check.sh <file> [--style ap|chicago|apa] [--verbose]"
    echo ""
    echo "Scans a file for common style inconsistencies:"
    echo "  - Mixed number formatting (spelled out vs numerals)"
    echo "  - Inconsistent capitalization"
    echo "  - Hyphenation inconsistencies"
    echo "  - Oxford comma usage (mixed)"
    echo "  - Terminology shifts"
    echo ""
    echo "Options:"
    echo "  --style ap|chicago|apa   Style guide to check against (default: ap)"
    echo "  --verbose                Show line numbers for each finding"
    exit 0
}

if [ $# -lt 1 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    usage
fi

FILE="$1"
shift

if [ ! -f "${FILE}" ]; then
    echo "Error: File not found: ${FILE}"
    exit 1
fi

if [ ! -r "${FILE}" ]; then
    echo "Error: Cannot read file: ${FILE}"
    exit 1
fi

STYLE="ap"
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --style)
            STYLE="${2:-ap}"
            if [[ "${STYLE}" != "ap" && "${STYLE}" != "chicago" && "${STYLE}" != "apa" ]]; then
                echo "Error: Style must be 'ap', 'chicago', or 'apa'"
                exit 1
            fi
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

ISSUES=0
CONTENT=$(cat "${FILE}")
WORD_COUNT=$(echo "${CONTENT}" | wc -w | tr -d ' ')

echo "Writing Coach Pro — Style Check"
echo "================================"
echo "File: ${FILE}"
echo "Words: ${WORD_COUNT}"
echo "Style guide: ${STYLE}"
echo ""

# Check 1: Mixed number formatting
# Look for both spelled-out small numbers and digit small numbers
HAS_SPELLED=$(echo "${CONTENT}" | grep -ciE '\b(one|two|three|four|five|six|seven|eight|nine)\b' || true)
HAS_DIGITS=$(echo "${CONTENT}" | grep -cE '\b[1-9]\b' || true)

if [ "${HAS_SPELLED}" -gt 0 ] && [ "${HAS_DIGITS}" -gt 0 ]; then
    echo "⚠ NUMBERS: Mixed formatting — some small numbers spelled out, some as digits"
    if [ "${VERBOSE}" = true ]; then
        echo "  Spelled out:"
        grep -niE '\b(one|two|three|four|five|six|seven|eight|nine)\b' "${FILE}" | head -5 | sed 's/^/    /'
        echo "  As digits:"
        grep -nE '\b[1-9]\b' "${FILE}" | head -5 | sed 's/^/    /'
    fi
    ISSUES=$((ISSUES + 1))
fi

# Check 2: Inconsistent hyphenation of common words
for PAIR in "e-mail:email" "on-line:online" "web-site:website" "co-operate:cooperate"; do
    HYPHENATED="${PAIR%%:*}"
    UNHYPHENATED="${PAIR##*:}"
    HAS_H=$(echo "${CONTENT}" | grep -ci "${HYPHENATED}" || true)
    HAS_U=$(echo "${CONTENT}" | grep -ci "${UNHYPHENATED}" || true)
    if [ "${HAS_H}" -gt 0 ] && [ "${HAS_U}" -gt 0 ]; then
        echo "⚠ HYPHENATION: Mixed usage of '${HYPHENATED}' and '${UNHYPHENATED}'"
        ISSUES=$((ISSUES + 1))
    fi
done

# Check 3: Oxford comma inconsistency
# Look for "X, Y, and Z" vs "X, Y and Z" patterns
OXFORD=$(echo "${CONTENT}" | grep -cE ', and ' || true)
NO_OXFORD=$(echo "${CONTENT}" | grep -cE '[a-z], [a-z]+ and ' || true)

if [ "${OXFORD}" -gt 0 ] && [ "${NO_OXFORD}" -gt 0 ]; then
    if [ "${STYLE}" = "ap" ]; then
        echo "⚠ COMMAS: Oxford comma used inconsistently (AP style omits it)"
    elif [ "${STYLE}" = "chicago" ]; then
        echo "⚠ COMMAS: Oxford comma used inconsistently (Chicago style requires it)"
    else
        echo "⚠ COMMAS: Oxford comma used inconsistently"
    fi
    ISSUES=$((ISSUES + 1))
fi

# Check 4: Percent formatting
HAS_SYMBOL=$(echo "${CONTENT}" | grep -cE '[0-9]+%' || true)
HAS_WORD=$(echo "${CONTENT}" | grep -ci '[0-9]+ percent' || true)

if [ "${HAS_SYMBOL}" -gt 0 ] && [ "${HAS_WORD}" -gt 0 ]; then
    echo "⚠ FORMATTING: Mixed '%' symbol and 'percent' spelling"
    ISSUES=$((ISSUES + 1))
fi

# Check 5: Heading capitalization consistency (markdown files)
if [[ "${FILE}" == *.md ]]; then
    TITLE_CASE=$(grep -cE '^#{1,3} ([A-Z][a-z]+ ){2,}[A-Z]' "${FILE}" || true)
    SENTENCE_CASE=$(grep -cE '^#{1,3} [A-Z][a-z]+ [a-z]' "${FILE}" || true)
    if [ "${TITLE_CASE}" -gt 0 ] && [ "${SENTENCE_CASE}" -gt 0 ]; then
        echo "⚠ HEADINGS: Mixed title case and sentence case in headings"
        ISSUES=$((ISSUES + 1))
    fi
fi

# Check 6: Common terminology pairs
for PAIR in "client:customer" "app:application" "user:end-user" "setup:set up"; do
    TERM_A="${PAIR%%:*}"
    TERM_B="${PAIR##*:}"
    HAS_A=$(echo "${CONTENT}" | grep -ciw "${TERM_A}" || true)
    HAS_B=$(echo "${CONTENT}" | grep -ciw "${TERM_B}" || true)
    if [ "${HAS_A}" -gt 2 ] && [ "${HAS_B}" -gt 2 ]; then
        echo "⚠ TERMINOLOGY: Both '${TERM_A}' (${HAS_A}x) and '${TERM_B}' (${HAS_B}x) used — pick one"
        ISSUES=$((ISSUES + 1))
    fi
done

# Check 7: Passive voice density (rough heuristic)
PASSIVE_MARKERS=$(echo "${CONTENT}" | grep -ciE '\b(is|was|were|are|been|being) [a-z]+ed\b' || true)
SENTENCE_COUNT=$(echo "${CONTENT}" | grep -cE '[.!?]' || true)
if [ "${SENTENCE_COUNT}" -gt 0 ]; then
    # Rough passive percentage
    PASSIVE_PCT=$((PASSIVE_MARKERS * 100 / SENTENCE_COUNT))
    if [ "${PASSIVE_PCT}" -gt 25 ]; then
        echo "⚠ VOICE: High passive voice density (~${PASSIVE_PCT}% of sentences)"
    fi
fi

echo ""
if [ "${ISSUES}" -eq 0 ]; then
    echo "✓ No style inconsistencies detected. Looking clean."
else
    echo "Found ${ISSUES} style inconsistency issue(s)."
    echo "For a full analysis, paste the text to your agent and say 'full review'."
fi
