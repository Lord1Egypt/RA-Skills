## Description:

Content Creator Pro helps agents create social media posts, content calendars, captions, and repurposed platform-specific drafts using a saved brand voice profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, founders, and small teams use this skill to define a brand voice, plan weekly social calendars, generate posts for X, LinkedIn, Instagram, TikTok, and Facebook, repurpose ideas across platforms, and track content performance notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can trust a spoofed home-directory match for the skill package path before copying an executable script.

Mitigation: Set the skill package path manually to a reviewed Content Creator Pro directory before copying config or scripts, and inspect copied scripts before execution.

Risk: The active skill instructions include unrelated product cross-sells.

Mitigation: Remove or disable the Cross-Sells section when unsolicited product suggestions are not appropriate for the deployment.

Risk: The skill persists brand voice, drafts, calendars, ideas, engagement notes, and competitor notes in local JSON files.

Mitigation: Use a workspace with appropriate permissions, avoid entering social media credentials, and review generated content before posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-content-creator-pro)
- [README](artifact/README.md)
- [Security audit](artifact/SECURITY.md)
- [First-run setup guide](artifact/SETUP-PROMPT.md)
- [Content configuration](artifact/config/content-config.json)
- [Dashboard companion spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with platform-labeled drafts, JSON-backed local state, and optional CSV or Markdown calendar exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can maintain brand profiles, pillars, calendars, ideas, history, engagement notes, and competitor notes in local JSON files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
