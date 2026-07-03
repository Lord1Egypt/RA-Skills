# model-fallback-retry

> 大模型 API 异常自动重试 + 多渠道消息回传队列管理

当 AI 模型调用遇到限速（429）、配额耗尽（2056）、服务过载（503）等异常时，自动将消息加入重试队列，通过定时任务自动重新发送，确保**零消息丢失**。

---

## 解决的问题

使用 OpenClaw 时，你是否遇到过：

- ❌ 消息发出去，AI 返回"已达到用量上限"或"429 Rate Limit"，消息就这样丢了
- ❌ API 临时限速，需要手动重发
- ❌ 配额耗尽后整个 agent 卡住
- ❌ 凌晨异常，醒来发现一整晚的消息都没响应

**model-fallback-retry** 就是来解决这些问题的。

---

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Plugin (index.mjs) - 常驻内存                              │
│                                                             │
│  三层异常检测：                                            │
│  Layer 1: errorCategory 拦截（rate_limit_error/quota_exhausted）│
│  Layer 2: HTTP Status Code 拦截（429/402/503）             │
│  Layer 3: 文本正则兜底（quota_error_patterns）              │
│                                                             │
│  命中任一层 → 写入 retry_queue.json (pending)             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Cron 定时任务（每 30 分钟）                               │
│                                                             │
│  检查 retry_queue.json 中到期的 pending 消息               │
│  → sessions_send 发 [RETRY:id=xxx] 原始消息               │
│  → increment_retry() 指数退避计算下次重试时间              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Agent 收到 RETRY 消息                                     │
│                                                             │
│  [RETRY:id=xxx] 用户原始消息                               │
│  → mark_completed(xxx) → 从 pending 移到 completed        │
│  → 用原始消息重新触发 AI 处理                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 异常检测规则

### 三层拦截机制

| 层级 | 触发条件 | 说明 |
|------|---------|------|
| **Layer 1** | `model_call_ended` + `errorCategory` | OpenClaw 结构化字段，最可靠 |
| **Layer 2** | `model_call_ended` + `httpStatus` | HTTP 状态码（429/402/503） |
| **Layer 3** | `agent_end` + 文本正则匹配 | 兜底，支持自定义 patterns |

### 支持的 errorCategory

| errorCategory | 含义 | 建议重试策略 |
|--------------|------|------------|
| `rate_limit_error` | TPM/RPM 限速 | 短间隔重试 |
| `quota_exhausted` | 配额耗尽 | 长间隔重试 |
| `overloaded_error` | 服务过载 | 短间隔重试 |
| `billing` | 余额不足 | 不重试，只通知 |

### 支持的 HTTP Status Code

| Status | 含义 |
|--------|------|
| 429 | Rate Limit（限速） |
| 402 | Payment Required（配额耗尽） |
| 503 | Service Unavailable（服务过载） |

### 文本正则 patterns

当前默认 patterns：

```json
"quota_error_patterns": [
  "Something went wrong while processing your request",
  "已达到 Token Plan 用量上限.*\\([0-9]+\\)",
  "Token Plan.*用量上限"
]
```

**支持自定义**：在 `config.json` 中添加更多正则表达式。

---

## 配置 (config.json)

| 配置项 | 说明 | 默认值 |
|-------|------|-------|
| `retry_interval_minutes` | 重试检查间隔（分钟） | 30 |
| `initial_wait_minutes` | 首次重试等待时间 | 30 |
| `max_retry_count` | 最大重试次数 | 5 |
| `intercept_on_error_categories` | 拦截的 errorCategory 列表 | `["rate_limit_error", "quota_exhausted"]` |
| `intercept_on_status_codes` | 拦截的 HTTP 状态码 | `[429, 402, 503]` |
| `quota_error_patterns` | 文本正则匹配 patterns | 见上方 |
| `clear_command` | 清空指令 | `#清空` |
| `status_command` | 状态查询指令 | `#队列状态` |

### 指数退避策略

首次失败 → 等待 `initial_wait_minutes`
第2次 → `initial_wait_minutes * 2`
第3次 → `initial_wait_minutes * 4`
...以此类推

例如 `initial_wait_minutes = 30`：

| 重试次数 | 等待时间 |
|---------|---------|
| 第1次 | 30 分钟 |
| 第2次 | 60 分钟 |
| 第3次 | 120 分钟 |
| 第4次 | 240 分钟 |
| 第5次 | 480 分钟 |

---

## 队列格式 (retry_queue.json)

```json
{
  "pending": [{
    "id": "uuid",
    "sessionKey": "agent:dd:feishu:direct:ou_xxx",
    "originalMessage": "用户发送的原始消息",
    "errorOutput": "AI 返回的错误信息",
    "errorType": "quota_error",
    "sent_at": "2026-06-19T12:00:00Z",
    "retry_count": 0,
    "next_retry_at": "2026-06-19T12:30:00Z",
    "max_retry_count": 5,
    "initial_wait_minutes": 30
  }],
  "completed": [],
  "cleared": []
}
```

---

## 用户指令

- `#清空` - 清空当前用户所有待重试消息
- `#队列状态` - 查看当前排队数量
- `#清空 消息ID` - 清空指定某一条

---

## RETRY 消息格式

当 Cron 定时任务检测到需要重试的消息时，会通过 `sessions_send` 发送：

```
[RETRY:id=abc-123] 用户原始消息内容
```

Agent 收到后：
1. 解析 `msg_id = abc-123`
2. 调用 `mark_completed(abc-123)` 从 pending 移到 completed
3. 用原始消息内容重新触发 AI 处理

---

## 安装

```bash
# 1. 安装 Skill 到 ~/.openclaw/skills/
cp -r model-fallback-retry ~/.openclaw/skills/

# 2. 重启 Gateway（让 Plugin 加载）
openclaw gateway restart

# 3. 配置 Cron 定时任务（使用 config.json 中的 cron 配置）
openclaw cron add \
  --name "model-fallback-retry-check" \
  --every 30m \
  --agent xiaoxiao \
  --to ou_50977b3a4ee416e61d71483e77bf3d09

# 4. 验证 Cron 是否配置成功
openclaw cron list
```

### 安装后必读

**config.json 中的 `cron` 配置项需要根据你的实际情况修改**：

| 配置项 | 说明 | 你的值 |
|-------|------|-------|
| `cron.agent` | 执行重试的 Agent 名称 | `xiaoxiao`（默认） |
| `cron.notify_to` | 失败通知的飞书/微信 ID | 需修改为你的 ID |
| `cron.interval_minutes` | 检查间隔 | `30`（默认） |

修改方法：编辑 `~/.openclaw/skills/model-fallback-retry/config.json` 中的 `cron.notify_to` 为你的飞书/微信 ID。

**注意**：重试消息本身是动态发送到原始 session 的（不依赖此配置），此配置仅用于：
1. 指定哪个 Agent 执行重试检查
2. 失败通知发到哪里

## 版本

当前版本：**1.0.0**

---

## Changelog

### 1.0.0
- 初始版本
- 支持三层异常检测（errorCategory / HTTP Status / 文本正则）
- 支持指数退避重试策略
- 支持多渠道（Feishu/WeChat 等）
