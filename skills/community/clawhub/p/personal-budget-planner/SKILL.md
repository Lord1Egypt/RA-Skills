---
slug: personal-budget-planner
version: "1.2.0"
tags: personal-budget, financial-planning, budgeting-framework, expense-management, savings-plan
type: descriptive
language: en
---

# Personal Budget Planner

## Overview

Helps individuals create personalized budget frameworks based on income, expenses, savings goals, and debt priorities. This is a descriptive skill that provides templates, frameworks, and heuristic analysis without executing real code, accessing external APIs, or performing actual financial transactions.

## Trigger

Use this skill when the user wants to:
- get structured guidance on personal budget planner
- apply best-practice frameworks to their financial situation
- generate templates and checklists for financial planning

### Example prompts
- "Help me create a personal budget"
- "Analyze my cash flow forecast"
- "Check my expense categorization"
- "Assess my financial health"
- "Review my receivables aging"
- "Check invoice compliance"
- "Develop a pricing strategy"
- "Find cost reduction opportunities"
- "Optimize my tax deductions"
- "Interpret my financial reports"

## Workflow

1. User provides context and goals.
2. Skill applies built-in templates and frameworks.
3. Skill generates structured output with recommendations.
4. User receives actionable insights and next steps.

## Inputs
- User context (financial situation, goals, constraints)
- Optional data inputs (amounts, categories, timeframes)
- Analysis preferences

## Outputs
- Structured analysis report
- Templates and frameworks
- Actionable recommendations
- Next steps checklist

## Usage Scenarios

### Scenario 1

**User input:** "Create a zero-based monthly budget for a family of 4 with $8,500 net income in Austin."

**Expected output:** Zero-based budget allocating every dollar — housing $2,400, food $1,200, transportation $700, childcare $1,500, insurance $600, savings $1,300, discretionary $800 — with category rationale, local cost references, and buffer recommendations.

### Scenario 2

**User input:** "I'm a freelancer with variable income ($4K-$9K/month). What budgeting method works best?"

**Expected output:** Variable-income budgeting framework — baseline-budget on $4K minimum, tiered surplus allocation rules (% to tax reserve, emergency fund, investments, lifestyle), with feast-month/famine-month cash-flow smoothing strategy.

### Scenario 3

**User input:** "Help us combine finances after marriage. We have different spending styles."

**Expected output:** Joint budgeting framework with values-alignment exercise, 'yours/mine/ours' account structure recommendation, discretionary allowance method, monthly money-date agenda template, and conflict-resolution communication scripts.
### Scenario 4: 月薪8000在一线城市怎么活
**User input:** "刚毕业在上海找到工作月薪税前8000，房租2000，请问怎么规划预算才能不月光？"
**Expected output:** 提供适合一线城市新人的预算方案：收入到手约6500（扣除五险一金+个税）。按50/30/20法则分配：必要开支50% (3250元)——房租2000+餐饮800+交通200+话费网费150+日用品100；可选消费30% (1950元)——社交娱乐500+购物500+学习200+其他；储蓄20% (1300元)——建议设置自动转账到独立账户。关键建议：住在离公司30分钟地铁的合租房（不要省交通费换更远的便宜房子，通勤时间是用金钱买不回来的）。推荐使用鲨鱼记账记录每一笔支出。

## Safety
- No real financial transactions or API calls
- No access to real bank accounts or financial systems
- Recommendations are informational only
- Users should consult financial professionals for actual decisions

## Acceptance Criteria
- Must return structured markdown/JSON output
- Must include actionable recommendations
- Must clearly state the descriptive/non-executable nature
- Must provide templates or frameworks for user adaptation
