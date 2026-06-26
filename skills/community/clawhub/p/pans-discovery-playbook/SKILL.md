---
name: pans-discovery-playbook
description: |
  AI算力销售发现阶段话术与框架工具。根据沟通场景（首次电话/需求介绍/POC/
  续约增购）和行业（科技/金融/医疗/自动驾驶/内容/制造/学术/政府）
  自动生成访谈问题清单、行业背景知识、话术建议和异议处理策略，
  输出 Markdown 或 JSON 格式发现指南。
  触发词：发现阶段, 客户访谈, 话术指南, 异议处理, 需求挖掘,
  discovery, 首次沟通, 客户沟通, 销售话术
---

# Pans Discovery Playbook

## Overview

AI算力销售发现阶段话术与框架工具。根据场景和行业生成访谈问题、话术建议和异议处理策略。

## 场景

| 场景 | 说明 |
|------|------|
| `first_call` | 首次电话沟通（冷启动，15-20分钟） |
| `intro_call` | 需求介绍会议（深入了解，30-60分钟） |
| `poc` | POC阶段访谈（技术细节，45-90分钟） |
| `renewal` | 续约/增购沟通（价值回顾，20-30分钟） |

## 行业

`technology` / `finance` / `healthcare` / `autonomous` / `media` / `manufacturing` / `academic` / `government`

## 使用方法

```bash
# 生成首次电话沟通指南（科技行业）
python3 scripts/discovery.py --scenario first_call --industry technology --format markdown

# 生成 POC 访谈指南（金融行业）
python3 scripts/discovery.py --scenario poc --industry finance --format json --output result.json

# 续约增购沟通
python3 scripts/discovery.py --scenario renewal --industry healthcare
```

## 关键发现记录

工具输出包含结构化发现记录模板，覆盖：
- 现状了解（团队规模、AI方向、现有架构）
- 痛点挖掘（核心痛点、紧迫度、业务影响）
- 权力确认（决策人、技术评估团队）
- 预算探索（年投入、价格敏感度）
- 时间线确认（POC需求、关键节点）
- 竞争态势（现有供应商、我们的优势）
