---
name: product-framework
description: Design product frameworks and architecture for AI product managers. Use when: (1) structuring a new product from scratch, (2) creating a product architecture diagram or layered model, (3) doing competitive analysis and positioning, (4) defining product pillars or capability maps, (5) organizing complex product thinking into a coherent framework. NOT for: detailed feature specs (use prd-writer), engineering architecture, or code design.
---

# Product Framework

Help AI product managers structure product thinking into clear, communicable frameworks.

## Core Frameworks

### 1. 产品分层架构（Layered Architecture）

Standard 4-layer model for AI products:

```
┌─────────────────────────────┐
│        用户体验层            │  交互、界面、触点
├─────────────────────────────┤
│        产品能力层            │  核心功能、AI 能力
├─────────────────────────────┤
│        数据/模型层           │  数据资产、算法模型
├─────────────────────────────┤
│        基础设施层            │  计算、存储、平台
└─────────────────────────────┘
```

Use this when mapping "what the product is made of."

### 2. 用户价值框架（Value Framework）

```
用户痛点 → 解决方案 → 差异化价值 → 商业模式
```

Use this when articulating "why this product matters."

### 3. 能力地图（Capability Map）

Map capabilities to: Core（护城河）/ Supporting（支撑）/ Commodity（通用）

### 4. 竞品定位矩阵

Pick 2 key dimensions → plot competitors → find whitespace.

## Process

1. **理解产品方向** — 问清楚产品是什么、面向谁、解决什么问题
2. **选择合适框架** — 根据目的选框架（架构图 / 价值链 / 竞品对比）
3. **填充内容** — 按层次逐步填入具体内容
4. **输出文档** — Markdown 表格 + Mermaid 图（参见 mermaid-diagram skill）

## Output Format

- 用 Markdown 结构化输出，带标题层级
- 关键框架用 Mermaid mindmap 或 flowchart 可视化
- 每个框架组件附一句话说明

## Reference Files

- **references/framework-templates.md** — 常用框架模板（可直接填充使用）
- **references/ai-product-patterns.md** — AI 产品常见模式（AIGC、推荐、搜索、对话等）

Read references when: user asks for a specific framework type, or when building frameworks for AI-specific product categories.
