---
name: pincaimao-labor-contracts
description: 聘才猫 - 劳动合同卫士 Use when calling Pincaimao Labor Contract Guard API to analyze a labor contract and generate an assessment report. Accepts either a contract file (cos_key) or contract text directly. Requires PCM_LABOR_CONTRACT_KEY env var.
version: 1.0.1
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "⚖️"
    homepage: https://www.pincaimao.com
    primaryEnv: PCM_LABOR_CONTRACT_KEY
    requires:
      env:
        - PCM_LABOR_CONTRACT_KEY
      bins:
        - curl
        - python3
---

# 聘才猫 - 劳动合同卫士

**REQUIRED:** 请先检查是否已安装 `pincaimao-basic`，若未安装请先安装，然后加载它了解通用接口（文件上传、鉴权、响应格式、SSE 解析模板）。

**环境变量**：`PCM_LABOR_CONTRACT_KEY`（智能体专属 key）
> 还没有密钥？通过邀请链接注册并完成认证即可免费获取：[pincaimao.com/agents/login?invite_code=uwqc](https://www.pincaimao.com/agents/login?invite_code=uwqc)

## 调用前的信息确认

执行前需确认合同内容来源（二选一）：

> "请问要分析的劳动合同是文件（docx/pdf）还是直接粘贴文本内容？"

- 文件 → 先上传获取 cos_key，传入 `file_url`
- 文本 → 直接传入 `input`

## 请求参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `inputs.file_url` | 二选一 | 合同文件的 cos_key |
| `inputs.input` | 二选一 | 合同文本内容 |
| `query` | 是 | 固定值 `"请对劳动合同进行分析"` |

`file_url` 与 `input` 必须提供其中一个，另一个传空字符串 `""`。

## 完整示例

### 方式一：上传文件

```bash
CONTRACT_FILE="/path/to/contract.docx"

# Step 1: 上传合同文件
UPLOAD=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/files/upload' \
  -H "Authorization: Bearer $PCM_LABOR_CONTRACT_KEY" \
  -F "file=@${CONTRACT_FILE}")
COS_KEY=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['cos_key'])")

# Step 2: 分析合同（用 Python 构造 JSON，避免 shell 注入）
python3 -c "
import json, urllib.request, os, sys
key = os.environ['PCM_LABOR_CONTRACT_KEY']
payload = json.dumps({
    'query': '请对劳动合同进行分析',
    'inputs': {'file_url': sys.argv[1], 'input': ''},
    'response_mode': 'blocking'
}).encode()
req = urllib.request.Request(
    'https://api.pincaimao.com/agents/v1/chat/chat-messages',
    data=payload,
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
)
resp = json.loads(urllib.request.urlopen(req).read())
print(resp['answer'])
" "$COS_KEY"
```

### 方式二：直接传文本

```bash
CONTRACT_TEXT="劳动合同
甲方（用人单位）：深圳市创新科技有限公司
乙方（劳动者）：..."

# 用 Python 构造 JSON，CONTRACT_TEXT 作为参数传入，避免 shell 注入
python3 -c "
import json, urllib.request, os, sys
key = os.environ['PCM_LABOR_CONTRACT_KEY']
payload = json.dumps({
    'query': '请对劳动合同进行分析',
    'inputs': {'file_url': '', 'input': sys.argv[1]},
    'response_mode': 'blocking'
}).encode()
req = urllib.request.Request(
    'https://api.pincaimao.com/agents/v1/chat/chat-messages',
    data=payload,
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
)
resp = json.loads(urllib.request.urlopen(req).read())
print(resp['answer'])
" "$CONTRACT_TEXT"
```

## 常见错误

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | Key 错误 | 检查 `PCM_LABOR_CONTRACT_KEY` |
| answer 为空 | `query` 不是固定值 | `query` 必须固定传 `"请对劳动合同进行分析"` |
| 分析结果不完整 | `file_url` 和 `input` 都为空 | 两者至少提供一个，另一个传 `""` |

## 输出模式

- **默认**：AI 对 API 返回结果进行整理表述，输出更易读的内容
- **原始输出**：用户说"显示原始输出"或"raw output"时，将 API 返回的原始内容用代码块原样展示，不作任何改动
  - Blocking 模式：直接取 `answer` 字段内容原样输出
  - Streaming 模式：将所有 `message` / `agent_message` 事件的 `answer` 片段拼接完整后，原样输出，不作重述

---

## External Endpoints

- `https://api.pincaimao.com` — Pincaimao platform API (chat, file upload, conversations)

## Security & Privacy

- API key is read from environment variable and passed via `Authorization` header; never hardcoded
- Resume files, job descriptions, and contract text are transmitted to `api.pincaimao.com` for AI processing
- Uploaded files are stored on Pincaimao's COS (Cloud Object Storage); returned `cos_key` paths should be treated as sensitive
- This skill does not store, log, or transmit data to any endpoint other than `api.pincaimao.com`
- Safe to invoke autonomously; all network calls are scoped to the authenticated user's API key
