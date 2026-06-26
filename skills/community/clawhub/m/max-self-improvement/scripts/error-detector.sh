#!/bin/bash
# Error Detector Script for Max-Self-Improvement
# Detects command errors and prompts for learning entry

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LEARNINGS_DIR="$SKILL_DIR/.learnings"

# Get last exit code
EXIT_CODE=${1:-$?}
TOOL_OUTPUT=${2:-""}

# Only log if there was an error
if [ "$EXIT_CODE" -eq 0 ] && [ -z "$TOOL_OUTPUT" ]; then
    exit 0
fi

# Generate error ID
DATE=$(date +%Y%m%d)
RANDOM_ID=$(head /dev/urandom | tr -dc 'A-Z0-9' | head -c 3)
ERROR_ID="ERR-${DATE}-${RANDOM_ID}"

# Check if learnings directory exists
if [ ! -d "$LEARNINGS_DIR" ]; then
    mkdir -p "$LEARNINGS_DIR"
fi

# Create error entry
ERRORS_FILE="$LEARNINGS_DIR/ERRORS.md"

# Check if file exists and has content
if [ ! -s "$ERRORS_FILE" ]; then
    echo "# Errors Log" > "$ERRORS_FILE"
    echo "" >> "$ERRORS_FILE"
    echo "Record of command failures, exceptions, and tool call errors." >> "$ERRORS_FILE"
    echo "" >> "$ERRORS_FILE"
    echo "---" >> "$ERRORS_FILE"
    echo "" >> "$ERRORS_FILE"
fi

# Append error entry
TIMESTAMP=$(date -Iseconds)

cat >> "$ERRORS_FILE" << EOF
## [$ERROR_ID] bash_command

**Logged**: $TIMESTAMP
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Command exited with non-zero status or unexpected output

### Error
\`\`\`
Exit code: $EXIT_CODE
Output: ${TOOL_OUTPUT:-(no output captured)}
\`\`\`

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: unknown
- Related Files: (none)
- See Also: (none)

---
EOF

echo "Error logged to $ERRORS_FILE"
echo "Entry ID: $ERROR_ID"
