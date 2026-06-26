---
name: pengleni-login-session-html-bridge
description: "Use when users need SMS code login, session creation, and HTML message exchange via /session/login and /session/message."
---

# SKILL: Pengleni Login Session HTML Bridge

## 0. Quick Checklist For Agent

在真正发请求前，先逐项确认：

1. `CLAWHUB_SKILL_TOKEN` 已配置。
2. 用户已提供合法手机号。
3. 如果要发消息，已拿到 `user_id` 和 `session_id`。
4. 默认设置 `stream=true`。
5. 用户输入包含 HTML 时，先做安全过滤。

## 1. Skill Purpose

当用户需要通过手机号验证码建立会话，并提交 HTML 内容获取智能体回复时，使用本 Skill。

适用意图关键词：

- 验证码登录
- 创建会话
- HTML 消息问答
- 多轮会话延续

## 2. Runtime Config

Agent 在调用前必须确认以下环境变量：

```env
SITE_BASE_URL=https://www.zhibianai.com
API_BASE_URL=https://www.zhibianai.com/api/v1/clawhub
CLAWHUB_SKILL_TOKEN=your_service_token
```

默认请求头：

```http
Authorization: Bearer ${CLAWHUB_SKILL_TOKEN}
Content-Type: application/json
```

## 3. API Contract

### 3.1 Send Verification Code

- Method: `POST`
- URL: `${SITE_BASE_URL}/chainlit/send-verification-code`
- Note: 站点级接口，不在 `${API_BASE_URL}` 下

Request:

```json
{
  "phone": "13800138000"
}
```

Validation:

- `phone` 必须匹配 `^[0-9]{11}$`

### 3.2 Login Session

- Method: `POST`
- URL: `${API_BASE_URL}/session/login`

Request:

```json
{
  "phone": "13800138000",
  "verify_code": "123456",
  "session_id": "optional-session-id"
}
```

Request Rules:

- `phone` required
- `verify_code` required
- `session_id` optional，用于延续已有会话

Success Response:

```json
{
  "request_id": "req_xxx",
  "user_id": "user_xxx",
  "session_id": "sess_xxx",
  "expires_in": 1800,
  "is_new_user": false
}
```

Error Mapping:

- `401`: token 无效或验证码失败
- `429`: 限流
- `500`: 服务异常

### 3.3 Send HTML Message

- Method: `POST`
- URL: `${API_BASE_URL}/session/message`

Request:

```json
{
  "user_id": "user_xxx",
  "session_id": "sess_xxx",
  "html_payload": "<p>你好，推荐一个通勤淡妆方案</p>",
  "stream": true,
  "metadata": {
    "source": "openclaw"
  }
}
```

Request Rules:

- `user_id` required
- `session_id` required
- `html_payload` required，最大 20000 字符
- `stream` optional，Agent 默认传 `true`
- `metadata` optional

Success Response:

```json
{
  "request_id": "req_xxx",
  "user_id": "user_xxx",
  "session_id": "sess_xxx",
  "answer_html": "<p>建议：底妆轻薄+暖调腮红</p>",
  "answer_text": "建议：底妆轻薄，搭配暖调腮红。",
  "finish_reason": "stop",
  "latency_ms": 620
}
```

Error Mapping:

- `400`: 参数不合法或 HTML 不合法
- `401`: 会话失效或鉴权失败
- `429`: 限流
- `504`: 上游超时
- `500`: 服务异常

## 4. Agent Execution Flow

按以下顺序执行，除非用户明确要求跳过某一步：

1. 调用验证码接口发送验证码。
2. 收集用户验证码后调用登录接口。
3. 从登录响应读取 `user_id` 和 `session_id`。
4. 调用消息接口发送 `html_payload`。
5. 优先返回 `answer_text`，若用户需要富文本则返回 `answer_html`。

## 5. Agent Behavior Rules

- 如果用户未提供 `session_id`，允许服务端创建。
- 如果登录后返回新 `session_id`，后续请求必须使用新值。
- 默认流式：Agent 默认 `stream=true`。
- 发生 `401` 时，优先提示重新登录，不要盲目重试消息接口。
- 发生 `429` 或 `504` 时，最多重试 2 次，退避 500ms。

## 6. Security Constraints

- 输入 HTML 需要白名单策略。
- 禁止 `script`、`style`、`iframe`、`object`、`embed`、`form`、`input` 标签。
- 应校验 `user_id` 与 `session_id` 的绑定关系。

## 7. Minimal Error Handling Template

当接口失败时，Agent 返回格式建议：

```text
调用阶段: <send_code|login|message>
HTTP状态: <status_code>
错误原因: <mapped_reason>
建议动作: <retry|relogin|check_input>
```

## 8. Local Debug Commands

```bash
python send_code_client.py --phone 13800138000
python login_client.py --phone 13800138000 --verify-code 123456
python chat_client.py --text "你好，帮我推荐一个通勤淡妆"
python chat_client.py --multi-turn
```