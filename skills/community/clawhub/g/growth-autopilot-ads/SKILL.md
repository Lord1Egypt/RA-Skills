---
name: growth-autopilot-ads
description: Automate full-funnel strategy generation, budget structure design, and dynamic bid/scale adjustments for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic campaigns.
---

# Growth Autopilot

## Purpose
Core mission:
- Auto-generate full paid growth strategy from goals.
- Auto-design budget and account structure.
- Dynamically adjust bids and scale pace by performance signals.
- Keep growth stable with guardrails and anomaly recovery rules.

## When To Trigger
Use this skill when the user asks for:
- automated growth strategy orchestration
- auto budget split and dynamic optimization
- autopilot decision loops for bidding and scaling
- continuous monitoring and adjustment policies

High-signal keywords:
- autopilot, automation, growth ai, growthbot
- budget, bidding, allocation, optimize, scale
- roas, cpa, revenue, performance, campaign

## Input Contract
Required:
- north_star_goal
- budget_constraints
- platform_scope
- control_limits (max drawdown, min roas, etc.)

Optional:
- warm_start_data
- creative_inventory_state
- seasonality_rules
- escalation_contacts

## Output Contract
1. Autopilot Strategy Blueprint
2. Budget and Structure Policy
3. Dynamic Bid/Scale Rules
4. Safety Guardrails and Kill-switches
5. Monitoring and Escalation Workflow

## Workflow
1. Convert business goal to machine-actionable policy set.
2. Initialize budget and structure by channel role.
3. Apply adaptive bid and scale rules by KPI trend.
4. Enforce guardrails and automatic rollback logic.
5. Emit periodic optimization reports and next actions.

## Decision Rules
- If KPI drift exceeds tolerance, shift into conservative mode.
- If confidence is low, reduce automation aggressiveness.
- If anomaly severity is high, trigger partial or full freeze.
- If recovery is confirmed, resume staged scale progression.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic

Platform behavior guidance:
- Autopilot rules should be channel-specific but policy-governed centrally.
- Keep bid logic aligned with platform optimization objective.

## Constraints And Guardrails
- Do not auto-approve risky policy-sensitive creative changes.
- Keep manual override path always available.
- Every auto action must map to an auditable rule.

## Failure Handling And Escalation
- If critical metrics are delayed, pause automated changes.
- If policy rejection rate spikes, route to human review queue.
- If data quality degrades, switch to monitoring-only mode.

## Code Examples
### Autopilot Policy YAML

    objective: maximize_revenue_with_roas_floor
    roas_floor: 2.3
    cpa_ceiling: 38
    budget_step_pct: 12
    rollback_trigger:
      roas_drop_pct: 18
      window_days: 3

### Decision Loop Pseudocode

    if roas >= roas_floor and cpa <= cpa_ceiling:
      increase_budget(step_pct)
    elif roas < roas_floor:
      decrease_budget(step_pct)
      tighten_bids()

## Examples
### Example 1: Autopilot bootstrap
Input:
- New account with limited baseline

Output focus:
- starter policy set
- safe exploration bounds
- monitoring cadence

### Example 2: Dynamic scale mode
Input:
- KPI stable for 3 weeks

Output focus:
- scale ladder
- bid adaptation rules
- rollback plan

### Example 3: Emergency stabilization
Input:
- ROAS crash + spend spike

Output focus:
- freeze/rollback action
- root-cause checklist
- re-entry conditions

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
