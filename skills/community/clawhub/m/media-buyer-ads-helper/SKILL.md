---
name: media-buyer-ads-helper
description: Support media buying execution for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic with account health checks, bidding efficiency analysis, AB test design, and real-time anomaly monitoring.
---

# Media Buyer Helper

## Purpose
Core mission:
- Evaluate account health and structure quality.
- Analyze bid logic and budget allocation efficiency.
- Design AB test architecture and scale model.
- Monitor campaigns in real time and detect anomalies.

## When To Trigger
Use this skill when the user asks for:
- media buyer execution support
- bid and budget efficiency diagnostics
- AB testing structure design
- live campaign watch and anomaly alerts

High-signal keywords:
- media, bidding, budget, auction, allocation
- abtest, campaign, performance, optimize
- cpa, roas, scale, monitor

## Input Contract
Required:
- account_structure_snapshot
- bidding_config
- budget_allocation_snapshot
- recent_performance_series

Optional:
- test_history
- alert_thresholds
- creative_breakdowns
- seasonality_notes

## Output Contract
1. Account Health and Structure Score
2. Bid and Budget Efficiency Findings
3. AB Test Structure Blueprint
4. Scale Model with Trigger Conditions
5. Monitoring and Alert Rules

## Workflow
1. Check account hierarchy and naming hygiene.
2. Evaluate bid strategy vs KPI objective.
3. Diagnose budget fragmentation and overlap.
4. Build AB test matrix with clear success metrics.
5. Define anomaly thresholds and response playbook.

## Decision Rules
- If structure complexity is high and spend is low, simplify before adding tests.
- If CPA variance is high, reduce concurrent experiments.
- If winning cells are statistically weak, extend learning window.
- If anomaly severity is high, prioritize containment over optimization.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, DSP/programmatic

Platform behavior guidance:
- Map bid logic to channel auction mechanics.
- Keep test isolation strict to avoid cross-cell contamination.

## Constraints And Guardrails
- Do not claim statistical significance without threshold checks.
- Avoid broad budget jumps without gate conditions.
- Keep alert rules tied to action ownership.

## Failure Handling And Escalation
- If data granularity is insufficient, request minimum breakdowns.
- If live anomaly cannot be diagnosed, escalate with incident payload.
- If policy rejects disrupt test integrity, pause affected cells and reroute budget.

## Code Examples
### AB Test Matrix

    test_id: AB-2026-07
    variable: bid_strategy
    cells:
      - control: target_cpa
      - challenger: max_conversion_value
    success_metric: blended_roas

### Anomaly Rule

    if spend_spike_pct > 35 and conversions_drop_pct > 25:
      severity: high
      action: notify_and_limit_budget

## Examples
### Example 1: Bid efficiency issue
Input:
- CPC up, CVR flat

Output focus:
- bid logic fix
- budget reallocation
- test plan

### Example 2: AB test setup
Input:
- Need test for broad vs layered audience

Output focus:
- clean test architecture
- significance rule
- rollout timeline

### Example 3: Real-time anomaly
Input:
- Sudden spend spike in one channel

Output focus:
- anomaly diagnosis
- immediate actions
- escalation path

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
