#!/bin/bash
# AI Task Router - Route tasks to the right tool/agent
# Usage: bash route-task.sh "your task description"

TASK="$1"

if [ -z "$TASK" ]; then
    echo "Usage: bash route-task.sh '<task description>'"
    exit 1
fi

echo "📋 Task: $TASK"
echo ""

# Analyze task and route
ROUTE="general"
CONFIDENCE=0.5
REASON=""

# Coding patterns
if echo "$TASK" | grep -qiE "(code|script|function|class|debug|fix|build|create \w+|write|python|javascript|sql|api)"; then
    ROUTE="coding"
    CONFIDENCE=0.85
    REASON="Detected coding keywords"
fi

# Research patterns
if echo "$TASK" | grep -qiE "(search|find|research|look up|analyze|compare|what is|who is|when|difference between)"; then
    if [ "$ROUTE" = "general" ]; then
        ROUTE="research"
        CONFIDENCE=0.75
        REASON="Detected research keywords"
    fi
fi

# Trading/DeFi patterns
if echo "$TASK" | grep -qiE "(trade|swap|buy|sell|wallet|balance|defi|nft|token|price|liquidity|farm|stake)"; then
    ROUTE="trading"
    CONFIDENCE=0.90
    REASON="Detected trading/DeFi keywords"
fi

# System/ops patterns
if echo "$TASK" | grep -qiE "(run|execute|cron|schedule|monitor|check|status|restart|deploy|install|update)"; then
    if [ "$ROUTE" = "general" ]; then
        ROUTE="system"
        CONFIDENCE=0.80
        REASON="Detected system operation keywords"
    fi
fi

# Content patterns
if echo "$TASK" | grep -qiE "(write|summarize|translate|blog|post|tweet|content|article|description)"; then
    if [ "$ROUTE" = "general" ]; then
        ROUTE="content"
        CONFIDENCE=0.70
        REASON="Detected content keywords"
    fi
fi

# Check complexity
WORD_COUNT=$(echo "$TASK" | wc -w)
if [ "$WORD_COUNT" -gt 15 ]; then
    COMPLEXITY="high"
elif [ "$WORD_COUNT" -gt 5 ]; then
    COMPLEXITY="medium"
else
    COMPLEXITY="low"
fi

# Output routing decision
echo "🎯 Route: $ROUTE"
echo "📊 Confidence: $CONFIDENCE"
echo "📝 Reason: $REASON"
echo "🔢 Complexity: $COMPLEXITY (words: $WORD_COUNT)"
echo ""

# Tool suggestion
case "$ROUTE" in
    coding)   TOOL="codex / claude-code / cursor" ;;
    research) TOOL="web_search / exa-plus / browser" ;;
    trading)  TOOL="trading bot / lighter / variational" ;;
    system)   TOOL="exec / crontab / openclaw CLI" ;;
    content)  TOOL="writer / summarizer / translate" ;;
    general)  TOOL="general LLM chat" ;;
esac

echo "🔧 Suggested tool: $TOOL"
