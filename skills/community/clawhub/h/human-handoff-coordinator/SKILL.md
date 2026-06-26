---
name: human-handoff-coordinator
description: Escalate automation conversations to human ad experts for Meta (Facebook/Instagram), Google Ads, TikTok Ads, and YouTube Ads operations.
---

# Ads Human Handoff

## Purpose
Core mission:
- handoff packet creation, escalation routing

This skill is specialized for advertising workflows and should output actionable plans rather than generic advice.

## When To Trigger
Use this skill when the user asks for:
- ad execution guidance tied to business outcomes
- growth decisions involving revenue, roas, cpa, or budget efficiency
- platform-level actions for: Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads
- this specific capability: handoff packet creation, escalation routing

High-signal keywords:
- ads, advertising, campaign, growth, revenue, profit
- roas, cpa, roi, budget, bidding, traffic, conversion, funnel
- meta, googleads, tiktokads, youtubeads, amazonads, shopifyads, dsp

## Input Contract
Required:
- question: user issue or decision request
- context: account, campaign, and objective context
- urgency_level

Optional:
- error_message
- screenshots_or_logs
- preferred_response_style

## Output Contract
1. Direct Answer
2. Root Cause Hypothesis
3. Immediate Actions
4. Escalation Criteria
5. Follow-up Questions

## Workflow
1. Classify question type (how-to, diagnosis, policy, strategy).
2. Provide shortest valid answer first.
3. Add context-aware action checklist.
4. Flag escalation if risk or uncertainty is high.
5. Return follow-up fields only if required.

## Decision Rules
- If answer confidence is low, state uncertainty and propose verification steps.
- If issue impacts spend safety, prioritize pause or cap recommendations.
- If user asks unsupported action, hand off with exact context package.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads

Platform behavior guidance:
- Keep recommendations channel-aware; do not collapse all channels into one generic plan.
- For Meta and TikTok Ads, prioritize creative testing cadence.
- For Google Ads and Amazon Ads, prioritize demand-capture and query/listing intent.
- For DSP/programmatic, prioritize audience control and frequency governance.

## Constraints And Guardrails
- Never fabricate metrics or policy outcomes.
- Separate observed facts from assumptions.
- Use measurable language for each proposed action.
- Include at least one rollback or stop-loss condition when spend risk exists.

## Failure Handling And Escalation
- If critical inputs are missing, ask for only the minimum required fields.
- If platform constraints conflict, show trade-offs and a safe default.
- If confidence is low, mark it explicitly and provide a validation checklist.
- If high-risk issues appear (policy, billing, tracking breakage), escalate with a structured handoff payload.

## Code Examples
### Quick Triage JSON

    {
      "issue_type": "delivery_drop",
      "severity": "medium",
      "first_actions": ["check spend cap", "check policy status"]
    }

### Handoff Payload

    ticket_type: platform_support
    required_fields: [account_id, campaign_id, timeline, last_change]

## Examples
### Example 1: Delivery suddenly dropped
Input:
- Campaign impressions down 60%
- No recent manual changes

Output focus:
- probable causes
- first 3 checks
- escalation trigger

### Example 2: Policy rejection question
Input:
- Ad rejected with vague reason
- User wants fastest fix

Output focus:
- policy interpretation
- rewrite direction
- approval retry order

### Example 3: Need human support now
Input:
- Billing or account lock issue
- Launch deadline is today

Output focus:
- handoff packet
- urgency level
- required owner and ETA

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
