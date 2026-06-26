# 自动触发机制 · Auto-Trigger

---

## 触发条件

| 条件 | 阈值 | 动作 |
|------|------|------|
| 上下文超过 70% | 143.5k/205k | 提示压缩（不强制） |
| 上下文超过 80% | 164k/205k | 强烈建议压缩 |
| 上下文超过 90% | 184.5k/205k | 强制压缩提示 |
| 上下文超过 95% | 194.75k/205k | 阻止继续写入 |

---

## 自动触发流程

```
每次回答前检查：
    │
    ├─ context < 60% → 不提示，继续
    │
    ├─ 60% ≤ context < 70% → 静默，继续
    │
    ├─ 70% ≤ context < 80% → 提示：
    │   "[🦅 Context: 72%] 建议压缩，输入 /compress"
    │
    ├─ 80% ≤ context < 90% → 强烈建议：
    │   "[🦅⚠️ Context: 84%] 上下文较满，请压缩 /compress"
    │
    └─ context ≥ 90% → 强制提示，阻止非必要写入：
        "[🦅🚨 Context: 93%] 必须压缩后才能继续"
```

---

## 每 N 轮自动检查

每完成 10 轮对话，自动检查上下文水位：

```
Round 10: 检查 → 68% → 正常
Round 20: 检查 → 73% → 提示
Round 30: 检查 → 81% → 强烈建议
Round 40: 检查 → 89% → 必须压缩
```

---

## 用户触发词（自然语言）

以下任何一句自动触发压缩：

```
压缩上下文
上下文太长了
压缩对话
reduce context
context too big
上下文爆了
瘦身
compress
context满
token太多了
上下文太多了
```

---

## 压缩确认流程

触发后，必须确认才执行：

```
[🦅 Context Compressor]

检测到上下文 72% (148k tokens)
建议压缩策略：normal（摘要+保留最近10轮）

效果预估：
  原始：148,000 tokens
  压缩后：约 35,000 tokens
  压缩比：约 4.2x
  保留消息：最近 10 轮完整 + 历史摘要

选项：
  [1] 执行 normal 压缩
  [2] 轻度压缩（保留更多）
  [3] 重度压缩（最小化）
  [4] 取消
```

---

## 压缩后自动写入

压缩完成后：

1. 将压缩结果写入 `memory/today.md`（历史记录）
2. 将压缩后的干净上下文替换当前对话
3. 向用户报告压缩结果：

```
✅ 压缩完成

  原始：148,000 tokens (72%)
  压缩后：35,000 tokens (17%)
  压缩比：4.2x
  节省：113,000 tokens

  可继续对话约 48 小时
```

---

## 配置项

```json
{
  "auto_trigger_enabled": true,
  "auto_trigger_threshold": 70,
  "check_interval_rounds": 10,
  "default_strategy": "normal",
  "keep_recent_normal": 10,
  "keep_recent_heavy": 5,
  "keep_recent_emergency": 3,
  "preserve_system_prompt": true
}
```
