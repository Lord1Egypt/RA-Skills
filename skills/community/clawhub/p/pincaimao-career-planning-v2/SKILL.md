---
name: pincaimao-career-planning-v2
description: 聘才猫 - 职业规划助手 V2 Use when calling Pincaimao Career Planning Assistant V2 API to generate career advice based on a resume and advice type. Requires PCM_CAREER_PLANNING_KEY env var.
version: 1.0.1
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "🚀"
    homepage: https://www.pincaimao.com
    primaryEnv: PCM_CAREER_PLANNING_KEY
    requires:
      env:
        - PCM_CAREER_PLANNING_KEY
      bins:
        - curl
        - python3
---

# 聘才猫 - 职业规划助手 V2

**REQUIRED:** 请先检查是否已安装 `pincaimao-basic`，若未安装请先安装，然后加载它了解通用接口（文件上传、鉴权、响应格式、SSE 解析模板）。

**环境变量**：`PCM_CAREER_PLANNING_KEY`（智能体专属 key）
> 还没有密钥？通过邀请链接注册并完成认证即可免费获取：[pincaimao.com/agents/login?invite_code=uwqc](https://www.pincaimao.com/agents/login?invite_code=uwqc)

## 调用前的信息确认

执行前需要确认：**简历文件** 和 **建议类型**。

确认策略：
- 上下文中已有相关信息 → 展示摘要并询问是否使用
- 上下文中没有 → 直接请用户提供

询问建议类型（三选一）：
> "请选择职业建议类型：初入职场 / 转型建议 / 晋升路径"

## 请求参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `inputs.type` | 是 | 建议类型，固定三选一：`初入职场`、`转型建议`、`晋升路径` |
| `inputs.file_url` | 是 | 简历文件的 cos_key |
| `query` | 是 | 固定值 `"分析简历，提出职业建议"` |

## 完整示例

```bash
#!/bin/bash
RESUME_FILE="/path/to/resume.pdf"
ADVICE_TYPE="晋升路径"  # 初入职场 | 转型建议 | 晋升路径

# Step 1: 上传简历
UPLOAD=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/files/upload' \
  -H "Authorization: Bearer $PCM_CAREER_PLANNING_KEY" \
  -F "file=@$RESUME_FILE")
COS_KEY=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['cos_key'])")

# Step 2: 生成职业建议
curl -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer $PCM_CAREER_PLANNING_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"query\": \"分析简历，提出职业建议\",
    \"inputs\": {
      \"type\": \"$ADVICE_TYPE\",
      \"file_url\": \"$COS_KEY\"
    },
    \"response_mode\": \"blocking\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

## 常见错误

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | Key 错误 | 检查 `PCM_CAREER_PLANNING_KEY` |
| 建议内容不相关 | `type` 传了非法值 | 只能是 `初入职场`、`转型建议`、`晋升路径` 之一 |
| answer 为空 | `query` 不是固定值 | `query` 必须固定传 `"分析简历，提出职业建议"` |

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
