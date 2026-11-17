## Description:

[Didoo AI] Generates a structured weekly performance report for Meta Ads accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, operators, and agents use this skill to generate an end-of-week Meta Ads performance report for a specified ad account, compare current and prior-week metrics, explain changes, and flag issues that need attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent receives read-only access to the specified Meta Ads account's performance data.

Mitigation: Use a token limited to ads_read and the intended ad account, and avoid granting write scopes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elias-didoo/skills/meta-ads-weekly-performance)
- [Didoo blog](https://didoo.ai/blog)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with KPI tables and concise bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; intended for read-only Meta Ads reporting with ads_read scope.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
