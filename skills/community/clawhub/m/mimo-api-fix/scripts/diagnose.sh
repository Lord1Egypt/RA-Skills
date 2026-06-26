#!/bin/bash
# mimo-api-fix 诊断脚本
# 用法: bash diagnose.sh

CONFIG="$HOME/.openclaw/openclaw.json"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== mimo API 诊断 ==="
echo ""

if [ ! -f "$CONFIG" ]; then
    echo -e "${RED}✗ 配置文件不存在: $CONFIG${NC}"
    exit 1
fi

API_KEY=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(d['models']['providers']['custom']['apiKey'])")
BASE_URL=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(d['models']['providers']['custom']['baseUrl'])")

echo "API: $BASE_URL"
echo ""

# Test 1: 连通性
echo "--- Test 1: API 连通性 ---"
MODELS=$(curl -s --connect-timeout 5 "$BASE_URL/models" -H "Authorization: Bearer $API_KEY" 2>/dev/null || true)
if echo "$MODELS" | python3 -c "import json,sys; d=json.load(sys.stdin); assert 'data' in d" 2>/dev/null; then
    echo -e "${GREEN}✓ API 端点可达${NC}"
    MIMO_MODELS=$(echo "$MODELS" | python3 -c "import json,sys; d=json.load(sys.stdin); print([m['id'] for m in d['data'] if 'mimo' in m['id']])")
    echo "  可用 mimo 模型: $MIMO_MODELS"
else
    echo -e "${RED}✗ API 端点不可达或返回错误${NC}"
    echo "  响应: $(echo $MODELS | head -c 200)"
    exit 1
fi
echo ""

# Test 2: 无工具调用
echo "--- Test 2: 无工具调用 ---"
RESULT=$(curl -s --connect-timeout 10 "$BASE_URL/chat/completions" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"mimo-v2.5-pro","messages":[{"role":"user","content":"hello, reply with one word"}],"max_tokens":50}' 2>/dev/null || true)
HAS_CONTENT=$(echo "$RESULT" | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    c=d.get('choices',[{}])[0].get('message',{}).get('content','')
    print('ok:'+c if c else 'fail:no_content')
except: print('fail:parse_error')
" 2>/dev/null)
if [[ "$HAS_CONTENT" == ok:* ]]; then
    echo -e "${GREEN}✓ 基础调用正常${NC}"
    echo "  回复: ${HAS_CONTENT#ok:}"
else
    echo -e "${RED}✗ 基础调用失败${NC}"
    echo "  状态: $HAS_CONTENT"
    echo "  响应: $(echo $RESULT | head -c 300)"
    exit 1
fi
echo ""

# Test 3: 带工具调用
echo "--- Test 3: 带工具调用 ---"
TOOL_RESULT=$(curl -s --connect-timeout 10 "$BASE_URL/chat/completions" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"mimo-v2.5-pro","messages":[{"role":"user","content":"what is the weather in hangzhou? use get_weather tool"}],"tools":[{"type":"function","function":{"name":"get_weather","description":"Get weather","parameters":{"type":"object","properties":{"location":{"type":"string"}},"required":["location"]}}}],"max_tokens":500}' 2>/dev/null || true)
TOOL_CHECK=$(echo "$TOOL_RESULT" | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    tc=d.get('choices',[{}])[0].get('message',{}).get('tool_calls')
    fr=d.get('choices',[{}])[0].get('finish_reason','')
    if tc:
        print('ok:'+tc[0]['function']['name'])
    else:
        print('fail:no_tool_calls,finish_reason='+fr)
except Exception as e: print('fail:'+str(e))
" 2>/dev/null)
if [[ "$TOOL_CHECK" == ok:* ]]; then
    echo -e "${GREEN}✓ 工具调用正常${NC}"
    echo "  调用: ${TOOL_CHECK#ok:}"
else
    echo -e "${RED}✗ 工具调用失败${NC}"
    echo "  状态: $TOOL_CHECK"
    echo "  响应: $(echo $TOOL_RESULT | head -c 300)"
fi
echo ""

# Test 4: OpenClaw 配置检查
echo "--- Test 4: OpenClaw 配置 ---"
python3 -c "
import json
d = json.load(open('$CONFIG'))
models = d['models']['providers']['custom']['models']
for m in models:
    if 'mimo' in m.get('id',''):
        tc = m.get('toolCall', '未设置')
        mt = m.get('maxTokens', '未设置')
        r = m.get('reasoning', '未设置')
        print(f'  model: {m[\"id\"]}')
        print(f'  toolCall: {tc}')
        print(f'  maxTokens: {mt}')
        print(f'  reasoning: {r}')
        if tc is False:
            print('  ⚠️  toolCall=false 会导致工具调用被禁用！')
" 2>/dev/null
echo ""

# Test 5: 日志检查
echo "--- Test 5: 最近日志 ---"
LOG_FILE="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
if [ -f "$LOG_FILE" ]; then
    ERRORS=$(grep -i "mimo" "$LOG_FILE" 2>/dev/null | grep -i "error\|fail\|400" | tail -3)
    if [ -n "$ERRORS" ]; then
        echo -e "${YELLOW}⚠ 发现错误日志:${NC}"
        echo "$ERRORS"
    else
        echo -e "${GREEN}✓ 无 mimo 相关错误${NC}"
    fi
else
    echo "  日志文件不存在"
fi
echo ""

echo "=== 诊断完成 ==="
