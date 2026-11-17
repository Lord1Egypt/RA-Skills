## Description:

Analyzes TikTok creators, TikTok Shop commerce, content, live streams, trends, ads, products, shops, categories, videos, hashtags, music, comments, and audience signals through the KeyAPI REST API using live official docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and commerce teams use this skill to turn TikTok research questions into documentation-guided KeyAPI workflows for creator discovery, product and seller research, content intelligence, live commerce, trend monitoring, and multi-endpoint reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can store a KeyAPI token persistently in plaintext shell profile files.

Mitigation: Prefer a temporary shell-scoped KEYAPI_TOKEN or a secure credential store; rotate any token saved in a shared or backed-up shell profile.

Risk: TikTok queries, uploaded images or request bodies, and retrieved results may be sent to KeyAPI during live workflows.

Mitigation: Use the skill only for data that may be shared with KeyAPI, and avoid sending unnecessary personal, confidential, or sensitive business information.

Risk: Follower, following, audience-region, comment, and download workflows can expose sensitive social graph or content data.

Mitigation: Limit scope to the minimum needed, review outputs before redistribution, and apply the user's privacy and compliance requirements before using or sharing results.

## Reference(s):

- [Global Rules](references/global-rules.md)
- [Scenario Cards](references/scenarios.md)
- [Routing Policy](references/routing-policy.md)
- [Setup And Auth](references/setup-and-auth.md)
- [TikTok Rules](references/tiktok-rules.md)
- [TikTok Influencer Module Rules](references/tiktok-influencer-rules.md)
- [TikTok Shop Composite Rules](references/tiktok-shop-rules.md)
- [TikTok Content Composite Rules](references/tiktok-content-rules.md)
- [TikTok Intelligence Module Rules](references/tiktok-intelligence-rules.md)
- [KeyAPI LLM Docs Index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI Bearer Authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown answers with inline shell commands and optional JSON summaries from KeyAPI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute live KeyAPI REST calls when credentials are configured; large responses can be saved to files on request.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
