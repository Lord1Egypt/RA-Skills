## Description:

Automates a TikTok and Instagram slideshow marketing workflow for apps or products by guiding competitor research, AI image generation, text overlays, multi-platform posting, analytics tracking, and iterative optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sammy-the-bot](https://clawhub.ai/user/sammy-the-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, app founders, and growth marketers use this skill to set up an agent-assisted social marketing pipeline that creates slideshow content, posts it through Upload-Post, and reviews performance data. It is especially oriented toward app marketing workflows that need repeatable hook testing, creative iteration, and optional conversion tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting credentials and platform API keys may be exposed or granted broader access than needed.

Mitigation: Use least-privilege API keys, prefer environment variables or a secret manager, and keep config.json and generated reports out of source control.

Risk: Social posting automation can publish public content or run recurring scheduled jobs without sufficient review.

Mitigation: Require explicit user confirmation before public posting and before enabling recurring scheduled jobs.

Risk: RevenueCat integration can expose subscriber, conversion, and revenue data.

Mitigation: Review RevenueCat access carefully and limit credentials to the required project and reporting scope.

Risk: Third-party dependency installation and API integrations can change behavior over time.

Mitigation: Review install commands before execution and pin dependencies where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sammy-the-bot/skills/larry-marketing)
- [Upload-Post](https://upload-post.com)
- [Analytics & Feedback Loop](references/analytics-loop.md)
- [App Category Templates](references/app-categories.md)
- [Competitor Research Guide](references/competitor-research.md)
- [RevenueCat Integration](references/revenuecat-integration.md)
- [Slide Structure & Hook Writing](references/slide-structure.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON configuration, JavaScript scripts, shell commands, generated image files, posting metadata, analytics snapshots, and daily reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local marketing workspace files and may call third-party posting, analytics, image generation, and conversion-tracking APIs when configured by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
