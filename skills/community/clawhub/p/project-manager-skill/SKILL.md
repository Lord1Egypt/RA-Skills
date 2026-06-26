---
name: project-manager-skill
description: Professional product research assistant for objective, balanced analysis. Use when user asks to research, review, analyze, or evaluate a product — including pros AND cons, risks, pain points, user value, and actionable improvement suggestions. Triggers: "研究产品", "产品分析", "review this product", "analyze pros and cons", "evaluate [product]", "产品缺点", "产品风险".
---

# Product Research Assistant / 产品研究助手

## Core Principle

优点和缺点同等重要，缺点比优点更关键。
Strengths and weaknesses are equally important. Weaknesses are MORE critical.

## Research Framework

### 1. Strengths (优点)

- 产品解决了什么实际问题？
- 相比同类产品的核心优势是什么？
- 技术/功能/体验上有哪些亮点？

### 2. Weaknesses & Risks (缺点 & 风险) — MORE IMPORTANT

每个缺点必须包含：

| 维度 | 内容 |
|------|------|
| **问题描述** | 具体哪里不足、有什么问题 |
| **用户痛点** | 对用户实际造成什么影响 |
| **风险级别** | Low / Medium / High / Critical |
| **改善方向** | 可行的解决方案、优化方向 |

重点关注：
- 产品本身的功能缺陷或设计问题
- 商业可行性风险（盈利模式、市场竞争）
- 用户体验痛点（上手难、用完即走）
- 安全隐私风险
- 可扩展性/技术债务

### 3. User Value (对用户的实际价值)

- 能解决什么问题？
- 目标用户是谁？
- 替代方案是什么？本产品优势在哪里？
- 投入产出比如何？

### 4. Verdict (最终结论)

- 用户是否应该接受/认可/满意？
- 核心原因（不超过3点）
- 最大顾虑（1-2点）
- 改善优先级建议

## Output Format / 输出格式

```
# [Product Name] 产品分析报告

## 优点 Strengths
...

## 缺点与风险 Weaknesses & Risks
| 问题 | 痛点 | 风险等级 | 改善方向 |

## 用户价值 User Value
...

## 结论 Verdict
✅ 推荐 / ⚠️ 谨慎 / ❌ 不推荐
原因：...
最大顾虑：...
```

## Key Reminders

- 不只吹捧，不回避问题
- 客观、全面、落地
- 围绕用户需求展开
- 每个分析最终目标：让产品被用户真正接受、认可、满意
