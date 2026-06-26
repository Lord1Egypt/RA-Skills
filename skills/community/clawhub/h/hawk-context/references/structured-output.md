# 结构化输出 · Structured Output

---

## JSON 输出格式

每次压缩后输出结构化 JSON：

```json
{
  "status": "success",
  "compressed_prompt": "...",
  "stats": {
    "original_tokens": 148000,
    "compressed_tokens": 35000,
    "ratio": "4.2x",
    "kept_messages": 10,
    "summarized_count": 87,
    "dropped_count": 12,
    "system_prompt_tokens": 500
  },
  "compression": {
    "level": "normal",
    "strategy": "summarize + merge + collapse",
    "keep_recent": 10
  },
  "timestamp": "2026-03-29T00:39:00+08:00",
  "messages": [
    {
      "role": "system",
      "content": "[永久保留的系统提示]",
      "status": "preserved"
    },
    {
      "role": "user",
      "content": "[最新问题完整原文]",
      "status": "preserved"
    },
    {
      "role": "assistant",
      "content": "[最新回答完整原文]",
      "status": "preserved"
    },
    {
      "role": "user",
      "content": "[历史消息摘要]",
      "original_count": 45,
      "status": "summarized"
    },
    {
      "role": "user",
      "content": "[代码折叠]",
      "original_lines": 120,
      "status": "collapsed"
    }
  ],
  "warnings": [],
  "next_check": "约48小时后或每10轮检查"
}
```

---

## 错误输出

```json
{
  "status": "error",
  "error": "context_too_small",
  "message": "上下文未达到压缩阈值（当前 45%，建议 >60%）",
  "current_tokens": 92250,
  "threshold": 123000,
  "suggestion": "当前上下文充足，无需压缩"
}
```

---

## 状态报告（每次回答后）

当 `hawk_alert` 开启时，每次回答附带：

```
[🦅 Context: 72%] 压缩建议: /compress
  原始: 148k | 压缩后: ~35k | 节省: 113k
```

---

## 压缩历史记录

每次压缩写入 `memory/today.md`：

```markdown
## 2026-03-29 压缩记录

### 00:39 压缩（normal）
- 原始: 148,000 tokens (72%)
- 压缩后: 35,000 tokens (17%)
- 压缩比: 4.2x
- 保留: 最近10轮 + 历史摘要
- 节省: 113,000 tokens
```

---

## 与 Context Hawk Memory 的关系

```
Context Compressor（压缩当前对话）
    ↓ 写入
memory/today.md（历史压缩记录）
    ↓
Context Hawk Memory（持久记忆管理）
    ↓
memory-lancedb-pro（向量检索）
```

两者协同工作：
- **Context Compressor** = 现在时（压缩当前）
- **Context Hawk Memory** = 过去时（管理历史）
