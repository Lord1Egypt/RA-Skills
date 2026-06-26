---
name: openclaw-cost-optimization
version: 1.0.1
description: OpenClaw 成本优化 - 降低 AI API 支出技巧。适合：成本敏感用户、企业部署。
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: []
---

# OpenClaw 成本优化指南

让你的 AI 助手更省钱。

## 模型成本对比

| 模型 | 输入价格 | 输出价格 | 适用场景 |
|------|----------|----------|----------|
| DeepSeek V3 | ¥1/百万 | ¥2/百万 | 日常对话（推荐） |
| GLM-4 | ¥10/百万 | ¥10/百万 | 国产合规 |
| Claude 3.5 Sonnet | $3/百万 | $15/百万 | 编程任务 |
| GPT-4o | $2.5/百万 | $10/百万 | 多模态 |
| GPT-4o-mini | $0.15/百万 | $0.6/百万 | 简单任务 |

**省钱技巧**：日常使用 DeepSeek，编程用 Claude，简单任务用 mini 版本。

## 配置优化

### 1. 选择便宜模型

```bash
# 默认使用 DeepSeek
openclaw config set model deepseek-chat
```

### 2. 设置缓存

```yaml
# ~/.openclaw/config.yaml
cache:
  enabled: true
  ttl: 3600  # 1小时
  max_size: 1000
```

### 3. 限制上下文长度

```yaml
context:
  max_tokens: 4000  # 限制上下文
  truncate_method: "middle"  # 保留首尾
```

### 4. 批量处理

```yaml
batch:
  enabled: true
  size: 10  # 每 10 条消息批量处理
```

## 使用技巧

### 技巧 1：分层使用模型

```yaml
models:
  simple: "gpt-4o-mini"      # 简单问答
  normal: "deepseek-chat"    # 日常对话
  complex: "claude-sonnet"   # 复杂任务
```

### 技巧 2：预热缓存

对常见问题预设回复，避免重复调用 API。

### 技巧 3：限制对话轮次

```yaml
conversation:
  max_turns: 20  # 超过 20 轮自动总结
```

### 技巧 4：使用流式输出

```yaml
stream: true  # 减少等待时间，提升体验
```

## 成本监控

### 查看用量

```bash
# 查看本月用量
openclaw stats usage

# 查看各模型消耗
openclaw stats models
```

### 设置预算

```yaml
budget:
  daily: 10    # 每天最多 ¥10
  monthly: 200 # 每月最多 ¥200
  alert: 0.8   # 达到 80% 时提醒
```

### 超预算处理

```yaml
budget:
  exceed_action: "fallback"  # 或 "stop"
  fallback_model: "gpt-4o-mini"
```

## 成本估算

### 个人用户

- 日均 100 条消息
- 每条约 500 tokens
- DeepSeek：约 ¥0.1/天 = ¥3/月

### 小团队（10人）

- 日均 500 条消息
- DeepSeek：约 ¥0.5/天 = ¥15/月

### 企业（100人）

- 日均 5000 条消息
- DeepSeek：约 ¥5/天 = ¥150/月

## 常见问题

### Q: 如何查看实时费用？

```bash
openclaw cost today
openclaw cost this-month
```

### Q: DeepSeek 和 Claude 差多少？

同样 100 万 tokens：
- DeepSeek：¥3
- Claude：¥108
- **差 36 倍**

### Q: 如何切换模型？

```bash
# 临时切换
openclaw ask "问题" --model claude-sonnet

# 永久切换
openclaw config set model deepseek-chat
```

## 需要帮助？

- 成本诊断：¥99
- 优化方案：¥299
- 企业咨询：¥999

联系：微信 yang1002378395 或 Telegram @yangster151
