---
name: hermes-learning
description: Hermes 学习材料同步技能。从 Hermes Agent 获取自我更新后的学习材料，帮助 WorkBuddy 进行自我优化。支持 evolution.db 持久化、概念关联、双向反馈闭环。
trigger_words: 学习hermes经验、应用hermes学习、同步hermes知识、hermes最佳实践、hermes学习材料
version: 4.1.0
---

# Hermes 学习材料同步技能

此技能从 Hermes Agent 同步学习材料，帮助 WorkBuddy 进行自我更新和优化。

## 版本历史

- **v4.1 (2026-04-20)**: 同步 Hermes 生成器 v3.6（评分 9.0+）；悬空助词 100% 消除；词汇边界截断优化；rule_id 唯一性机制完善；专有名词规范化（Hermes Agent / WorkBuddy Agent）
- **v4 (2026-04-18)**: 修复 evolution.db 路径（全局路径）、移除无效 batch_size 自增、完善反馈数据结构
- **v3**: 双向反馈闭环、evolution.db 集成、概念关联
- **v2**: 策略库 + 效果追踪
- **v1**: 基础学习材料同步

## 学习材料来源

所有材料来自 Hermes 的记忆处理系统：
- 位置：`~/.hermes/shared/memory_summary.json`
- 反馈文件：`~/.hermes/shared/workbuddy_feedback.json`
- 策略库：`~/.workbuddy/skills/hermes-learning/strategies.json`

## evolution.db

- **路径**: `~/.workbuddy/memory/evolution.db`（全局统一路径）
- **表**: memories（学习条目）、concept_links（概念关联）
- **来源标识**: source = 'hermes_learning'

## 使用方法

```bash
# 查看状态
python3 ~/.workbuddy/skills/hermes-learning/apply_learning.py status

# 应用学习材料
python3 ~/.workbuddy/skills/hermes-learning/apply_learning.py apply

# 列出所有策略
python3 ~/.workbuddy/skills/hermes-learning/apply_learning.py list

# 检查内容是否命中避免模式
python3 ~/.workbuddy/skills/hermes-learning/apply_learning.py check "要检查的内容"

# 查看反馈分析
python3 ~/.workbuddy/skills/hermes-learning/apply_learning.py feedback
```

## 双向反馈

- **Hermes → WorkBuddy**: 学习材料通过 `memory_summary.json` 同步
- **WorkBuddy → Hermes**: 反馈通过 `workbuddy_feedback.json` 回传
- **效果报告**: `learning_effect_report.json` 记录应用效果
