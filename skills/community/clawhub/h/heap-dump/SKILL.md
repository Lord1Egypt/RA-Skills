---
name: heap-dump
description: 内存快照分析（v8 heap snapshot）+ 性能分析（perf_hooks）
version: 1.0.1
---

# Heap Dump & Profiler — 内存与性能分析

**版本**: 1.0.1  
**创建日期**: 2026-04-13  
**更新日期**: 2026-04-14

---

## 📋 功能

| 功能 | 说明 |
|------|------|
| **heap-dump** | 生成 v8 堆快照，Chrome DevTools 分析 |
| **profiler** | perf_hooks 性能分析（start/checkpoint/end/report） |

---

## 📂 文件结构

```
skills/heap-dump/
├── SKILL.md
├── skill.json
└── scripts/
    ├── heap-dump.js     # 内存快照生成
    └── profiler.js      # 性能分析工具
```

---

## 🔧 用法

```bash
# 内存快照
node skills/heap-dump/scripts/heap-dump.js snapshot

# 性能分析
node skills/heap-dump/scripts/profiler.js start "任务名"   # 开始
node skills/heap-dump/scripts/profiler.js checkpoint "阶段" # 标记点
node skills/heap-dump/scripts/profiler.js end              # 结束
node skills/heap-dump/scripts/profiler.js report           # 生成报告
```

---

## 📊 触发方式

- **手动触发**（按需使用的诊断工具，无需自动化）

---

## ⚠️ 注意事项

- heap snapshot 文件较大，建议分析后删除
- profiler 输出写入 `memory/perf/` 目录
- 已合并 headless-profiler 功能
