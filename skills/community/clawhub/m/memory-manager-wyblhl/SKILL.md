---
name: memory-manager
description: >
  自动管理 OpenClaw 的记忆系统，包括工作记忆、短期记忆、长期记忆、记忆合并与压缩。
  Triggers: memory manager, memory management, 记忆管理，memory compression, memory cleanup
metadata:
  author: wyblhl
  version: "1.0.0"
---

# 🧠 Memory Manager - 记忆管理技能

**版本**: 1.0
**创建时间**: 2026-03-19
**状态**: ✅ 激活

---

## 🎯 功能说明

自动管理 OpenClaw 的记忆系统，包括：
- 工作记忆（最近 7 天）
- 短期记忆（最近 30 天）
- 长期记忆（永久保存）
- 记忆合并与压缩
- 记忆清理与归档

---

## 📁 记忆结构

```
D:\OpenClaw\workspace\memory\
├── MEMORY.md                    ← 主记忆文件（始终保留）
├── capabilities.json            ← 能力评估（每次学习后更新）
├── knowledge-graph.json         ← 知识图谱（每次学习后更新）
├── learning-round-*.json        ← 学习轮次记录（保留最近 50 轮）
├── conversation-*.json          ← 会话记录（保留最近 10 个）
└── tiers/
    ├── config.json              ← 分层配置
    ├── working/                 ← 工作记忆（7 天）
    ├── short-term/              ← 短期记忆（30 天）
    └── long-term/               ← 长期记忆（永久）
```

---

## 🔄 自动执行任务

### 每轮学习后
1. 更新 `capabilities.json`
2. 更新 `knowledge-graph.json`
3. 创建 `learning-round-N.json`
4. 保存到 `memory/tiers/working/`

### 每日清理
1. 合并 7 天前的工作记忆到短期记忆
2. 合并 30 天前的短期记忆到长期记忆
3. 删除超过 50 轮的旧学习记录
4. 生成记忆归档报告

### 每周优化
1. 压缩长期记忆文件
2. 生成记忆统计报告
3. 优化知识图谱结构

---

## ⚙️ 配置参数

```json
{
  "memoryManager": {
    "enabled": true,
    "workingMemoryDays": 7,
    "shortTermMemoryDays": 30,
    "maxLearningRounds": 50,
    "maxConversations": 10,
    "autoCompact": true,
    "compactThreshold": 0.7,
    "mergeStrategy": "summarize"
  }
}
```

---

## 📝 记忆合并策略

### 合并规则
1. **相同主题合并**: 将相同主题的记忆合并为一条
2. **时间序列合并**: 按时间顺序合并连续的记忆
3. **重要性分级**: 高重要性记忆单独保留
4. **知识关联**: 建立记忆之间的关联边

### 压缩算法
```
原始记忆 → 提取关键词 → 生成摘要 → 保存核心信息 → 删除冗余
```

---

## 🚀 使用方法

### 自动触发
每轮学习完成后自动执行记忆管理

### 手动触发
```bash
# 运行记忆管理
node -e "require('./skills/memory-manager').run()"

# 清理旧记忆
node -e "require('./skills/memory-manager').cleanup()"

# 合并记忆
node -e "require('./skills/memory-manager').merge()"
```

---

## 📊 记忆质量指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 记忆完整度 | ≥95% | - |
| 检索响应时间 | <100ms | - |
| 压缩率 | ≥50% | - |
| 关联准确率 | ≥90% | - |

---

## 🔐 安全保护

- ✅ 合并前自动备份
- ✅ 删除前确认重要性
- ✅ 关键记忆永久保留
- ✅ 错误恢复机制

---

**记忆管理技能结束**
