## Description:

Didoo AI diagnoses sudden performance drops in Meta Ads campaigns when CTR, ROAS, or conversions decline without an obvious explanation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, marketers, and advertising operators use this skill to diagnose sudden Meta Ads campaign performance drops by comparing recent metrics, identifying likely root causes, and organizing next-step guidance for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meta token with ads_read access and Meta ad account performance data.

Mitigation: Confirm the required token scope and account data exposure before installation.

Risk: Recovery guidance may be mistaken for an approved automated action plan.

Mitigation: Review any recovery plan manually in Ads Manager before changing campaigns.

Risk: The skill documentation is inconsistent about whether recovery recommendations belong in this diagnosis skill or a separate recommendation skill.

Mitigation: Treat the output as diagnostic guidance and route detailed action planning to the appropriate recommendation workflow.

## Reference(s):

- [Didoo AI Blog](https://didoo.ai/blog)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic report with a performance snapshot table, root cause analysis, and recovery plan sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes session context keys primary_root_cause and recovery_plan.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
