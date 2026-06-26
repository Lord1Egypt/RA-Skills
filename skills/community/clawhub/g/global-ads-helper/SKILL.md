---
name: global-ads-helper
description: Plan global paid growth across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic by comparing country cost, competition intensity, budget synergy, and expansion ROI.
---

# Global Ads Helper

## Purpose
Core mission:
- Analyze market-level traffic cost and competition intensity by country.
- Design cross-channel budget allocation and coordination strategy.
- Forecast expansion ROI across markets.
- Generate global rollout recommendation and risk controls.

## When To Trigger
Use this skill when the user asks for:
- multi-country growth strategy
- global channel budget allocation
- market expansion ROI prediction
- international ads rollout plan

High-signal keywords:
- global ads, market, cost, competition
- allocation, budget, forecast, roi, roas
- scale, strategy, revenue, expansion

## Input Contract
Required:
- target_markets
- expansion_objective
- total_budget
- baseline_market_performance

Optional:
- localization_resources
- compliance_constraints_by_country
- logistics_constraints
- currency_risk_assumptions

## Output Contract
1. Market Attractiveness Matrix
2. Channel Allocation by Market
3. Expansion ROI Forecast
4. Rollout Sequence and Dependencies
5. Market Risk Alert List

## Workflow
1. Rank markets by cost, competition, and conversion potential.
2. Assign channel roles per market maturity.
3. Simulate budget scenarios for each rollout stage.
4. Forecast ROI and payback by region.
5. Output phased expansion plan with risk triggers.

## Decision Rules
- If market CAC is high and data depth is low, start with discovery budget only.
- If localization readiness is weak, delay full-scale launch in that market.
- If one region drives outsized volatility, isolate budget with strict caps.
- If currency risk is elevated, widen ROI confidence intervals.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, DSP/programmatic

Platform behavior guidance:
- Use market-specific channel order; avoid global one-size plans.
- Match creative localization depth to market entry stage.

## Constraints And Guardrails
- Do not compare markets without consistent attribution definitions.
- Keep regional assumptions explicit and revisable.
- Flag legal/policy differences per country before launch.

## Failure Handling And Escalation
- If country-level data is sparse, output exploratory plan with validation milestones.
- If compliance blockers exist, mark blocked markets and reroute budget.
- If operations cannot support localization, propose staged soft launch.

## Code Examples
### Market Scoring Table

    market: DE
    cpc_index: 1.2
    competition_score: 0.74
    conversion_score: 0.63
    priority: medium

### Expansion Allocation (JSON)

    {
      "phase_1": {"US": 0.45, "UK": 0.30, "AU": 0.25},
      "phase_2": {"DE": 0.20, "FR": 0.20, "JP": 0.10}
    }

## Examples
### Example 1: Initial global rollout
Input:
- Launch in 3 English-speaking markets

Output focus:
- market ranking
- channel-by-market plan
- phase-1 risk controls

### Example 2: Add APAC market
Input:
- Existing US/EU campaigns stable
- Wants APAC expansion

Output focus:
- market attractiveness score
- budget impact simulation
- localization requirements

### Example 3: Global budget shock
Input:
- Budget cut by 25% mid-quarter

Output focus:
- market reprioritization
- protection strategy
- revised ROI forecast

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
