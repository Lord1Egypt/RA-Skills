## Description:

[Didoo AI] Analyzes creative fatigue signals across Meta Ads campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams and advertising operators use this skill to analyze Meta Ads creative fatigue, identify declining CTR or ROAS, and plan creative refresh timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect active Meta Ads performance across the configured account when campaign_id or ad_ids are not provided.

Mitigation: Use campaign_id or ad_ids for narrower analysis when account-wide review is not intended.

Risk: The skill requires read-only Meta Ads credentials and account identifiers.

Mitigation: Provide credentials with the documented ads_read scope only, and handle META_ACCESS_TOKEN and META_AD_ACCOUNT_ID as sensitive configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elias-didoo/skills/meta-ads-creative-fatigue)
- [Didoo AI blog](https://didoo.ai/blog)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis tables with concise recommendation guidance and session context values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fatigue status, frequency decay, ROAS degradation, rotation pipeline, and refresh recommendation sections; no executive summary.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
