---
name: growth-hub
description: Top-level orchestration skill that manages ads operations and enterprise growth decisions across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic.
---

# Growth Hub

## Purpose
Core mission:
- Act as the top-level orchestration layer for the Growth Hub system.
- Parse user intent and route to the right execution or decision path.
- Coordinate ads operations and enterprise growth workflows in one place.
- Keep outputs consistent with platform strategy and operating constraints.

## When To Trigger
Use this skill when the user asks for:
- end-to-end planning that spans ads execution and business growth decisions
- a unified control-plane recommendation instead of a single specialist task
- cross-functional coordination among marketing, finance, and growth teams
- platform-level system behavior and operating rules

High-signal keywords:
- growth hub, growth, strategy, report, dashboard
- ads, advertising, campaign, performance, optimize
- revenue, profit, budget, allocation, forecast

## Input Contract
Required:
- business_goal_bundle: revenue, profit, cashflow, and growth targets
- operating_scope: markets, channels, teams, and timeline
- decision_priority: speed, efficiency, scale, or risk control

Optional:
- platform_constraints
- capital_constraints
- existing_operating_playbook
- governance_policies

## Output Contract
1. Unified Intent Map
2. Orchestration Plan (which helper/skill does what)
3. Cross-functional KPI Tree
4. Execution and Decision Timeline
5. Governance and Escalation Matrix

## Workflow
1. Parse the request into execution and decision components.
2. Route execution tasks to ads-specific paths and growth tasks to decision paths.
3. Build shared KPI tree across teams.
4. Sequence actions and dependencies.
5. Output control-plane instructions and ownership.

## Decision Rules
- If request spans multiple domains, prioritize dependency-safe sequencing.
- If KPI conflict exists, surface trade-off before final recommendation.
- If governance constraints are missing, apply conservative defaults.
- If decision impact is high, require explicit review gates.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic

Platform behavior guidance:
- Use specialist skills for channel-level execution details.
- Keep Growth Hub output at orchestration level unless deep-dive is explicitly requested.

## Constraints And Guardrails
- Do not bypass governance for speed.
- Keep ownership and accountability explicit in every plan.
- Separate policy from recommendation.

## Failure Handling And Escalation
- If request is ambiguous, ask only for missing high-impact fields.
- If cross-team dependencies are unclear, return dependency map before execution plan.
- If risk exceeds threshold, escalate to Growth Strategy Hub decision flow.

## Code Examples
### Orchestration Payload (JSON)

    {
      "orchestrator": "growth-hub",
      "execution_path": ["ads-execution-hub", "shopify-ads-helper"],
      "decision_path": ["growth-strategy-hub"],
      "governance_level": "standard"
    }

### KPI Tree Spec (YAML)

    north_star: contribution_profit
    children:
      - revenue
      - blended_roas
      - cashflow_stability
      - customer_ltv

## Examples
### Example 1: Unified quarterly plan
Input:
- Need one plan for ads + enterprise growth

Output focus:
- orchestration map
- ownership matrix
- phased timeline

### Example 2: Multi-team execution conflict
Input:
- Marketing wants scale, finance wants cash preservation

Output focus:
- conflict resolution logic
- KPI trade-off framework
- staged plan

### Example 3: Platform expansion + governance
Input:
- Add two channels while maintaining controls

Output focus:
- control-plane routing
- governance gates
- escalation paths

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
