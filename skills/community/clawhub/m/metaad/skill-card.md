## Description:

This skill automates the creation of Meta (Facebook/Instagram) ads using the Marketing API. It handles campaign setup, audience targeting, media upload, and ad creation in a streamlined workflow. Use this skill when users want to create Meta ads programmatically, manage ad campaigns via API, or automate their advertising workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zine1993](https://clawhub.ai/user/zine1993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and advertising teams use this skill to create Meta ads programmatically, including campaign setup, ad set targeting, media upload, creative construction, and ad creation through the Meta Marketing API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meta access token with permissions capable of managing ads.

Mitigation: Use a least-privilege token and install only when that access level is acceptable.

Risk: The skill stores Meta ad credentials in a plaintext local configuration file.

Mitigation: Avoid entering credentials while screen sharing or recording, do not provide the optional App Secret unless needed, and delete or protect ~/.workbuddy/meta_ads_config.json after use.

Risk: The skill can create campaigns, ad sets, creatives, and ads in a Meta ad account.

Mitigation: Keep generated ads paused by default and review all campaigns in Meta Ads Manager before activation.

## Reference(s):

- [Meta Marketing API Reference](artifact/references/meta_api.md)
- [Meta Marketing API Documentation](https://developers.facebook.com/docs/marketing-api/)
- [Meta Marketing API Limits](https://developers.facebook.com/docs/marketing-api/overview/limits)
- [Meta Audience Targeting Reference](https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to create or invoke scripts that configure Meta API credentials, upload media, and create paused Meta ad campaigns for review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
