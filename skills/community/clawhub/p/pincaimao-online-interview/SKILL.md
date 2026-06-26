---
name: pincaimao-online-interview
description: 聘才猫 - 在线面试 Use when calling Pincaimao Online Interview API to conduct a multi-turn AI interview session. Supports text and video interview modes, custom question lists, and report callbacks. Requires PCM_ONLINE_INTERVIEW_KEY env var.
version: 1.0.1
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "🎥"
    homepage: https://www.pincaimao.com
    primaryEnv: PCM_ONLINE_INTERVIEW_KEY
    requires:
      env:
        - PCM_ONLINE_INTERVIEW_KEY
      bins:
        - curl
        - python3
---

# 聘才猫 - 在线面试

**REQUIRED:** 请先检查是否已安装 `pincaimao-basic`，若未安装请先安装，然后加载它了解通用接口（文件上传、鉴权、响应格式、SSE 解析模板）。

**环境变量**：`PCM_ONLINE_INTERVIEW_KEY`（智能体专属 key）
> 还没有密钥？通过邀请链接注册并完成认证即可免费获取：[pincaimao.com/agents/login?invite_code=uwqc](https://www.pincaimao.com/agents/login?invite_code=uwqc)

## 调用前的信息确认

执行前需要确认：**职位描述（job_info）** 和 **简历文件**。

确认策略：
- 上下文中已有相关信息 → 展示摘要并询问是否使用
- 上下文中没有 → 直接请用户提供

同时可询问：
- 面试题总数（`question_number`，默认 5）
- 是否使用自定义题目（`question_list`）
- 是否视频面试（需要 `video_url`）
- 报告回调地址（`url_callback`）

## 多轮对话说明

在线面试是多轮对话，**必须使用 `conversation_id` 保持上下文**：
- 第一轮：不传 `conversation_id`，从响应中保存返回的 `conversation_id`
- 后续轮次：每次都传入同一个 `conversation_id`
- `query` 第一次传 job_info 前 20 字符，后续传用户回答内容（视频面试传视频转写文字）

## 请求参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `inputs.job_info` | 是 | 职位描述全文 |
| `inputs.file_url` | 否 | 简历文件 cos_key |
| `inputs.file_name` | 否 | 简历文件名 |
| `inputs.resume_content` | 否 | 简历文本，JSON 字符串或纯文本，AI 自动解析 |
| `inputs.job_title` | 否 | 职位名称 |
| `inputs.video_url` | 否 | 视频文件 cos_key 或公网地址，视频面试每轮都需传 |
| `inputs.question_number` | 否 | 面试题总数，默认 5，字符串类型 |
| `inputs.question_list` | 否 | 自定义题目，JSON 字符串数组，如 `"[\"问题1\",\"问题2\"]"` |
| `inputs.url_callback` | 否 | 报告生成后的回调 URL（POST，返回 base64 编码报告） |
| `query` | 是 | 第一轮：job_info 前 20 字符；后续：用户回答 |
| `conversation_id` | 第二轮起必填 | 保持多轮对话上下文 |

## 完整示例

```bash
#!/bin/bash
JOB_INFO="高级销售专员 / 销售主管，行业领先平台，完善晋升通道"
JOB_TITLE="高级销售专员"
RESUME_FILE="/path/to/resume.docx"

# Step 1: 上传简历（可选）
UPLOAD=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/files/upload' \
  -H "Authorization: Bearer $PCM_ONLINE_INTERVIEW_KEY" \
  -F "file=@$RESUME_FILE")
COS_KEY=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['cos_key'])")
FILE_NAME=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['filename'])")

# Step 2: 第一轮 - 开始面试
QUERY=$(echo "$JOB_INFO" | cut -c1-20)
ROUND1=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer $PCM_ONLINE_INTERVIEW_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"query\": \"$QUERY\",
    \"inputs\": {
      \"job_info\": \"$JOB_INFO\",
      \"job_title\": \"$JOB_TITLE\",
      \"file_url\": \"$COS_KEY\",
      \"file_name\": \"$FILE_NAME\",
      \"question_number\": \"5\"
    },
    \"response_mode\": \"blocking\"
  }")

# 保存 conversation_id 用于后续轮次
CONV_ID=$(echo "$ROUND1" | python3 -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")
echo "面试官：$(echo "$ROUND1" | python3 -c "import sys,json; print(json.load(sys.stdin)['answer'])")"

# Step 3: 后续轮次 - 提交回答
USER_ANSWER="我有5年销售经验，擅长大客户开拓..."
curl -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer $PCM_ONLINE_INTERVIEW_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"query\": \"$USER_ANSWER\",
    \"inputs\": {},
    \"conversation_id\": \"$CONV_ID\",
    \"response_mode\": \"blocking\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

## 任务结束检测

面试结束时，streaming 模式下会收到：
```
node_finished 且 data.title 包含"聘才猫任务结束"
```
此时停止轮询，面试报告将通过 `url_callback` 回调（如已配置）。

## 常见错误

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | Key 错误 | 检查 `PCM_ONLINE_INTERVIEW_KEY` |
| 第二轮面试官不记得上文 | 未传 `conversation_id` | 每轮必须传第一轮返回的 `conversation_id` |
| `question_number` 无效 | 传了数字类型 | 此字段需传**字符串**，如 `"5"` |
| 回调未收到报告 | 面试未正常结束 | 检查是否收到任务结束事件 |

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
