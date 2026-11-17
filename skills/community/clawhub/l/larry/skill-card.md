## Description:

Automate TikTok slideshow marketing for any app or product by researching competitors, generating AI images, adding text overlays, posting via Postiz, tracking analytics, and iterating on what works.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olliewazza](https://clawhub.ai/user/olliewazza)

### License/Terms of Use:


## Use Case:

External developers, app builders, and growth teams use this skill to build and run a TikTok slideshow marketing workflow for apps or products. It guides competitor research, campaign setup, content generation, posting, analytics review, and iteration using social and conversion data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use powerful social-posting and analytics credentials stored in local configuration.

Mitigation: Use least-privilege API keys, prefer environment variables or a secret manager, and avoid committing tiktok-marketing/config.json or generated snapshots.

Risk: Recurring automation can post, analyze, or change campaign state without close human supervision.

Mitigation: Review any cron job before enabling it and keep posting workflows in a draft or manually reviewed state where supported.

Risk: Postiz-to-TikTok release-ID mappings can be hard to reverse if the wrong video is connected.

Mitigation: Manually verify release-ID mappings and wait for TikTok indexing before running commands that connect analytics records.

## Reference(s):

- [Analytics & Feedback Loop](references/analytics-loop.md)
- [App Category Templates](references/app-categories.md)
- [Competitor Research Guide](references/competitor-research.md)
- [RevenueCat Integration](references/revenuecat-integration.md)
- [Slide Structure & Hook Writing](references/slide-structure.md)
- [Postiz](https://postiz.pro/oliverhenry)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, and generated content artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local campaign configuration, research files, slide prompts, image assets, analytics reports, and posting commands when used by an agent.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
