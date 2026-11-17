## Description:

Fast on-demand Meta Ads campaign status check that answers whether ads are working using Green, Yellow, and Red thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill for a quick, on-demand Meta Ads campaign health check before a meeting or when performance feels off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires credentials that let an agent read the specified Meta Ads account's campaign and ad set performance data.

Mitigation: Use a token limited to ads_read where possible and invoke the skill explicitly when an ads health check is intended.

Risk: The skill provides a quick threshold-based status check rather than a full diagnostic or optimization plan.

Mitigation: Treat Yellow or Red findings as triage signals and escalate to a deeper ads analysis or recommendation skill before changing campaigns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elias-didoo/skills/meta-ads-healthcheck)
- [Didoo AI blog](https://didoo.ai/blog)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown campaign-by-campaign status report with Green, Yellow, and Red statuses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses META_ACCESS_TOKEN and META_AD_ACCOUNT_ID to read Meta Ads campaign and ad set performance data.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
