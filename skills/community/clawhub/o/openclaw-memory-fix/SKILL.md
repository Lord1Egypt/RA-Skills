---
name: openclaw-memory-fix
description: OpenClaw记忆系统优化方案 - 四层架构 + 动态衰减 + 智能检索
homepage: https://github.com/openclaw/openclaw
metadata:
  clawdbot:
    emoji: 🧠
    requires:
      bins: [node]
      env: []
    triggers:
      - 记忆系统
      - 优化记忆
      - 记忆衰减
      - 记忆检索
---

# OpenClaw Memory Fix 🧠

OpenClaw记忆系统优化方案 - 四层架构 + 动态衰减 + 智能检索

## 功能

### 1. 四层记忆架构
- L1 短期记忆：当前会话、任务状态
- L2 情景记忆：场景、情绪、置信度
- L3 语义记忆：知识库、经验教训
- L4 长期记忆：核心原则、用户画像

### 2. 层间迁移
| 方向 | 触发条件 |
|------|---------|
| L1→L2 | 任务完成、用户确认 |
| L2→L3 | 相似情景3次+ |
| L3→L4 | 知识验证10次+ |

### 3. 动态衰减
- L4核心原则：永久保留
- L4画像：1%/月
- L3知识：5%/月
- L2情景：10%/月
- L1临时：50%/会话

### 4. 智能检索
- 向量索引 + 知识图谱
- 多维筛选（标签/时间/情绪）

### 5. 自我反思
- 记忆模糊时主动询问
- 效能监控与调优

## 使用方法

```bash
# 查看记忆状态
node scripts/memory.js status

# 手动触发迁移
node scripts/memory.js migrate

# 触发遗忘模拟
node scripts/memory.js preview-decay
```

## 配置

在 WORKSPACE 下创建 `memory/` 目录：

```
memory/
├── L1/           # 短期记忆
├── L2/           # 情景记忆
├── L3/           # 语义记忆
├── L4/           # 长期记忆
└── config.json   # 配置文件
```

## 详细文档

参考：`references/MEMORY.md`

## 更新日志

- 2026-03-08: 初始版本
  - 四层架构
  - 动态衰减
  - 智能检索
  - 自我反思

---

作者：Odin for 馒头哥
