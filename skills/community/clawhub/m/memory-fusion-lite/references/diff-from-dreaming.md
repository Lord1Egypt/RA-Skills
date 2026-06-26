# memory-fusion-lite vs Dreaming — 分工边界说明

## 核心区别

| 维度 | Dreaming | memory-fusion-lite |
|------|----------|-------------------|
| **定位** | 语义理解和记忆整理 | 增量扫描和滚动更新 |
| **触发** | 每晚 3am（固定一次） | L2 23:30 / L3 周一 00:20 |
| **处理范围** | 全量 session 历史 | 上次处理后的增量 |
| **输出重点** | 语义提炼 → DREAMS.md | 滚动更新 → MEMORY.md A′区 |
| **分类** | 按语义主题自动分类 | 人工定义的分类（偏好/决策/项目） |
| **遗忘机制** | HOT/WARM/COLD 晋升+淘汰 | 滚动7天窗口 + 每周清理 |

## 分工协作图

```
session JSONL（每日新增）
    │
    ├──→ Dreaming（每晚 3am）────→ DREAMS.md + memory/dreaming/
    │                                    │
    │                              语义理解 + 记忆提炼
    │
    └──→ memory-fusion-lite L2（每天 23:30）→ MEMORY.md#A′ 滚动7天
              │
              ├──→ A′ 区（每日最多5条，滚动清理）
              │
              └──→ memory-fusion-lite L3（每周一）→ MEMORY.md 主分类 + weekly 归档
                           │
                           └──→ 晋升 + 分类治理 + 归档
```

## 关键设计原则

1. **Dreaming 负责理解**：深度语义分析，提炼模式
2. **memory-fusion-lite 负责维护**：增量更新，滚动清理，分类治理
3. **两者都写 MEMORY.md**：不冲突，内容互补
   - Dreaming 写语义提炼的洞见
   - memory-fusion-lite 写用户偏好/决策/项目进展

## 冲突避免

如果两边同时写 A′ 区同一批次 session，以 **memory-fusion-lite L2** 的结果为准（因为它是增量、更精确）。

Dreaming 不会写 A′ 区，只写 DREAMS.md。

## 何时启用 memory-fusion-lite

| 条件 | 建议 |
|------|------|
| Dreaming 正常运行 | ✅ 可以加 |
| 觉得 Dreaming 不够勤快（只有每晚一次） | ✅ 值得加 |
| 希望 MEMORY.md 更快更新 | ✅ 值得加 |
| 未启用 Dreaming | ❌ 先启用 Dreaming |
| 觉得系统已经太复杂 | ❌ 不要加 |
