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

## 特性

- ✅ **三层异常检测**：errorCategory / HTTP Status / 文本正则兜底
- ✅ **指数退避重试**：智能间隔，避免频繁触发限速
- ✅ **多租户支持**：自动识别用户，无需手动配置
- ✅ **零配置安装**：复制 + 重启即可运行
- ✅ **多渠道支持**：Feishu / WeChat / Telegram 等

---

## 架构

```
用户发消息
    ↓
OpenClaw 处理，调用 AI 模型
    ↓
Plugin 三层检测（任一命中即拦截）
    ├─ Layer 1: errorCategory（rate_limit_error / quota_exhausted）
    ├─ Layer 2: httpStatus（429 / 402 / 503）
    └─ Layer 3: 文本正则（quota_error_patterns）
    ↓
消息入队 → retry_queue.json
    ↓
Cron 定时检查（每 30 分钟）
    ↓
sessions_send 发 RETRY 到原始 session
    ↓
用户收到重试消息
```

---

## 安装

```bash
# 1. 复制 skill 到 OpenClaws plugins 目录
cp -r model-fallback-retry ~/.openclaw/plugins/

# 2. 重启 Gateway
openclaw gateway restart
```

安装后会自动：
- 检测你的 tenant_id
- 生成默认配置
- 创建 cron 定时任务

---

## 配置

编辑 `config.json`（自动生成，或参考 `config.json.example`）：

```json
{
  "version": "1.0.0",
  "log_level": "debug",
  "retry_interval_minutes": 30,
  "initial_wait_minutes": 30,
  "max_retry_count": 5,
  "quota_error_patterns": [
    "Something went wrong while processing your request",
    "已达到 Token Plan 用量上限.*\\([0-9]+\\)"
  ],
  "intercept_on_error_categories": ["rate_limit_error", "quota_exhausted"],
  "intercept_on_status_codes": [429, 402, 503]
}
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|-------|------|-------|
| `retry_interval_minutes` | 检查间隔（分钟） | 30 |
| `initial_wait_minutes` | 首次等待时间 | 30 |
| `max_retry_count` | 最大重试次数 | 5 |
| `intercept_on_error_categories` | 拦截的 errorCategory | `["rate_limit_error", "quota_exhausted"]` |
| `intercept_on_status_codes` | 拦截的 HTTP 状态码 | `[429, 402, 503]` |
| `quota_error_patterns` | 文本正则 patterns | 见上方 |
| `log_level` | 日志级别 | `debug` |

---

## 用户指令

- `#清空` - 清空所有待重试消息
- `#队列状态` - 查看当前排队数量
- `#调试开` - 开启 debug 日志
- `#调试关` - 关闭 debug 日志

---

## 指数退避策略

```
第0次失败 → 等 initial_wait_minutes（默认 30 分钟）
第1次失败 → 等 60 分钟
第2次失败 → 等 120 分钟
第3次失败 → 等 240 分钟
第4次失败 → 等 480 分钟
第5次失败 → 标记 FAILED，不再重试
```

---

## 许可证

MIT
