## Description:

Predict repeat-customer churn risk from purchase history and tier activity, then output branch-specific win-back and activation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

Commerce and retention teams use this skill to identify silent or at-risk repeat customers, split them into VIP and standard segments, and plan win-back workflows across email, SMS, app push, or customer success outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request or operate on customer metrics such as purchase recency, loyalty tier, points expiry, and consent status.

Mitigation: Use appropriately scoped or anonymized customer data where possible, and verify consent and local marketing rules before applying campaign recommendations.

Risk: Vague business phrasing about falling repeat rates can lead to broad retention recommendations without enough cohort context.

Mitigation: Confirm the intended retention workflow and gather recency, frequency, value, tier, channel, and consent constraints before producing a full win-back plan.

## Reference(s):

- [LTV & loyalty win-back playbook](references/loyalty_playbook.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with risk summaries, segment branches, workflow tables, and campaign recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include channel timing, points-expiry sequences, success metrics, and consent-aware workflow notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
