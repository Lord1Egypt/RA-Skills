#!/bin/bash
SEARCH_STR="Review"_"Report.md"
matches=$(grep -rn --exclude="test_legacy_string_cleanup.sh" --exclude-dir="__pycache__" "$SEARCH_STR" scripts/ tests/ config/ playbooks/ 2>/dev/null)

if [ -n "$matches" ]; then
    echo "Found legacy string '$SEARCH_STR' in the following files:"
    echo "$matches"
    exit 1
else
    echo "No legacy strings found. Cleanup successful."
    exit 0
fi
