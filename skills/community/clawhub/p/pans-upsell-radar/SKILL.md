---
name: pans-upsell-radar
description: |
  AI算力销售增购机会雷达。识别GPU利用率、团队扩张、新模型发布等增购信号。
  支持机会评分、扩容方案生成、最佳时机预测。
  触发词：增购机会, 扩容信号, upsell, 交叉销售, 客户增长
---

# pans-upsell-radar 使用指南

## 概述

pans-upsell-radar 是 AI 算力销售增购机会雷达工具，帮助识别客户扩容信号、评估增购机会并生成扩容方案。

## 核心功能

### 增购信号识别
- GPU 利用率持续 >80%
- 任务排队时间增加
- 团队扩张（新成员加入）
- 新模型发布（需要更大算力）
- 业务增长（收入/用户增长）
- 新区域/新场景需求

### 机会评分体系
- **高**：多个信号 + 决策窗口期 → 立即跟进
- **中**：单一信号 → 持续观察
- **低**：潜在需求 → 培育阶段

## CLI 参数

| 参数 | 说明 |
|------|------|
| `--scan` | 扫描所有客户，生成增购机会报告 |
| `--client <name>` | 分析指定客户，输出详细信号和评分 |
| `--list` | 列出所有增购机会（快速概览） |
| `--score` | 显示各客户机会评分 |
| `--suggest` | 生成增购方案和建议 |

## 使用示例

```bash
# 扫描所有客户
python upsell.py --scan

# 分析指定客户
python upsell.py --client "某AI公司"

# 列出增购机会
python upsell.py --list

# 显示机会评分
python upsell.py --score

# 生成增购方案
python upsell.py --suggest
```

## 数据存储

- 客户数据：`~/.qclaw/skills/pans-upsell-radar/data/customers.json`
- 信号记录：`~/.qclaw/skills/pans-upsell-radar/data/signals.json`
- 机会评分：`~/.qclaw/skills/pans-upsell-radar/data/opportunities.json`

## 输出格式

工具输出结构化的增购机会报告，包含：
- 客户名称
- 识别到的信号列表
- 机会评分（高/中/低）
- 建议的扩容方案
- 最佳跟进时机
