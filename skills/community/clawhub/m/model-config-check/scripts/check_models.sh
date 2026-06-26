#!/bin/bash
# check_models.sh - 快速检查所有模型配置和连通性
# 用法: bash check_models.sh [config_path]

CONFIG="${1:-$HOME/.openclaw/openclaw.json}"
ISSUES=()
OK_COUNT=0
TOTAL=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo " 🔍 OpenClaw 模型配置校验"
echo "=========================================="
echo ""

if [ ! -f "$CONFIG" ]; then
    echo -e "${RED}❌ 配置文件不存在: ${CONFIG}${NC}"
    exit 1
fi
echo "✅ 配置文件: ${CONFIG}"
echo ""

# Extract providers
TMPEXTRACT=$(mktemp)
cat > "$TMPEXTRACT" << 'PYEOF'
import json, sys
config_path = sys.argv[1]
with open(config_path) as f:
    config = json.load(f)
providers = config.get("models", {}).get("providers", {})
for name, p in providers.items():
    models = [m["id"] for m in p.get("models", [])]
    base = p.get("baseUrl", "")
    key = p.get("apiKey", "")
    api = p.get("api", "")
    print(f"{name}\t{base}\t{key}\t{api}\t{','.join(models)}")
PYEOF

PROVIDERS=$(python3 "$TMPEXTRACT" "$CONFIG" 2>/dev/null)
rm -f "$TMPEXTRACT"

if [ -z "$PROVIDERS" ]; then
    echo -e "${RED}❌ 未找到任何模型 provider 配置${NC}"
    exit 1
fi

# Parser for Anthropic responses
TMPPARSE=$(mktemp)
cat > "$TMPPARSE" << 'PYPARSE'
import json, sys
resp_file = sys.argv[1]
with open(resp_file) as f:
    raw = f.read().strip()
if not raw:
    print("EMPTY")
    sys.exit(0)
try:
    r = json.loads(raw)
    # Check for text content
    for c in r.get("content", []):
        if c.get("type") == "text" and c.get("text", "").strip():
            print(c["text"].strip())
            sys.exit(0)
    # Check for thinking content (model is reasoning but didn't produce text yet)
    for c in r.get("content", []):
        if c.get("type") == "thinking" and c.get("thinking", "").strip():
            print("THINKING_ONLY: " + c["thinking"].strip()[:80])
            sys.exit(0)
    if "error" in r:
        print("ERROR: " + json.dumps(r["error"]))
    else:
        print("EMPTY")
except Exception as e:
    print("PARSE_FAIL: " + str(e))
PYPARSE

# Parser for OpenAI responses
TMPPARSE_OAI=$(mktemp)
cat > "$TMPPARSE_OAI" << 'PYPARSE'
import json, sys
resp_file = sys.argv[1]
with open(resp_file) as f:
    raw = f.read().strip()
if not raw:
    print("EMPTY")
    sys.exit(0)
try:
    r = json.loads(raw)
    choices = r.get("choices", [])
    if choices:
        msg = choices[0].get("message", {})
        content = msg.get("content", "")
        if content and content.strip():
            print(content.strip())
            sys.exit(0)
        reasoning = msg.get("reasoning_content", "")
        if reasoning and reasoning.strip():
            print("REASONING_ONLY: " + reasoning.strip()[:80])
            sys.exit(0)
    if "error" in r:
        print("ERROR: " + json.dumps(r["error"]))
    else:
        print("EMPTY")
except Exception as e:
    print("PARSE_FAIL: " + str(e))
PYPARSE

