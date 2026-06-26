---
name: offer-profitability-checker
description: Check whether an ecommerce offer is commercially viable after discounts, costs, refunds, and traffic economics are included. Use when teams need a fast profitability reality check before launch or scale.
---

# Offer Profitability Checker

A quick commercial reality check for offers that look good on the surface but may not hold up economically.

## 先交互，再分析

开始时先问清楚：
1. 这次你想评估的 offer 是什么？
   - 直降
   - bundle
   - upsell
   - 满减
   - 包邮
2. 你们平时怎么判断一个 offer “可做”？
   - 看净利？
   - 看 contribution margin？
   - 看 CAC 容忍度？
3. 你希望沿用现有口径，还是让我给一套推荐的电商 profitability 框架？
4. 这次最关心的是：利润、放量空间、转化假设，还是风险边界？

如果用户没有明确口径，先给推荐分析框架，再让用户确认。

## Python script guidance

当用户提供结构化数字后：
- 生成 Python 脚本建模
- 先展示假设与公式
- 再输出 baseline / scenario / sensitivity
- 最后返回可复用脚本

如果关键数据缺失，不要直接假装精确；继续追问或给推荐默认值并等待确认。

## Solves

Many ecommerce teams make pricing or offer decisions with incomplete economics:
- they see revenue upside but not margin drag;
- they model one variable but ignore knock-on effects;
- they test offers without clear guardrails;
- they scale offers before checking break-even logic.

Goal:
**Turn offer assumptions into a clearer economic view that is easier to evaluate and act on.**

## Use when

- You want to compare offer scenarios before launching
- A discount, bundle, or upsell idea sounds good but needs economic validation
- Growth teams need a faster way to pressure-test merchandising decisions
- Teams want clearer go / watch / no-go logic before scale

## Inputs

- Core commercial assumptions relevant to the scenario
- Price and cost structure
- Margin or refund assumptions
- Traffic / conversion or attach-rate assumptions
- Constraints or guardrails

## Workflow

1. Clarify the baseline commercial setup and evaluation logic.
2. Model the scenario inputs that change order economics.
3. Surface upside, downside, and sensitivity.
4. Identify the biggest weak points or break-even pressure.
5. Recommend whether to test, revise, or avoid the scenario.
6. Return reusable Python script when structured inputs exist.

## Output

1. Baseline view
2. Scenario result
3. Margin / break-even implications
4. Key risks and weak points
5. Recommendation
6. Python script

## Quality bar

- Output should be commercially interpretable, not just a raw formula dump.
- Recommendations should stay grounded in ecommerce economics.
- Weak points should be clearly separated from upside assumptions.
- The result should help a team decide what to test next.
- Do not pretend precision before assumptions are confirmed.

## Resource

See `references/output-template.md`.
