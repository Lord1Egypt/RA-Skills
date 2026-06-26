#!/bin/bash
# Pre-task learning retrieval
# Usage: ./pre-task-check.sh <task-type> [keywords...]

SEARCH_SCRIPT="$HOME/.openclaw/workspace/skills/keenlycat-self-improving-agent/search-learnings.sh"

if [[ $# -lt 1 ]]; then
    echo "Usage: ./pre-task-check.sh <task-type> [keywords...]"
    echo ""
    echo "Examples:"
    echo "  ./pre-task-check.sh deployment"
    echo "  ./pre-task-check.sh npm install"
    echo "  ./pre-task-check.sh feishu configuration"
    exit 1
fi

TASK_TYPE="$1"
shift

echo "🔍 Pre-task Learning Check"
echo "=========================="
echo "Task: $TASK_TYPE $*"
echo ""

# Search for relevant learnings
if [[ -x "$SEARCH_SCRIPT" ]]; then
    echo "📚 Searching for relevant learnings..."
    echo ""
    
    # Search by task type and keywords
    "$SEARCH_SCRIPT" "$TASK_TYPE $*" --limit 5
    
    echo ""
    echo "💡 Tip: Review these learnings before starting your task!"
    echo ""
else
    echo "❌ Search script not found. Make sure the skill is installed."
fi
