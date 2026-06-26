---
name: memory-strategy
description: |
  当用户需要管理对话记忆时应使用此skill。
  
  触发条件包括：
  - 用户说"记下来"、"记住这个"、"别忘了"、"永久保存"、"这是一个重点"
  - 用户查询历史信息："之前是怎么做的"、"查找关于...的记录"、"回忆一下..."
  - 会话结束需要自动整理归档
  - 需要评估信息重要性并决定存储位置
  - 需要更新记忆索引或检索规则
  
  本skill提供双层记忆机制（长期记忆+短期记忆）、时间衰减算法（30天周期）、
  智能评分系统（1-5分）和Silent Agent自动整理功能。
version: 1.0.0
author: HugoChan
---

# Memory Strategy Skill

## 概述

本skill提供完整的对话记忆管理策略，包括：
- **双层记忆架构**：长期记忆（永久保存）+ 短期记忆（30天衰减）
- **时间衰减机制**：近期内容权重更高，自动归档过期记忆
- **智能评分系统**：1-5分自动评估信息重要性
- **Silent Agent**：会话结束自动整理归档

## 快速开始

### 初始化记忆系统

在首次使用时，创建记忆目录结构：

```bash
# 在项目根目录执行
mkdir -p .memory/{long-term,short-term}
touch .memory/INDEX.md
touch .memory/README.md
```

### 配置参数

在 `.memory/config.yaml` 中配置：

```yaml
# 时间衰减配置
time_decay:
  period: 30              # 衰减周期（天）
  min_weight: 0.2         # 最小权重
  curve: "linear"         # 衰减曲线：linear/exponential

# 评分维度权重
scoring_weights:
  impact: 0.25            # 影响范围
  persistence: 0.25       # 持久性
  reusability: 0.25       # 复用价值
  decision_basis: 0.25    # 决策依据

# 存储路径
storage_paths:
  core_memory: ".memory/long-term/MEMORY.md"
  contacts: ".memory/long-term/contacts.md"
  projects: ".memory/long-term/projects.md"
  decisions: ".memory/long-term/decisions.md"
  patterns: ".memory/long-term/patterns.md"
  preferences: ".memory/long-term/preferences.md"
  feedback: ".memory/long-term/feedback.md"
  daily_log: ".memory/short-term/"
```

## 核心功能

### 1. 记忆写入

#### 自动评分（支持 Kimi API）

**方式1：Kimi API 智能评分（推荐）**
```bash
python scripts/evaluate_importance.py --auto --text "这里是需要评分的内容"
```
Kimi API 会根据内容语义自动判断4个维度的分值。

**方式2：手动输入4维度**
```
总分 = 影响范围×25% + 持久性×25% + 复用价值×25% + 决策依据×25%

5分 (核心配置) → 写入 MEMORY.md
4分 (重要经验) → 写入 patterns.md 或 decisions.md
3分 (常规工作) → 写入当日日志
2分 (临时工作) → 写入当日日志（简要）
1分 (不记录)   → 丢弃
```

#### 触发词检测

用户说以下词语时自动提升评分：

| 触发词 | 评分 | 写入位置 |
|--------|------|----------|
| "永久保存" | 5分 | MEMORY.md |
| "这是一个重点" | 5分 | MEMORY.md |
| "记下来" | 4分 | 长期记忆 |
| "记住这个" | 4分 | 长期记忆 |
| "别忘了" | 4分 | 长期记忆 |

### 2. 记忆检索

#### 时间衰减权重

```
天数    权重    加载方式
─────────────────────────────
0-3     100%    完整内容 + [最近]标签
4-7     80%     完整内容 + [近期]标签
8-14    60%     摘要形式
15-30   40%     仅关键信息
>30     20%     已归档，仅强匹配时加载

权重公式: weight = max(0.2, 1 - (days / 30) × 0.8)
```

#### 三级检索策略

```
Level 1: 核心记忆 (P0)
├── MEMORY.md - 关键配置段落
└── contacts.md - 相关API密钥

Level 2: 专题记忆 (P1/P2)
├── 检测用户查询关键词
├── 匹配INDEX.md主题分类
└── 加载对应的专题文件

Level 3: 历史记忆
├── 0-7天: 完整内容，高权重
├── 8-30天: 摘要形式，中权重
└── >30天: 已归档，低权重
```

### 3. Silent Agent 静默整理

#### 触发时机
- 会话结束前（用户说"结束"、"就这样"）
- 长时间无交互（10分钟）
- 用户说"立即整理"

#### 整理流程

1. **内容提取**：回顾会话，提取关键事件
2. **自动评分**：4维度加权计算1-5分
3. **分级写入**：按评分写入对应文件
4. **更新索引**：更新INDEX.md
5. **生成报告**：向用户展示整理结果

#### 输出示例

```
[Silent Agent] 已为您整理今日记录：
- ⭐⭐⭐⭐⭐ 5分（核心配置）：1条 → 已保存到 MEMORY.md
- ⭐⭐⭐⭐ 4分（重要经验）：2条 → 已保存到 patterns.md
- ⭐⭐⭐ 3分（常规工作）：3条 → 已记录到 2026-03-15.md
```

