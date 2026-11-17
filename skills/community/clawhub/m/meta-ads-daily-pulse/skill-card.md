## Description:

Meta Ads Daily Pulse performs a daily Meta Ads monitoring scan that compares yesterday's performance with the same day of the prior week and ranks urgent change alerts by revenue impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and paid media operators use this skill before daily review meetings to detect meaningful Meta Ads changes, including week-over-week drops, spend without conversions, budget-cap opportunities, and creative fatigue. It is a detection workflow rather than a full diagnostic or recommendation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example Meta Graph API calls place the access token in the URL query string, which may expose credentials through logs or diagnostics.

Mitigation: Use a least-privilege, read-only Meta token, avoid shell tracing or verbose logs, and prefer sending the token with an Authorization header or credential-aware SDK.

## Reference(s):

- [Meta Ads Daily Pulse on ClawHub](https://clawhub.ai/elias-didoo/skills/meta-ads-daily-pulse)
- [Didoo AI Blog](https://didoo.ai/blog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown alert report with supporting curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; alert sections should include specific campaign or ad IDs and metrics, with no more than three items per section.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
