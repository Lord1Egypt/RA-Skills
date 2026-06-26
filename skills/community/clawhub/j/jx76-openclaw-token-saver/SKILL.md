---
name: openclaw-token-saver
description: OpenClaw Token 节省指南。提供5大类20+种减少Token消耗的方法，包括上下文瘦身、工具优化、缓存复用、模型控制和本地替代方案。当Token使用超过阈值时自动触发优化建议。
tags: ["openclaw", "token-optimization", "cost-saving", "performance", "chinese"]
triggers:
  - token_threshold: 0.8
  - token_budget_exceeded: true
  - context_compaction_needed: true
---

# OpenClaw Token 节省指南

降低 OpenClaw 使用成本的完整策略手册。

## 自动触发条件

当以下情况发生时，自动调用此 skill：

1. **Token 使用超过 80%** - 触发优化建议
2. **单次请求超过 4000 tokens** - 建议压缩上下文
3. **上下文接近上限** - 自动提示清理方案
4. **连续 10 轮对话** - 建议压缩或重置

## 自动响应逻辑

```
IF token_usage > 80%:
    → 显示警告 + 提供压缩选项
    → 建议使用 /compact
    → 推荐切换到 /nc 模式

IF token_per_turn > 4000:
    → 提示精简输入
    → 建议分批处理
    → 启用工具返回限制

IF context_window > 90%:
    → 强制建议清理
    → 提供 /reset 选项
    → 显示当前 Token 统计
```

## 一、上下文瘦身

### 1. 手动压缩
- 对话中发送 `/compact`
- 自动将长历史转为摘要

### 2. 滑动窗口
```json
{
  "max_history_messages": 10
}
```
只保留最近 N 条消息

### 3. 分层上下文切换
| 命令 | 作用 |
|------|------|
| `/nc` | 仅当前+系统提示 |
| `/cc` | 最近10条 |
| `/fc` | 全量上下文 |

### 4. 重置/新建
- `/reset` - 清空当前会话，保留记忆
- `/new` - 开启全新对话

### 5. 自动压缩
安装 `claw-compact`：
```bash
clawhub install claw-compact
```
满15轮或5000 token自动压缩

---

## 二、工具与提示词优化

### 6. 禁用无用工具
只开启必要工具：
```json
{
  "tools": {
    "enabled": ["read", "write", "exec"]
  }
}
```
系统提示词可从 3500 → 800 token

### 7. 精简 Skill 描述
- 技能 YAML frontmatter 保持简洁
- 描述控制在 100 字以内

### 8. 限制工具返回
强制工具返回摘要：
```json
{
  "web_search": {
    "max_results": 3,
    "max_chars": 500
  }
}
```

### 9. 精简系统提示
```json
{
  "bootstrapMaxChars": 2000
}
```

---

## 三、缓存与复用

### 10. 开启模型缓存
利用 Anthropic 提示缓存：
```json
{
  "model": "claude-3-sonnet",
  "enable_prompt_caching": true
}
```

### 11. 心跳保活
缓存 TTL 1h 时，设置 55min 心跳：
```json
{
  "heartbeat": {
    "interval_minutes": 55
  }
}
```

### 12. 本地检索替代
安装 `qmd` 本地索引：
```bash
clawhub install qmd
```
只取需要的段落，节省 80%+

### 13. 搜索优化
使用 `exa-search`：
```bash
clawhub install exa-search
```
过滤广告/HTML，返回纯文本，省 70%+

---

## 四、模型与调用控制

### 14. 模型分层
| 任务类型 | 推荐模型 |
|---------|---------|
| 简单计算/查天气 | GPT-3.5 / Haiku |
| 代码生成 | GPT-4 / Sonnet |
| 复杂推理 | GPT-4o / Opus |

### 15. 关闭重试/兜底
```json
{
  "max_retries": 0,
  "enable_fallback": false
}
```

### 16. 限制迭代次数
```json
{
  "max_iterations": 10
}
```

### 17. Token 预算
```json
{
  "token_budget": {
    "per_turn": 4000,
    "per_session": 50000
  }
}
```

---

## 五、本地替代

### 18. 本地部署模型
使用 Ollama：
```bash
ollama run qwen2.5:14b
```

配置 OpenClaw 连接本地：
```json
{
  "model": {
    "provider": "ollama",
    "base_url": "http://localhost:11434"
  }
}
```
Token 费用为 0

### 19. 本地代理转发
Node.js 协议转换：
```javascript
// 走网页版 AI，不耗官方 Token
```

### 20. 批量处理
将多个小任务合并为一次请求：
```
❌ 10次单独请求
✅ 1次批量处理
```

---

## 快速检查清单

- [ ] 配置 `max_history_messages: 10`
- [ ] 禁用不需要的 tools
- [ ] 安装 `claw-compact`
- [ ] 设置 Token 预算
- [ ] 使用 `/compact` 定期压缩
- [ ] 考虑本地模型替代

---

## 参考配置

```json
{
  "context": {
    "max_history_messages": 10,
    "auto_compact": true
  },
  "tools": {
    "enabled": ["read", "write", "exec", "web_search"]
  },
  "model": {
    "default": "gpt-3.5-turbo",
    "complex_tasks": "gpt-4"
  },
  "limits": {
    "max_retries": 0,
    "max_iterations": 10,
    "token_budget_per_session": 50000
  }
}
```

---

**预计节省: 50-90% Token 消耗**
