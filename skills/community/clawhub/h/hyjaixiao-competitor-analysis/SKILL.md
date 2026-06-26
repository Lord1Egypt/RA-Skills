---
name: competitor-analyzer-v1
description: 竞品分析神器 v1.0。输入你的产品和竞品列表，自动生成结构化竞品分析报告，含对比矩阵、战略建议、风险预警。
version: 1.0.0
tags: [analysis, competitor, business, strategy, market-research, report]
author: AI Skill 商业生产
price: ¥39.9
---

# 📊 竞品分析神器 v1.0 (付费版)

## 一句话卖点

> **输入你的产品+竞品，自动输出完整的竞品分析报告。创业、立项、融资前必做。**

## 核心能力

1. **一键分析** — 输入产品名称和竞品列表，自动生成结构化报告
2. **完整框架** — 行业概览→竞品逐一分析→对比矩阵→战略建议→风险预警
3. **双模式** — 有API Key走AI深度分析，无Key走模板框架
4. **历史管理** — 所有报告自动存档，随时回顾对比
5. **快速检查** — --quick模式，快速概览竞品格局

## 使用方式

### 深度分析（推荐）

```bash
python3 competitor_analyzer.py \
  --product "AI短视频生成器" \
  --competitors "剪映,Pika,RunwayML,HeyGen" \
  --strengths "中文支持好,竖屏优化,自动化程度高" \
  --market "国内自媒体创作者" \
  --category "AI视频工具"
```

### 快速检查

```bash
python3 competitor_analyzer.py \
  --product "我的笔记App" \
  --competitors "Notion,飞书,语雀" \
  --quick
```

## 报告结构

```
一、行业概览          ← 市场规模、玩家格局
二、竞品逐一分析     ← 每个竞品的定位/功能/定价/弱点
三、对比矩阵          ← 多维度评分对比表
四、战略建议          ← 短/中/长期可执行策略
五、风险预警          ← 需要警惕的风险点
```

## 环境要求

- Python 3.8+
- OpenAI API Key (推荐 gpt-4o-mini，走深度分析)
- `pip install requests`

## 配置

```bash
export OPENAI_API_KEY="sk-xxx"
# 可选
export OPENAI_MODEL="gpt-4o-mini"
export CA_OUTPUT_DIR="./ca_output"
export CA_FREE_MODE="false"  # true=强制模板模式
```

## 输出

```
ca_output/20260425/
└── 竞品分析_AI短视频生成器_20260425_153000.md
```

---

## 上架物料

### 卖点文案

> **创业第一步：搞清楚你的对手是谁。**
>
> 市面上100个创业项目，90个死于不了解竞争。
>
> 📊 这个工具帮你：
> ✅ 输入产品，自动分析竞品定位、功能、定价
> ✅ 输出多维度对比矩阵，看清差距在哪
> ✅ 给出短中长期的战略建议
>
> 不管是立项调研、融资准备，还是日常竞争监控
> 一份清晰的竞品分析报告，就是你的作战地图
>
> 💰 ¥39.9，一次购买永久使用
> 👇 想看清战场的，上车

### 目标用户
- 创业者 / 产品经理
- 投资人做DD
- 企业战略部门
- 自由职业者接商业分析单
- 大学生创业比赛

### 关键词标签

`竞品分析` `市场调研` `商业分析` `产品分析` `竞争策略` `创业工具` `商业计划` `融资准备` `市场研究` `战略分析`
