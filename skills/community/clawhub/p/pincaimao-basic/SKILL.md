---
name: pincaimao-basic
description: 聘才猫平台基础能力 Use when calling any Pincaimao platform API — file upload, presigned URL, conversation list, message history, audio-to-text, resume JSON upload, or the base chat-messages interface. Reference this skill before building any PCM agent skill.
version: 1.0.2
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "🏗️"
    homepage: https://www.pincaimao.com
    requires:
      env:
        - PCM_ANY_KEY  # General-purpose key for non-chat endpoints. Agent-specific keys (e.g. PCM_JD_ASSISTANT_KEY) are declared in each agent skill.
      bins:
        - curl
        - python3
---

# 聘才猫平台基础能力

所有聘才猫智能体 skill 共用的底层接口。具体智能体（JD 助手、简历匹配等）的 `inputs` 参数见各自的 skill，通用部分统一在此。

---

## 鉴权

| 接口 | Key 要求 |
|------|----------|
| `chat-messages` | 必须使用**该智能体专属** key，不同智能体 key 不能混用 |
| 其他所有接口 | 任意创建的 key 均可 |

> 还没有密钥？通过邀请链接注册并完成认证即可免费获取：[pincaimao.com/agents/login?invite_code=uwqc](https://www.pincaimao.com/agents/login?invite_code=uwqc)

```bash
# chat-messages 示例（key 由各智能体 skill 的 primaryEnv 声明，如 PCM_JD_ASSISTANT_KEY）
-H "Authorization: Bearer <agent-specific-key>"

# 其他接口示例
-H "Authorization: Bearer $PCM_ANY_KEY"   # 任意 key 即可
```

---

## 1. chat-messages（智能体对话）

**POST** `https://api.pincaimao.com/agents/v1/chat/chat-messages`

### 请求体

```json
{
  "query": "...",
  "inputs": {},
  "response_mode": "blocking",
  "conversation_id": null,
  "user": null
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `query` | 是 | 依智能体而定 |
| `inputs` | 否 | 各智能体自定义参数 |
| `response_mode` | 否 | `"blocking"` 或 `"streaming"`，默认 streaming |
| `conversation_id` | 否 | 多轮对话时传入，保持上下文 |
| `user` | 否 | 业务侧用户 ID |

### Blocking 响应

```json
{
  "event": "message",
  "message_id": "...",
  "conversation_id": "...",
  "answer": "AI 回复内容",
  "metadata": { "usage": { "total_tokens": 953 } }
}
```

取结果：`.answer`

### Streaming 响应（SSE）

每行以 `data: ` 开头，包含 JSON 对象：

| 事件 | 说明 | 关键字段 |
|------|------|----------|
| `message_start` | 开始生成 | `conversation_id`, `message_id` |
| `message` / `agent_message` | 内容片段 | `answer`（需拼接） |
| `node_finished` | 节点完成 | `data.inputs.LLMText`（完整文本）, `data.title` |
| `message_end` | 生成结束 | — |

**特殊**：`node_finished` 且 `data.title` 含"聘才猫任务结束"→ 任务完成。

### Streaming 解析模板

```bash
curl -N -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer <agent-specific-key>" \
  -H 'Accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{"query":"...","inputs":{},"response_mode":"streaming"}' \
| python3 -c "
import sys, json
answer = ''
for line in sys.stdin:
    line = line.strip()
    if not line.startswith('data: '):
        continue
    try:
        d = json.loads(line[6:])
        event = d.get('event', '')
        if event in ('message', 'agent_message'):
            answer += d.get('answer', '')
        elif event == 'message_end':
            break
    except json.JSONDecodeError:
        pass
print(answer)
"
```

---

## 2. 文件上传

**POST** `https://api.pincaimao.com/agents/v1/files/upload`

```bash
curl -s -X POST 'https://api.pincaimao.com/agents/v1/files/upload' \
  -H "Authorization: Bearer $PCM_ANY_KEY" \
  -F "file=@/path/to/file.pdf"
```

响应：
```json
{
  "filename": "resume.docx",
  "ext": "docx",
  "cos_key": "/resources/file/20250711/abc123.docx",
  "presigned_url": "https://..."
}
```

**注意**：后续传给智能体的是 `cos_key`，不是 `presigned_url`。支持格式：xlsx、docx、pdf、txt、csv、jpg、png，最大 50MB。

---

## 3. 获取文件临时链接

**GET** `https://api.pincaimao.com/agents/v1/files/presigned-url`

```bash
curl -s "https://api.pincaimao.com/agents/v1/files/presigned-url?cos_key=/resources/file/xxx/abc.jpg" \
  -H "Authorization: Bearer $PCM_ANY_KEY"
```

响应包含 `file_url`（10 分钟有效）。可选参数 `expired`（秒，最长 30 天）。

---

## 4. 获取会话列表

**GET** `https://api.pincaimao.com/agents/v1/chat/conversations`

```bash
curl -s "https://api.pincaimao.com/agents/v1/chat/conversations?limit=20&user=user_001" \
  -H "Authorization: Bearer $PCM_ANY_KEY"
```

| 参数 | 说明 |
|------|------|
| `last_id` | 游标分页，上一页最后一条 ID |
| `user` | 按用户 ID 筛选 |
| `limit` | 每页条数，默认 20，最大 100 |

响应：`data.data[]` 含 `id`（conversation_id）、`name`、`inputs`、`created_at`。

---

## 5. 获取会话历史消息

**GET** `https://api.pincaimao.com/agents/v1/chat/messages`

```bash
curl -s "https://api.pincaimao.com/agents/v1/chat/messages?conversation_id=xxxx&limit=20" \
  -H "Authorization: Bearer $PCM_ANY_KEY"
```

倒序返回。参数 `first_id` 用于翻页。响应 `data.data[]` 含 `query`、`answer`、`inputs`、`created_at`。

---

## 6. 音视频转文字

**POST** `https://api.pincaimao.com/agents/v1/tts/audio_to_text`

```bash
curl -s -X POST 'https://api.pincaimao.com/agents/v1/tts/audio_to_text' \
  -H "Authorization: Bearer $PCM_ANY_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"cos_key": "/resources/file/xxx/audio.mp3"}'
```

响应：`data.text`（转写文字）。目前仅支持 cos_key 路径。

---

## 7. 简历 JSON 上传

**POST** `https://api.pincaimao.com/v1/files/resume-json`

将结构化简历数据上传，返回 cos_key 供后续智能体使用。

```bash
curl -s -X POST 'https://api.pincaimao.com/v1/files/resume-json' \
  -H "Authorization: Bearer $PCM_ANY_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "张三",
    "gender": "男",
    "age": "28",
    "degree": "本科",
    "work_year": "5",
    "city": "广州市",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "apply_job": "软件工程师",
    "education_objs": [...],
    "job_exp_objs": [...],
    "skills_objs": [{"skills_name": "Java", "skills_level": "精通"}]
  }'
```

响应：`data.cos_key`（供后续接口使用）。

<details>
<summary>简历 JSON 完整字段列表</summary>

**基本信息**：`name`, `gender`, `age`, `marital_status`, `birthday`, `race`, `hometown_address`, `nationality`, `polit_status`, `city`, `phone`, `email`, `qq`, `weixin`, `avatar_url`, `avatar_data`

**求职意向**：`apply_job`, `apply_cpy`, `work_year`, `work_position`, `work_company`, `work_status`, `work_salary`, `work_job_nature`

**学历**：`college`, `college_dept`, `major`, `degree`, `recruit`

**自述**：`cont_my_desc`, `cont_hobby`

**期望工作** (`expect_job_objs[]`)：`expect_job`, `expect_cpy`, `expect_salary`, `expect_industry`, `expect_time`, `expect_jnature`, `expect_jstatus`, `expect_jlocation`

**教育经历** (`education_objs[]`)：`start_date`, `end_date`, `edu_college`, `edu_college_dept`, `edu_major`, `edu_recruit`, `edu_degree`, `edu_content`

**工作经历** (`job_exp_objs[]`)：`start_date`, `end_date`, `job_cpy`, `job_position`, `job_dept`, `job_nature`, `job_salary`, `job_location`, `job_content`

**项目经历** (`proj_exp_objs[]`)：`start_date`, `end_date`, `proj_name`, `proj_cpy`, `proj_position`, `proj_content`, `proj_resp`

**培训经历** (`training_objs[]`)：`start_date`, `end_date`, `train_org`, `train_loc`, `train_name`, `train_cert`, `train_cont`

**技能** (`skills_objs[]`)：`skills_name`, `skills_level`（掌握/熟悉/擅长/精通）

**语言** (`lang_objs[]`)：`language_name`, `language_level`

**证书奖项** (`all_cert_objs[]`)：`cert_name`, `cert_type`（`certificate` 或 `award`）

</details>

---

## 常见错误

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | Key 错误或混用 | chat-messages 必须用智能体专属 key |
| 上传返回非 200 | 文件超 50MB 或格式不支持 | 检查文件大小和格式 |
| Streaming 无输出 | curl 缺 `-N` 标志 | 加 `-N` 禁用缓冲 |
| 临时链接失效 | presigned_url 超过 10 分钟 | 重新调用 presigned-url 接口 |

---

## External Endpoints

- `https://api.pincaimao.com` — Pincaimao platform API (chat, file upload, conversations)

## Security & Privacy

- API key is read from environment variable and passed via `Authorization` header; never hardcoded
- Resume files, job descriptions, and contract text are transmitted to `api.pincaimao.com` for AI processing
- Uploaded files are stored on Pincaimao's COS (Cloud Object Storage); returned `cos_key` paths should be treated as sensitive
- This skill does not store, log, or transmit data to any endpoint other than `api.pincaimao.com`
- Safe to invoke autonomously; all network calls are scoped to the authenticated user's API key
