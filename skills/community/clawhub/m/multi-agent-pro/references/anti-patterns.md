# 反模式说明

本文档列出 3 类常见错误用法及改进对比，帮助开发者避免常见陷阱。

---

## 反模式 1：循环依赖

### 错误用法

```json
{
  "agents": [
    {"id": "A", "depends_on": ["C"]},
    {"id": "B", "depends_on": ["A"]},
    {"id": "C", "depends_on": ["B"]}
  ]
}
```

**问题**：A → C → B → A 形成循环，拓扑排序无法完成，引擎会报错中止。

### 正确做法

打破循环，找到可以移除的依赖：

```json
{
  "agents": [
    {"id": "A", "depends_on": []},
    {"id": "B", "depends_on": ["A"]},
    {"id": "C", "depends_on": ["B"]}
  ]
}
```

如果确实需要双向数据传递，考虑合并为一个节点，或拆分为两个独立的流水线。

---

## 反模式 2：巨型节点

### 错误用法

```json
{
  "agents": [
    {
      "id": "do_everything",
      "name": "采集+清洗+分析+报告",
      "role": "完成所有工作",
      "depends_on": []
    }
  ]
}
```

**问题**：
- 失去了 DAG 编排的意义（等同于单 Agent 执行）
- 无法实现部分失败重试（一个环节失败要整体重来）
- 无法实现并行优化
- 输出数据庞大，状态文件臃肿

### 正确做法

按职责拆分为多个节点：

```json
{
  "agents": [
    {"id": "collector", "name": "数据采集", "depends_on": []},
    {"id": "cleaner", "name": "数据清洗", "depends_on": ["collector"]},
    {"id": "analyzer", "name": "数据分析", "depends_on": ["cleaner"]},
    {"id": "reporter", "name": "报告生成", "depends_on": ["analyzer"]}
  ]
}
```

**原则**：每个节点只负责一个明确的职责。

---

## 反模式 3：不设降级策略

### 错误用法

```json
{
  "agents": [
    {
      "id": "collector",
      "retry": 0,
      "fallback": "abort"
    }
  ]
}
```

**问题**：采集节点零容错，任何临时性故障（网络抖动、API 限流）都会导致整个流水线中止。

### 正确做法

根据节点重要性设置合理的容错策略：

```json
{
  "agents": [
    {
      "id": "collector",
      "retry": 3,
      "timeout": 60,
      "fallback": "skip"
    },
    {
      "id": "analyzer",
      "retry": 2,
      "timeout": 120,
      "fallback": "default",
      "default_value": {"analysis_result": "数据不足"}
    },
    {
      "id": "reporter",
      "retry": 1,
      "timeout": 180,
      "fallback": "abort"
    }
  ]
}
```

**原则**：
- 前端采集节点：高重试 + skip/default 降级（容错优先）
- 中间处理节点：中等重试 + default 降级（平衡）
- 末端输出节点：低重试 + abort（质量优先）

---

## 改进对比总结

| 反模式 | 问题 | 改进方向 |
|--------|------|---------|
| 循环依赖 | 死锁，无法执行 | 打破循环，改为 DAG |
| 巨型节点 | 丧失编排价值 | 按职责拆分 |
| 零容错 | 临时故障即中止 | 分层设置 retry + fallback |
