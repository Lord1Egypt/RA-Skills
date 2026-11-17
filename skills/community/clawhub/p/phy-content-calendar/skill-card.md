## Description:

Phy Content Calendar generates 2-4 week social media posting calendars from topic pillars and a target platform, with rotating content styles, platform-specific scheduling, and optional content-library atom hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, founders, marketers, and developer advocates use this skill to plan platform-specific social media calendars from topic pillars. It helps agents produce posting schedules, draft outlines, and optional links to local content atoms for LinkedIn, Reddit, Twitter/X, and Hacker News workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --library mode can execute local Python code from predictable user-writable phy-content-compound paths without verification.

Mitigation: Use --library only when the local phy-content-compound file and its directory are trusted and have not been modified by another package or user.

Risk: Generated calendars and draft outlines may not match current platform rules, audience expectations, or brand policy.

Mitigation: Review scheduled posts and outlines before publishing, especially for regulated topics or brand-sensitive channels.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-content-calendar)
- [Publisher profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain text calendar, Markdown table, or JSON entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs scheduled post entries with date, weekday, platform, content style, topic pillar, outline, and optional local content atom hints.]

## Skill Version(s):

1.0.3 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
