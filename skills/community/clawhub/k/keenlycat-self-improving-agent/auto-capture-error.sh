#!/bin/bash
# Auto-capture errors from command execution
# Usage: ./auto-capture-error.sh <command> [args...]

set -e

LEARNINGS_FILE="$HOME/.openclaw/workspace/memory/learnings.jsonl"
CAPTURE_SCRIPT="$HOME/.openclaw/workspace/skills/keenlycat-self-improving-agent/capture-learning.sh"

# Execute command and capture output
echo "🔧 Executing: $*"
echo ""

# Run command and capture exit code
set +e
OUTPUT=$("$@" 2>&1)
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -ne 0 ]]; then
    echo ""
    echo "❌ Command failed with exit code $EXIT_CODE"
    echo ""
    echo "Output:"
    echo "$OUTPUT"
    echo ""
    
    # Auto-capture as learning
    if [[ -x "$CAPTURE_SCRIPT" ]]; then
        echo "📝 Capturing error as learning..."
        
        # Extract error summary (first 200 chars)
        ERROR_SUMMARY=$(echo "$OUTPUT" | head -c 200 | tr '\n' ' ' | tr '"' "'")
        
        # Capture learning
        "$CAPTURE_SCRIPT" \
            --type error \
            --severity high \
            --context "Command failed: $*" \
            --issue "$ERROR_SUMMARY" \
            --correction "Review error and fix" \
            --lesson "Command '$1' failed, review error message for details" \
            --tags "auto-captured,command-error" \
            --task-slug "cmd-$1"
        
        echo ""
        echo "✅ Error captured! Review with: ./search-learnings.sh --type error"
    fi
    
    exit $EXIT_CODE
else
    echo "✅ Command succeeded!"
    echo "$OUTPUT"
fi
