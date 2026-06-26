---
name: pincaimao-interview-question
description: 聘才猫 - 面试出题大师 Use when calling Pincaimao Interview Question Master API to generate interview questions based on a job description and candidate resume. Requires PCM_INTERVIEW_QUESTIONS_KEY env var.
version: 1.0.1
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "❓"
    homepage: https://www.pincaimao.com
    primaryEnv: PCM_INTERVIEW_QUESTIONS_KEY
    requires:
      env:
        - PCM_INTERVIEW_QUESTIONS_KEY
      bins:
        - curl
        - python3
---

# 聘才猫 - 面试出题大师

**REQUIRED:** 请先检查是否已安装 `pincaimao-basic`，若未安装请先安装，然后加载它了解通用接口（文件上传、鉴权、响应格式、SSE 解析模板）。

**环境变量**：`PCM_INTERVIEW_QUESTIONS_KEY`（智能体专属 key）
> 还没有密钥？通过邀请链接注册并完成认证即可免费获取：[pincaimao.com/agents/login?invite_code=uwqc](https://www.pincaimao.com/agents/login?invite_code=uwqc)

## 调用前的信息确认

执行前需要确认：**职位描述（job_info）** 和 **简历文件**。

确认策略：
- 上下文中已有相关信息 → 展示摘要并询问是否使用，例如：
  > "检测到上下文中有一份 JD（XXX），是否使用这个？"
- 上下文中没有 → 直接请用户提供

同时询问：
- **题目数量**（question_number，默认 6）
- **是否输出分析**（can_outputAnalysis，默认 `"false"`）

## 请求参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `inputs.job_info` | 是 | 职位描述全文 |
| `inputs.file_url` | 是 | 简历文件的 cos_key |
| `inputs.job_title` | 否 | 职位名称 |
| `inputs.question_number` | 否 | 题目数量，默认 6，类型为数字 |
| `inputs.can_outputAnalysis` | 否 | 是否输出分析，字符串 `"true"` 或 `"false"`，默认 `"false"` |
| `query` | 是 | job_info 前 20 个字符，无 job_info 时用文件名 |

## 完整示例

```bash
#!/bin/bash
RESUME_FILE="/path/to/resume.docx"
JOB_INFO="高级销售专员 / 销售主管，行业领先平台，完善晋升通道和培训体系"
JOB_TITLE="高级销售专员"

# Step 1: 上传简历
UPLOAD=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/files/upload' \
  -H "Authorization: Bearer $PCM_INTERVIEW_QUESTIONS_KEY" \
  -F "file=@$RESUME_FILE")
COS_KEY=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['cos_key'])")

# Step 2: 生成面试题
QUERY=$(echo "$JOB_INFO" | cut -c1-20)
curl -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer $PCM_INTERVIEW_QUESTIONS_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"query\": \"$QUERY\",
    \"inputs\": {
      \"job_info\": \"$JOB_INFO\",
      \"file_url\": \"$COS_KEY\",
      \"job_title\": \"$JOB_TITLE\",
      \"question_number\": 6,
      \"can_outputAnalysis\": \"false\"
    },
    \"response_mode\": \"blocking\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

## 常见错误

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | Key 错误 | 检查 `PCM_INTERVIEW_QUESTIONS_KEY` |
| 题目数量不对 | `question_number` 传成了字符串 | 确保传数字类型 `6`，不是 `"6"` |
| `can_outputAnalysis` 无效 | 传成了布尔值 | 必须是字符串 `"true"` 或 `"false"` |
| answer 为空 | `file_url` 传了 `presigned_url` | 用上传响应的 `cos_key` 字段 |

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
