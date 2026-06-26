---
name: mimo-api-fix
description: 诊断和修复 mimo-v2.5-pro（或其他 mimo 系列模型）调用失败的问题。当 LLM 请求返回 400 Param Incorrect、provider rejected the request schema or tool payload、或 providerRuntimeFailureKind=schema 时触发。用于排查 API 兼容性、tool calling 格式、模型配置等问题。
---

# mimo-api-fix

## 问题症状

OpenClaw 调用 mimo-v2.5-pro 时报错：
- `400 Param Incorrect`
- `provider rejected the request schema or tool payload`
- `failoverReason: "format"`
- `providerRuntimeFailureKind: "schema"`

系统会自动 fallback 到其他模型（如 qwen3.5:122b）。

## 诊断流程

### Step 1: 确认 API 端点可用

```bash
# 从配置获取 API key 和 baseUrl
API_KEY=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['models']['providers']['custom']['apiKey'])")
BASE_URL=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['models']['providers']['custom']['baseUrl'])")

# 测试基础连通性
curl -s "$BASE_URL/models" -H "Authorization: Bearer $API_KEY" | python3 -m json.tool | head -20
```

### Step 2: 测试无工具调用

```bash
curl -s "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role":"user","content":"hello, reply with one word"}],
    "max_tokens": 50
  }' | python3 -m json.tool
```

如果失败 → API 端点本身有问题，不是 OpenClaw 的问题。

### Step 3: 测试带工具调用

```bash
curl -s "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role":"user","content":"what is the weather? use get_weather tool"}],
    "tools": [{"type":"function","function":{"name":"get_weather","description":"Get weather","parameters":{"type":"object","properties":{"location":{"type":"string"}},"required":["location"]}}}],
    "max_tokens": 500
  }' | python3 -m json.tool
```

检查返回中 `finish_reason` 是否为 `"tool_calls"`，`tool_calls` 是否有内容。

### Step 4: 检查 OpenClaw 配置

```bash
python3 -c "
import json
d = json.load(open('$HOME/.openclaw/openclaw.json'))
for m in d['models']['providers']['custom']['models']:
    if 'mimo' in m.get('id',''):
        print(json.dumps(m, indent=2))
"
```

关键字段：
- `toolCall`: 如果为 `false`，工具调用被禁用
- `maxTokens`: 过高可能导致 API 拒绝
- `reasoning`: 某些 API 不支持

### Step 5: 检查日志获取精确错误

```bash
grep -i "mimo" /tmp/openclaw/openclaw-*.log | grep -i "error\|fail\|400" | tail -10
```

## 常见原因和修复

### 原因 1: 配置热加载竞态条件（最常见）

**症状**：之前能用，突然报 400，过一会儿又好了

**原因**：配置热加载瞬间有请求在处理，请求格式不一致

**修复**：通常无需处理，会自动恢复。如果持续报错，重启 gateway：
```bash
openclaw gateway restart
```

### 原因 2: toolCall 被误禁用

**症状**：模型能对话但不能调用工具

**检查**：查看配置中 `toolCall` 是否为 `false`

**修复**：
```bash
python3 -c "
import json
f = '$HOME/.openclaw/openclaw.json'
d = json.load(open(f))
for m in d['models']['providers']['custom']['models']:
    if 'mimo' in m.get('id',''):
        m['toolCall'] = True
json.dump(d, open(f,'w'), indent=2, ensure_ascii=False)
"
```

### 原因 3: API 端点不支持 function calling

**症状**：curl 测试带 tools 也返回 400

**修复**：确认使用的是正确的 mimo-v2.5-pro 端点，不是其他不支持 tools 的模型。

### 原因 4: 模型名称错误

**症状**：`model_not_found` 错误

**检查**：确认配置中 `id` 字段与 API 端点支持的模型名一致：
```bash
curl -s "$BASE_URL/models" -H "Authorization: Bearer $API_KEY" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for m in d['data']:
    print(m['id'])
"
```

## 运行诊断脚本

```bash
bash ~/.openclaw/workspace/skills/skills/mimo-api-fix/scripts/diagnose.sh
```
