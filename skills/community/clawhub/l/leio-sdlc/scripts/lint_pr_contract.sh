#!/usr/bin/env bash
# Lints a PR contract markdown file.

if [ -z "$1" ]; then
    echo "Usage: $0 <contract_file.md>"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File $FILE does not exist."
    exit 1
fi

REQUIRED_SECTIONS=(
    "## 1. Objective" 
    "## 2. Target Working Set & File Placement" 
    "## 3. Implementation Scope" 
    "## 4. TDD Blueprint & Acceptance Criteria"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$FILE"; then
        echo "Error: Missing section '$section'"
        exit 1
    fi
done

exit 0
