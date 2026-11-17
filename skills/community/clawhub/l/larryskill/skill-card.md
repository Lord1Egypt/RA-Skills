## Description:

Automates TikTok slideshow marketing for apps and products by guiding competitor research, image generation, text overlays, Postiz posting, analytics tracking, and iterative content optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batsirai](https://clawhub.ai/user/batsirai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, app makers, and product teams use this skill to set up and operate a TikTok slideshow marketing workflow. It helps create content, post through Postiz, track engagement and optional RevenueCat conversions, and revise hooks and CTAs based on performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for persistent API-driven social posting and revenue analytics access.

Mitigation: Review before installing, use a separate working directory, and require explicit approval before browser research, Postiz posting, cross-posting, RevenueCat access, npm installation, sudo commands, or scheduled jobs.

Risk: Configuration and analytics files can contain API keys, social platform identifiers, revenue data, or transaction-derived timestamps.

Mitigation: Prefer environment variables or a secret manager, do not commit tiktok-marketing/config.json or analytics snapshots, rotate any key stored in a shared file, and set retention and deletion rules for reports and snapshots.

Risk: Automated posting and analytics matching can connect the wrong TikTok video ID after publication.

Mitigation: Wait for the TikTok indexing window described by the artifact, compare unconnected Postiz posts against new TikTok video IDs, and verify counts before connecting release IDs.

Risk: The artifact includes a Postiz signup URL that may be an author referral link.

Mitigation: Use a neutral Postiz signup URL when a referral relationship is not desired.

## Reference(s):

- [Analytics & Feedback Loop](references/analytics-loop.md)
- [App Category Templates](references/app-categories.md)
- [Competitor Research Guide](references/competitor-research.md)
- [RevenueCat Integration](references/revenuecat-integration.md)
- [Slide Structure & Hook Writing](references/slide-structure.md)
- [ClawHub Skill Page](https://clawhub.ai/batsirai/skills/larryskill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration files, shell commands, JavaScript helper scripts, generated image files, analytics snapshots, and daily report Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files under the user's TikTok marketing workspace and may call configured third-party APIs when the user supplies credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
