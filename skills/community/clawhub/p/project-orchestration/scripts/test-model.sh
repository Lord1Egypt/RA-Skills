#!/usr/bin/env bash
# test-model.sh — Check if a model endpoint is reachable and report basic info
# Usage: bash scripts/test-model.sh <model-id>
#
# This is a CONNECTIVITY check, not a capability test.
# For actual capability testing (tool calls, reasoning, vision),
# use OpenClaw's session_status and spawn a test subagent.
#
# Examples:
#   bash scripts/test-model.sh lmstudio/local/qwen3.6-35b
#   bash scripts/test-model.sh openrouter/deepseek/deepseek-v4-flash

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
MODELS_JSON="$DATA_DIR/models.json"

MODEL_ID="${1:-}"

if [ -z "$MODEL_ID" ]; then
    echo "Usage: bash scripts/test-model.sh <model-id>"
    echo ""
    echo "Checks if a model endpoint is reachable."
    echo "For capability testing, use OpenClaw's session tools."
    echo ""
    echo "Examples:"
    echo "  bash scripts/test-model.sh lmstudio/local/qwen3.6-35b"
    echo "  bash scripts/test-model.sh openrouter/deepseek/deepseek-v4-flash"
    exit 1
fi

echo "🧪 Testing connectivity: $MODEL_ID"
echo ""

# Determine provider from model ID
PROVIDER=$(echo "$MODEL_ID" | cut -d'/' -f1)
ALL_PASSED=true

# Test 1: Check if model is in inventory
echo "  [1/3] Inventory check..."
if [ -f "$MODELS_JSON" ]; then
    if grep -q "\"$MODEL_ID\"" "$MODELS_JSON" 2>/dev/null; then
        echo "    ✅ Found in models.json"
    else
        echo "    ⚠️  Not in models.json — run discover-models.sh or add manually"
    fi
else
    echo "    ⚠️  models.json not found — run discover-models.sh first"
fi

# Test 2: Check endpoint reachability
echo "  [2/3] Endpoint check..."
case "$PROVIDER" in
    lmstudio|local)
        ENDPOINT="http://localhost:1234/v1/models"
        if curl -s --max-time 5 "$ENDPOINT" | grep -q '"data"' 2>/dev/null; then
            echo "    ✅ LM Studio reachable at localhost:1234"
        else
            echo "    ❌ LM Studio not reachable at localhost:1234"
            ALL_PASSED=false
        fi
        ;;
    openrouter)
        ENDPOINT="https://openrouter.ai/api/v1/models"
        if curl -s --max-time 10 "$ENDPOINT" | grep -q '"data"' 2>/dev/null; then
            echo "    ✅ OpenRouter reachable"
        else
            echo "    ⚠️  OpenRouter check failed (may be rate limited)"
        fi
        ;;
    opencode)
        if command -v opencode &>/dev/null; then
            echo "    ✅ opencode CLI found"
        else
            echo "    ⚠️  opencode CLI not found locally"
        fi
        ;;
    *)
        echo "    ℹ️  Unknown provider '$PROVIDER' — cannot check endpoint automatically"
        echo "       Verify manually that this model is accessible"
        ;;
esac

# Test 3: Check if model is listed by its provider
echo "  [3/3] Provider listing check..."
case "$PROVIDER" in
    lmstudio|local)
        RESULT=$(curl -s --max-time 5 "http://localhost:1234/v1/models" 2>/dev/null || echo '{"data":[]}')
        if echo "$RESULT" | grep -q "\"$MODEL_ID\"" 2>/dev/null; then
            echo "    ✅ Model confirmed in LM Studio model list"
        else
            echo "    ⚠️  Model not found in LM Studio model list"
            echo "       (LM Studio may need to load the model first)"
        fi
        ;;
    openrouter)
        RESULT=$(curl -s --max-time 10 "https://openrouter.ai/api/v1/models" 2>/dev/null || echo '{"data":[]}')
        if echo "$RESULT" | grep -q "\"$MODEL_ID\"" 2>/dev/null; then
            echo "    ✅ Model confirmed on OpenRouter"
        else
            echo "    ⚠️  Model not found in OpenRouter listing"
        fi
        ;;
    *)
        echo "    ℹ️  Skipping provider listing check for $PROVIDER"
        ;;
esac

echo ""
if $ALL_PASSED; then
    echo "✅ Connectivity OK for $MODEL_ID"
else
    echo "⚠️  Some checks failed for $MODEL_ID"
    echo "   The model may still work via OpenClaw routing"
fi