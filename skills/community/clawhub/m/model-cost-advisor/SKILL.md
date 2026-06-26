---
name: model-cost-advisor
description: Analyze any task and recommend the most cost-effective LLM — with live pricing data from 30+ models, tier analysis, token estimation, and projected cost. Perfect for developers who use multiple LLMs and want to optimize spending.
version: 1.1.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [AI, Cost, LLM, Pricing, Optimization, Budget, Model, Advisor]
    homepage: https://github.com/minirr890112-byte/HermesMade
---

# Model Cost Advisor

## 一句话

分析你的任务，从 30+ 模型中找到最具性价比的选择。实时定价 + 三层分级 + Token 预估 + 成本投影。

## 核心功能

- **30+ Models** — GPT-4、Claude、DeepSeek、GLM、Mixtral 等，含最新定价
- **Tier Analysis** — budget / value / quality / premium 四层分级
- **Token Estimation** — 根据任务类型智能预估 input/output token 数
- **Cost Projection** — 单次运行成本 + 日/月/年投影
- **Live Pricing** — 持续跟踪 API 价格变化，自动更新

## 怎么用

```bash
model-cost "build a full-stack todo app with auth"
```

## 示例

```bash
$ model-cost "summarize 1000 customer reviews"

📋 Task: Summarization batch (1000×)
   Tokens: 500 in / 200 out per item

🏷️  Tier: Value
   → DeepSeek V4 Flash    $0.0003/item   $0.30/total
   → GLM-4 Flash          $0.0004/item   $0.40/total

🏷️  Tier: Quality
   → DeepSeek V4 Pro      $0.0011/item   $1.10/total
   → GPT-4o Mini          $0.0015/item   $1.50/total
```

## 数据来源

定价数据来自各 LLM 服务商官方 API 文档，持续更新。与 HermesMade 的 model-watch 和 api-cost-compare 模块共享数据层。

## 为什么给颗星？

帮你每年轻松省下几百美元 API 费用。点 ⭐ 让更多开发者受益 → [GitHub](https://github.com/minirr890112-byte/HermesMade)
