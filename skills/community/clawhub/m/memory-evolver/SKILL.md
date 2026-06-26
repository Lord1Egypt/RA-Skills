---
name: memory-evolver
description: 记忆系统优化器 - 结合三层记忆与知识图谱的持续自我进化系统。自动诊断、优化、记录记忆系统状态，实现记忆的持续进化。
---

# Memory Evolver - 记忆进化器

## 概述

结合三层记忆系统（MEMORY.md + 每日日志 + PROJECTS.md）与知识图谱的持续自我进化系统。

## 核心理念

- 🔄 **持续循环**: 诊断 → 计划 → 执行 → 记录 → 进化
- 🧠 **三层记忆**: 长期记忆 + 每日日志 + 项目跟踪
- 🔗 **知识图谱**: 从记忆构建语义网络
- 📈 **指数成长**: 1% daily improvement = 37x yearly growth

## 功能

### 1. 记忆系统诊断
- 检查 MEMORY.md 完整性
- 检查 PROJECTS.md 状态
- 检查每日日志数量
- 检查知识图谱实体数

### 2. 优化计划生成
- 根据问题生成优化优先级
- 分类：高/中/低
- 可执行的具体行动

### 3. 知识图谱重建
- 从 memory/ 文件提取实体
- 识别实体间关系
- 构建可查询的图结构

### 4. 优化循环日志
- 记录每次优化的诊断、计划、执行
- 追踪优化历史
- 持续改进机制

## 文件结构

```
memory-evolver/
├── SKILL.md              # 本文件
├── index.py              # 主程序
├── diagnose.py          # 诊断模块
├── knowledge_graph.py    # 知识图谱
└── config.json          # 配置
```

## 使用方式

### 手动运行
```bash
python skills/memory-evolver/index.py
```

### 定时执行
```bash
# 每天23点自动优化
openclaw cron add --name "memory-evolver" --cron "0 23 * * *"
```

## EvoMap 集成

- **Node ID**: node_6d28b52505ad2d41
- **状态**: 自动化运行
- **报告**: 支持 Feishu 卡片报告

## 三层记忆模板

### MEMORY.md (长期)
```markdown
# 长期记忆
## 核心锚点
- 用户: 先生
- 风格: 直接、效率优先
## 目标
- [ ] 构建完整AI系统
```

### memory/YYYY-MM-DD.md (每日)
```markdown
# 2026-03-18
## 事件
- 11:00: 创建知识图谱
## 决策
- 优先先生指定功能
```

### PROJECTS.md (项目)
```markdown
## 项目名
- 状态: X/Y
- 阻碍: 无
- 下一步: 继续优化
```

## 成功指标

- [x] 诊断系统就绪
- [x] 优化循环建立
- [x] 知识图谱可查询
- [ ] 每日自动运行

---

**版本**: 1.0.0  
**作者**: Sharon  
**EvoMap**: node_6d28b52505ad2d41
