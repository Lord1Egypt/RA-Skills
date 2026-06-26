---
name: pincaimao-jd-assistants
description: 聘才猫 - JD 助手 Use when calling Pincaimao JD Assistant API to generate job postings from job descriptions or generate structured job tags from job titles. Requires PCM_JD_ASSISTANT_KEY env var.
version: 1.0.1
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "📝"
    homepage: https://www.pincaimao.com
    primaryEnv: PCM_JD_ASSISTANT_KEY
    requires:
      env:
        - PCM_JD_ASSISTANT_KEY
      bins:
        - curl
        - python3
---

# 聘才猫 - JD 助手

**REQUIRED:** 请先检查是否已安装 `pincaimao-basic`，若未安装请先安装，然后加载它了解通用接口（文件上传、鉴权、响应格式、SSE 解析模板）。

**环境变量**：`PCM_JD_ASSISTANT_KEY`（智能体专属 key）
> 还没有密钥？通过邀请链接注册并完成认证即可免费获取：[pincaimao.com/agents/login?invite_code=uwqc](https://www.pincaimao.com/agents/login?invite_code=uwqc)

两个功能均调用同一 endpoint：`POST https://api.pincaimao.com/agents/v1/chat/chat-messages`

---

## 功能一：生成招聘 JD

```bash
RESULT=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer $PCM_JD_ASSISTANT_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "请帮我生成这个职位的招聘信息：",
    "inputs": {
      "job_info": "职位名称：Java高级工程师，薪资：20k-30k，福利：五险一金、年终奖，学历：本科，经验：5年以上，技能：Java、Spring Boot、MySQL、Redis"
    },
    "response_mode": "blocking"
  }')
echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['answer'])"
```

`job_info` 可包含：职位名称、薪资范围、福利待遇、学历要求、工作职责、任职资格、工作地点等。

---

## 功能二：生成职位标签

```bash
RESULT=$(curl -s -X POST 'https://api.pincaimao.com/agents/v1/chat/chat-messages' \
  -H "Authorization: Bearer $PCM_JD_ASSISTANT_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "请帮我生成职位标签",
    "inputs": {"job_title": "产品经理", "function_type": 1},
    "response_mode": "blocking"
  }')

# answer 是 JSON 字符串，需二次解析
echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
tags = json.loads(d['answer'])
for group in tags['tagGroup']:
    print(f\"{group['dimensionName']}: {group['defaultTags']}\")
"
```

`function_type` 固定为数字 `1`（不能是字符串 `"1"`）。

### 标签响应结构

```json
{
  "position": "产品经理",
  "tagGroup": [
    {
      "dimensionName": "专业技能",
      "defaultTags": ["需求分析", "原型设计"],
      "optionalTags": ["数据分析", "用户研究", "A/B测试"]
    },
    {
      "dimensionName": "月薪范围",
      "defaultTags": [],
      "optionalTags": ["12k-15k", "15k-20k", "20k以上"]
    }
  ]
}
```

---

## 常见错误

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | Key 未配置或使用了其他智能体的 key | 检查 `PCM_JD_ASSISTANT_KEY` |
| answer 为空 | `function_type` 传成了字符串 | 确保 `"function_type": 1`（数字） |
| 标签解析失败 | `answer` 是 JSON 字符串 | 对 `answer` 再执行 `json.loads()` |

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