while IFS=$'\t' read -r NAME BASEURL APIKEY API_TYPE MODELS; do
    echo "----------------------------------------"
    echo "📦 Provider: ${NAME}"
    echo "   API 类型: ${API_TYPE}"
    echo "   Base URL: ${BASEURL}"

    if [ -z "$BASEURL" ]; then
        echo -e "   ${RED}❌ baseUrl 为空${NC}"
        ISSUES+=("${NAME}: baseUrl 为空")
        continue
    fi
    if [ -z "$APIKEY" ]; then
        echo -e "   ${RED}❌ apiKey 为空${NC}"
        ISSUES+=("${NAME}: apiKey 为空")
        continue
    fi
    echo -e "   ${GREEN}✅ 配置完整${NC}"

    # Network check
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$BASEURL" 2>/dev/null)
    if [ "$HTTP_CODE" = "000" ]; then
        echo -e "   ${RED}❌ 网络不可达${NC}"
        ISSUES+=("${NAME}: 网络不可达")
        continue
    fi
    echo -e "   ${GREEN}✅ 网络连通${NC} (HTTP ${HTTP_CODE})"

    IFS=',' read -ra MODEL_LIST <<< "$MODELS"
    for MODEL_ID in "${MODEL_LIST[@]}"; do
        TOTAL=$((TOTAL + 1))
        echo -n "   🧪 ${MODEL_ID} ... "

        TMPRESP=$(mktemp)

        if [[ "$API_TYPE" == *"anthropic"* ]]; then
            # Build URL: append /v1/messages if not already in the path
            if [[ "$BASEURL" == *"/v1/messages"* ]]; then
                FULL_URL="$BASEURL"
            else
                FULL_URL="${BASEURL%/}/v1/messages"
            fi

            curl -s -X POST "$FULL_URL" \
                -H "Content-Type: application/json" \
                -H "x-api-key: ${APIKEY}" \
                -H "anthropic-version: 2023-06-01" \
                -d "{\"model\":\"${MODEL_ID}\",\"max_tokens\":512,\"messages\":[{\"role\":\"user\",\"content\":\"reply ok\"}]}" \
                --connect-timeout 10 --max-time 60 \
                -o "$TMPRESP" 2>/dev/null

            TEXT=$(python3 "$TMPPARSE" "$TMPRESP" 2>/dev/null)

        else
            # OpenAI: construct the full endpoint URL
            # If baseUrl doesn't end with /chat/completions or /completions, append /chat/completions
            if [[ "$BASEURL" == *"/chat/completions" ]] || [[ "$BASEURL" == *"/completions" ]]; then
                OAI_URL="$BASEURL"
            else
                OAI_URL="${BASEURL%/}/chat/completions"
            fi

            curl -s -X POST "$OAI_URL" \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer ${APIKEY}" \
                -d "{\"model\":\"${MODEL_ID}\",\"messages\":[{\"role\":\"user\",\"content\":\"reply ok\"}],\"max_tokens\":512}" \
                --connect-timeout 10 --max-time 60 \
                -o "$TMPRESP" 2>/dev/null

            TEXT=$(python3 "$TMPPARSE_OAI" "$TMPRESP" 2>/dev/null)
        fi

        rm -f "$TMPRESP"

        if [[ "$TEXT" == "THINKING_ONLY"* ]] || [[ "$TEXT" == "REASONING_ONLY"* ]]; then
            echo -e "${YELLOW}⚠️  模型工作正常，输出在 reasoning 字段${NC}"
            OK_COUNT=$((OK_COUNT + 1))
        elif [[ "$TEXT" == "ERROR"* ]]; then
            echo -e "${RED}❌ ${TEXT}${NC}"
            ISSUES+=("${MODEL_ID}: ${TEXT}")
        elif [[ "$TEXT" == "EMPTY" ]] || [[ "$TEXT" == "PARSE_FAIL"* ]] || [ -z "$TEXT" ]; then
            echo -e "${RED}❌ 无返回内容${NC}"
            ISSUES+=("${MODEL_ID}: 无返回内容")
        else
            echo -e "${GREEN}✅ 返回: ${TEXT}${NC}"
            OK_COUNT=$((OK_COUNT + 1))
        fi
    done
    echo ""
done <<< "$PROVIDERS"

rm -f "$TMPPARSE" "$TMPPARSE_OAI"

echo "=========================================="
echo "📊 校验总结"
echo "=========================================="
echo "可用模型: ${OK_COUNT}/${TOTAL}"
echo ""

if [ ${#ISSUES[@]} -eq 0 ]; then
    echo -e "${GREEN}🎉 所有模型配置正常！${NC}"
else
    echo -e "${RED}⚠️  发现 ${#ISSUES[@]} 个问题:${NC}"
    for issue in "${ISSUES[@]}"; do
        echo "   • ${issue}"
    done
    echo ""
    echo "💡 修复建议:"
    echo "   - apiKey 无效 → 更新配置中的 apiKey"
    echo "   - HTTP 500 → 检查账户余额或联系服务商"
    echo "   - 连接超时 → 检查网络或 baseUrl"
    echo "   - 无返回内容 → 检查 model id 是否正确、max_tokens 是否充足"
fi
