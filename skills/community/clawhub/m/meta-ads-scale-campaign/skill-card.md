## Description:

[Didoo AI] Guides Meta Ads campaign scaling - increases budget, expands audiences, replicates to new geos for campaigns that have exited Learning Phase and have stable cost metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and operators use this skill to decide whether a Meta Ads testing campaign is ready to scale, then choose budget, audience, or geography scaling actions and monitor post-scale performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meta credentials could expose ad account data if the token is broader than the advertised read-only ads scope.

Mitigation: Use a Meta token limited to ads_read and only provide the required ad account identifier.

Risk: Scaling recommendations can still lead to ad spend changes or campaign activation decisions even though the artifact does not automate them.

Mitigation: Review proposed budget, audience, and geo changes in Meta Ads Manager before activation and monitor CPL, frequency, spend, and learning status after scaling.

## Reference(s):

- [Didoo AI Blog](https://didoo.ai/blog)
- [ClawHub skill page](https://clawhub.ai/elias-didoo/skills/meta-ads-scale-campaign)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance with decision criteria, scaling steps, monitoring signals, and troubleshooting reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID when the agent checks Meta Ads status or insights; guidance is read-only and does not automate budget or campaign activation changes.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
