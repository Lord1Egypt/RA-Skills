## Description:

Provides public artist, track, album, playlist, and music-chart data across Spotify, Apple Music, SoundCloud, and TikTok through ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Artists, A&R teams, playlist curators, and music researchers use this skill to compare public music metrics and monitor emerging tracks and chart trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and pairing the third-party ClawLink plugin connects an external service to the user's agent.

Mitigation: Review the plugin and approve pairing before use.

Risk: Data lookups spend ClawLink credit, especially when repeated at scale.

Mitigation: Check current per-call prices and obtain approval before costly calls or broad batches.

Risk: The skill is intended only for public music-platform data.

Mitigation: Do not use it for private account information or actions that change platform data.

## Reference(s):

- [Music Intel on ClawHub](https://clawhub.ai/hith3sh/skills/music-intel)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=music-intel)
- [Verify the ClawLink plugin](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-language answers in chat]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes public music data returned by paid ClawLink lookups.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
