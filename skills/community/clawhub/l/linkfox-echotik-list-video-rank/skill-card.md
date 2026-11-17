## Description:

Queries EchoTik TikTok Shop video rankings by date, period, region, and ranking metric to surface top videos with engagement, sales, and GMV metrics across 16 marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border sellers, marketers, and commerce analysts use this skill to find ranked TikTok Shop videos for a selected day, week, or month and compare video performance by views, sales, and estimated GMV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox API credentials and can guide account login flows that involve phone or SMS details.

Mitigation: Use a clean environment with trusted endpoint variables, review credential handling before installation, and avoid placing secrets in plaintext shell profile files when a safer secret store is available.

Risk: The skill includes billing and order flows for buying credits.

Mitigation: Only run payment-related commands when the user intentionally wants to purchase credits, and confirm the selected plan and payment method before continuing.

Risk: The skill saves full API responses to local workspace files.

Mitigation: Review where response files are stored, limit workspace access to trusted users, and remove saved outputs when they are no longer needed.

Risk: The skill can automatically report feedback when behavior or user sentiment indicates an issue.

Mitigation: Review the feedback behavior before deployment and avoid including sensitive user data in feedback context.

## Reference(s):

- [EchoTik-TikTok视频排行 API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-list-video-rank)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown summaries and tables with links, plus saved JSON response files and optional inline JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses to a local linkfox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
