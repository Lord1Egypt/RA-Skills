## Description:

Marketing strategy simulation with multi-agent analysis for evaluating strategies, product launches, campaigns, and consumer, expert, and marketer perspectives on marketing decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorongss](https://clawhub.ai/user/dorongss)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, product owners, and founders use this skill to simulate Korean-language reactions to a marketing scenario before committing to product-launch, campaign, or page-optimization decisions. It coordinates scenario framing, consumer personas, marketing analysis, and expert review into a scored report with action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs are hardcoded to Korean and may not fit non-Korean workflows.

Mitigation: Confirm language expectations before use or adapt the prompts before deployment.

Risk: The workflow may run five sequential analysis agents, increasing latency and token cost.

Mitigation: Budget for longer execution and review whether all five perspectives are needed for the scenario.

Risk: Marketing scores and recommendations are simulated perspectives, not market validation.

Mitigation: Use the report as ideation input and validate decisions with customer, campaign, and business data.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Korean Markdown report with scores, insights, risks, and prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses five sequential analysis perspectives; outputs are hardcoded to Korean.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
