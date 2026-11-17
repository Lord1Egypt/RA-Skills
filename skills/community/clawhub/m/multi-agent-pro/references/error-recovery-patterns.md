# 错误恢复模式库

## 概述

本文档列出 5 种常见的错误场景及推荐恢复模式。

---

## 模式 1：临时性失败（网络抖动/API 限流）

**场景**：数据采集 Agent 调用外部 API 时遇到 429 限流或网络超时。

**恢复策略**：Level 1 重试

```json
{
  "id": "collector",
  "retry": 3,
  "timeout": 60,
  "fallback": "skip"
}
```

**操作**：
```bash
# 第1次失败
python error_recovery.py retry state.json collector "API 返回 429 限流"
# 引擎自动等待 2秒后重试

# 第2次失败
python error_recovery.py retry state.json collector "API 返回 429 限流"
# 引擎自动等待 4秒后重试

# 第3次失败（达到最大重试）
# 引擎自动进入 Level 2 降级
```

---

## 模式 2：数据缺失（下游可容错）

**场景**：采集 Agent 失败，但分析 Agent 可以在无数据情况下输出"数据不足"报告。

**恢复策略**：Level 2 降级 - skip

```json
{
  "id": "collector",
  "retry": 2,
  "fallback": "skip"
}
```

**效果**：collector 被跳过，analyzer 收到 `{"skipped": true}`，自行判断是否继续。

---

## 模式 3：部分成功（使用默认值）

**场景**：清洗 Agent 部分数据格式异常，但可以输出默认清洗结果。

**恢复策略**：Level 2 降级 - default

```json
{
  "id": "cleaner",
  "retry": 1,
  "fallback": "default",
  "default_value": {"cleaned_data": "使用原始数据，未做清洗"}
}
```

**效果**：cleaner 失败后，使用 `default_value` 作为输出，下游 analyzer 照常执行。

---

## 模式 4：关键节点失败（必须中止）

**场景**：报告生成 Agent 失败，无法产出最终报告，整个流水线无意义。

**恢复策略**：Level 2 降级 - abort

```json
{
  "id": "reporter",
  "retry": 1,
  "fallback": "abort"
}
```

**效果**：reporter 失败后，流水线中止。状态保存，可断点续传。

---

## 模式 5：断点续传（修复后恢复）

**场景**：流水线在第 3 个节点失败并中止，用户修复问题后想从断点继续。

**操作**：
```bash
# 1. 查看当前状态
python orchestrator.py status state.json

# 2. 重置失败节点为待执行
python orchestrator.py resume state.json

# 3. 继续执行
python orchestrator.py step state.json

# 4. 完成后生成报告
python orchestrator.py report state.json
```

**效果**：已完成的节点跳过，仅重新执行 failed 和 pending 节点。

---

## 恢复决策树

```
节点失败
  │
  ├─ retry_count < max_retry?
  │   ├─ 是 → Level 1: 重试（等待 2^n 秒）
  │   │         ├─ 成功 → 继续
  │   │         └─ 失败 → 回到决策树顶部
  │   └─ 否 → 进入降级
  │
  └─ fallback?
      ├─ skip → 跳过节点，下游收到空输出
      ├─ default → 使用 default_value，下游收到默认值
      └─ abort → 中止流水线，保存状态
                   ├─ 修复后 → resume 断点续传
                   └─ 不修复 → 生成部分报告
```

---

## 重试间隔说明

| 重试次数 | 等待时间 | 说明 |
|---------|---------|------|
| 第 1 次 | 2 秒 | 快速重试，适合临时性故障 |
| 第 2 次 | 4 秒 | 中等等待，适合限流恢复 |
| 第 3 次 | 8 秒 | 较长等待，适合服务重启 |
| 第 4 次 | 16 秒 | 长等待，适合严重故障 |

间隔公式：`delay = 2 ^ retry_count` 秒（指数退避）。
