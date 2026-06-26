---
name: pincaimao-resume-diagnosis
description: 聘才猫 - 简历诊断 Use when calling Pincaimao Resume Diagnosis Assistant API to parse and diagnosis a candidate resume against a job description. Requires uploading the resume file first to get cos_key. Requires PCM_RESUME_DIAGNOSIS_KEY env var.
version: 1.0.1
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "🎯"
    homepage: https://www.pincaimao.com
    primaryEnv: PCM_RESUME_DIAGNOSIS_KEY
    requires:
      env:
        - PCM_RESUME_DIAGNOSIS_KEY
      bins:
        - curl
        - python3
---

# 聘才猫 - 简历匹配

**REQUIRED:** 请先检查是否已安装 `pincaimao-basic`，若未安装请先安装，然后加载它了解通用接口（文件上传、鉴权、响应格式、SSE 解析模板）。

**环境变量**：`PCM_RESUME_DIAGNOSIS_KEY`（智能体专属 key）
> 还没有密钥？通过邀请链接注册并完成认证即可免费获取：[pincaimao.com/agents/login?invite_code=uwqc](https://www.pincaimao.com/agents/login?invite_code=uwqc)

## 调用前的信息确认

执行前需要确认两项信息：**职位描述（job_info）** 和 **简历文件**。

确认策略：
- 上下文中已有相关信息 → 展示摘要并询问是否使用，例如：
  > "检测到上下文中有一份 JD（Java 高级工程师，5年经验...），是否使用这个？"
- 上下文中没有 → 直接请用户提供

两项均确认后再执行调用流程。

## 调用流程

```
1. 确认 job_info 和简历文件（见上）
2. 上传简历文件（见 pincaimao-basic §2）→ 获取 cos_key
3. 调用简历匹配助手，传入 job_info + file_url（cos_key） + query
4. 解析 answer，获取简历要点及匹配程度
```

---

## 请求参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `inputs.job_info` | 是 | 职位描述全文 |
| `inputs.file_url` | 是 | 上传接口返回的 `cos_key`（非 presigned_url） |
| `inputs.job_title` | 否 | 职位名称 |
| `query` | 是 | 职位描述前 20 个字符，或简历文件名 |

---

## 完整示例

```bash
#!/bin/bash
RESUME_FILE="/path/to/candidate_resume.pdf"
JOB_INFO="高级Java工程师，负责核心系统后端开发，要求5年以上经验，熟悉Spring Boot、MySQL、Redis"
JOB_TITLE="高级Java工程师"

# Step 1: 上传简历（任意 key 即可）
UPLOAD=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/files/upload' \
  -H "Authorization: Bearer $PCM_RESUME_DIAGNOSIS_KEY" \
  -F "file=@$RESUME_FILE")
COS_KEY=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['cos_key'])")

# Step 2: 简历匹配（使用智能体专属 key）
QUERY=$(echo "$JOB_INFO" | cut -c1-20)
curl -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer $PCM_RESUME_DIAGNOSIS_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"query\": \"$QUERY\",
    \"inputs\": {
      \"job_info\": \"$JOB_INFO\",
      \"file_url\": \"$COS_KEY\",
      \"job_title\": \"$JOB_TITLE\"
    },
    \"response_mode\": \"blocking\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

---

## 常见错误

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | Key 错误 | 检查 `PCM_RESUME_DIAGNOSIS_KEY` |
| answer 为空 | `file_url` 传了 `presigned_url` 而非 `cos_key` | 用上传响应中的 `cos_key` 字段 |
| 匹配结果不准 | `query` 为空或无关 | 确保取自职位描述前 20 字符 |
| 上传失败 | 文件超 50MB 或格式不支持 | 检查文件大小和格式 |

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