## 工作流程

### 场景1：用户说"记下来"

```
用户: "记下来：第三方API字段映射需要验证实际返回格式"
     ↓
检测到触发词"记下来"
     ↓
自动评分: 4分（用户明确要求记录）
     ↓
写入: .memory/long-term/patterns.md
     ↓
更新: .memory/INDEX.md 索引
     ↓
反馈: "已记录到patterns.md，评分4分"
```

### 场景2：会话结束自动整理

```
用户: "结束今天的对话"
     ↓
触发Silent Agent
     ↓
提取关键事件:
  - 设计双层记忆机制 → 5分
  - 修复API字段映射 → 4分
  - 更新配置文件 → 3分
     ↓
分级写入:
  - 5分 → MEMORY.md
  - 4分 → patterns.md
  - 3分 → 2026-03-15.md
     ↓
更新索引 → 生成报告
```

### 场景3：查询历史记忆

```
用户: "之前是怎么配置数据监控的？"
     ↓
关键词匹配: "数据监控"
     ↓
加载相关记忆:
  - projects.md#stock-monitor (Level 2)
  - 近7天日志中相关内容 (Level 3, 80%权重)
  - 7-30天日志摘要 (Level 3, 40%权重)
     ↓
整合回答
```

## 文件结构

```
.memory/
├── INDEX.md              # 记忆索引（快速导航）
├── README.md             # 使用说明
├── config.yaml           # 配置文件
│
├── long-term/            # 长期记忆（始终生效）
│   ├── MEMORY.md         # 核心知识库（P0）
│   ├── contacts.md       # 联系人信息（P0）
│   ├── projects.md       # 项目信息（P1）
│   ├── decisions.md      # 重要决策（P1）
│   ├── patterns.md       # 模式实践（P2）
│   ├── preferences.md    # 用户偏好（P2）
│   └── feedback.md       # 反馈记录（P2）
│
└── short-term/           # 短期记忆（30天衰减）
    └── YYYY-MM-DD.md     # 每日工作记录
```

## 使用脚本

### evaluate_importance.py

评估信息重要性并返回1-5分，支持手动评分和 Kimi API 自动评分：

**手动评分：**
```bash
python scripts/evaluate_importance.py \
  --impact 5 \
  --persistence 5 \
  --reusability 4 \
  --decision_basis 5
```

**Kimi API 自动评分（推荐）：**
```bash
# 需要先配置 API Key
export KIMI_API_KEY="your-api-key"

python scripts/evaluate_importance.py \
  --auto \
  --text "这是一个需要评估重要性的工作内容描述..."
```

**输出示例：**
```json
{
  "score": 4,
  "level": "重要经验",
  "storage": "long-term/patterns.md 或 decisions.md",
  "stars": "⭐⭐⭐⭐",
  "dimensions": {
    "impact": 4,
    "persistence": 5,
    "reusability": 4,
    "decision_basis": 4
  },
  "reasoning": "这是一个重要的技术方案决策...",
  "method": "kimi_api"
}
```

### retrieve_memory.py

检索记忆（带时间衰减）：

```python
python scripts/retrieve_memory.py \
  --query "数据监控" \
  --days 30 \
  --output results.json
```

### silent_agent.py

静默整理会话内容：

```python
python scripts/silent_agent.py \
  --session-log conversation.json \
  --auto-write true
```

### update_index.py

更新记忆索引：

```python
python scripts/update_index.py \
  --memory-dir .memory/
```

## 最佳实践

### 记忆写入
- 完成实质性工作后自动追加到当日日志
- 重要决策、偏好变更立即写入长期记忆
- 使用触发词强制提升优先级

### 记忆检索
- 会话开始时读取相关长期记忆
- 涉及历史工作时读取对应日期的短期记忆
- 利用时间衰减优先查看近期内容

### 定期维护
- 每周检查当日日志长度
- 每月1日整理上月短期记忆
- 将重要信息迁移到长期记忆
- 删除已无价值的临时记录

## 故障排除

### 问题1：记忆写入失败
**原因**: 目录权限不足或路径错误
**解决**: 检查 `.memory/` 目录权限，确认 config.yaml 路径配置正确

### 问题2：检索不到历史记忆
**原因**: 索引未更新或关键词不匹配
**解决**: 运行 `update_index.py` 更新索引，检查INDEX.md中的标签

### 问题3：Silent Agent未触发
**原因**: 触发条件未满足
**解决**: 手动说"立即整理"触发，或检查config.yaml中的超时设置

## 参考文档

- `references/retrieval_rules.md` - 检索规则详解
- `references/scoring_criteria.md` - 评分标准
- `references/time_decay_formula.md` - 时间衰减算法
- `references/silent_agent_guide.md` - Silent Agent使用指南

## 示例文件

- `assets/templates/daily_log_template.md` - 每日日志模板
- `assets/templates/memory_index_template.md` - 索引模板
- `assets/examples/sample_daily_log.md` - 示例日志

## 版本历史

- v1.0.0 (2026-03-15) - 初始版本，包含双层记忆、时间衰减、智能评分、Silent Agent