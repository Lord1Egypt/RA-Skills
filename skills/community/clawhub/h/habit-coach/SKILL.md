---
name: habit-coach
description: "习惯养成教练。充当AI问责伙伴，帮助建立、追踪和坚持好习惯。Keywords: 习惯养成, 自律, habit tracker, 打卡."
---

## 概述

充当AI问责伙伴，帮助建立、追踪和坚持好习惯。适用于日常习惯打卡、目标进度追踪、行为模式分析等场景。awesome-openclaw-usecases收录：带问责机制的习惯追踪器。

## 适用范围

**适用场景**：
- 每日习惯打卡记录
- 查看习惯连续坚持天数
- 制定新的习惯养成计划

**不适用场景**：
- 需要实时硬件控制或低延迟响应的场景
- 涉及敏感个人隐私数据的未授权处理

**触发关键词**: 习惯养成, 自律, habit tracker, 打卡, 问责

## 前置条件

```bash
pip install requests
```

> ⚠️ 首次使用前请确认依赖已安装，否则脚本将无法运行。

## 核心能力

### 能力1：个性化习惯计划制定与打卡追踪
个性化习惯计划制定与打卡追踪

### 能力2：AI问责伙伴——鼓励/提醒/分析原因
AI问责伙伴——鼓励/提醒/分析原因

### 能力3：习惯数据可视化与行为模式洞察
习惯数据可视化与行为模式洞察


## 命令列表

| 命令 | 说明 | 用法 |
|------|------|------|
| `track` | 习惯打卡 | `python3 scripts/habit_coach_tool.py track [参数]` |
| `review` | 进度回顾 | `python3 scripts/habit_coach_tool.py review [参数]` |
| `plan` | 制定计划 | `python3 scripts/habit_coach_tool.py plan [参数]` |


## 处理步骤

### Step 1：习惯打卡

**目标**：打卡今日运动和阅读

**为什么这一步重要**：这是整个工作流的数据采集/初始化阶段，确保后续步骤基于准确的输入。

**执行**：
```bash
python3 scripts/habit_coach_tool.py track --habits 'exercise,reading' --status done
```

**检查点**：确认输出包含预期数据，无报错信息。

### Step 2：进度回顾

**目标**：回顾本月习惯完成情况

**为什么这一步重要**：核心处理阶段，将原始数据转化为有价值的输出。

**执行**：
```bash
python3 scripts/habit_coach_tool.py review --range month --show-streaks
```

**检查点**：确认生成结果格式正确，内容完整。

### Step 3：制定计划

**目标**：制定新的21天习惯计划

**为什么这一步重要**：最终输出阶段，将处理结果以可用的形式呈现。

**执行**：
```bash
python3 scripts/habit_coach_tool.py plan --habit '每天冥想10分钟' --duration 21d
```

**检查点**：确认最终输出符合预期格式和质量标准。

## 验证清单

- [ ] 依赖已安装：`pip install requests`
- [ ] Step 1 执行无报错，输出数据完整
- [ ] Step 2 处理结果符合预期格式
- [ ] Step 3 最终输出质量达标
- [ ] 无敏感信息泄露（API Key、密码等）

## 输出格式

```markdown
# 📊 习惯养成教练报告

**生成时间**: YYYY-MM-DD HH:MM

## 核心发现
1. [关键发现1]
2. [关键发现2]
3. [关键发现3]

## 数据概览
| 指标 | 数值 | 趋势 | 评级 |
|------|------|------|------|
| 指标A | XXX | ↑ | ⭐⭐⭐⭐ |
| 指标B | YYY | → | ⭐⭐⭐ |

## 详细分析
[基于实际数据的多维度分析内容]

## 行动建议
| 优先级 | 建议 | 预期效果 |
|--------|------|----------|
| 🔴 高 | [具体建议] | [量化预期] |
| 🟡 中 | [具体建议] | [量化预期] |
```

## 参考资料

### 原有链接
- [Atomic Habits框架](https://jamesclear.com/atomic-habits)

### GitHub
- [awesome-openclaw-usecases Habit Tracker](https://github.com/hesamsheikh/awesome-openclaw-usecases)

### Reddit
- [Reddit: AI习惯追踪与问责讨论](https://www.reddit.com/r/productivity/comments/ai_habit_tracker/)

## 注意事项

- 所有分析基于脚本获取的实际数据，**不编造数据**
- 数据缺失字段标注"数据不可用"而非猜测
- 建议结合人工判断使用，AI分析仅供参考
- 首次使用请先安装依赖：`pip install requests`
- 如遇到API限流，请适当增加请求间隔
