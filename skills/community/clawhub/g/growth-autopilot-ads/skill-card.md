## Description:

Automate full-funnel strategy generation, budget structure design, and dynamic bid/scale adjustments for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

Growth marketers, performance media operators, and developers use this skill to draft paid-media automation policies for budget allocation, bid and scale adjustments, guardrails, rollback rules, and monitoring workflows across major ad platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide automated ad budget and bidding changes without a clear human approval gate.

Mitigation: Keep outputs advisory or monitoring-only unless explicit human approval, budget caps, rollback limits, audit logging, and platform-specific execution permissions are enforced outside the skill.

Risk: Incorrect performance signals or delayed metrics could lead to harmful optimization recommendations.

Mitigation: Pause automated changes when critical metrics are delayed or data quality degrades, and require human review before resuming execution.

Risk: Policy-sensitive creative or campaign changes could be approved too aggressively.

Mitigation: Do not auto-approve policy-sensitive creative changes; route policy rejection spikes and high-severity anomalies to a human review queue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/skills/growth-autopilot-ads)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Code]

**Output Format:** [Markdown with policy YAML and pseudocode examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces strategy blueprints, budget and structure policies, dynamic bid/scale rules, safety guardrails, kill-switches, and monitoring workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
