## Description:

Check OpenClaw release notes from GitHub, show highlights and categorized changes translated to the user's language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjefferson](https://clawhub.ai/user/tjefferson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to check latest, recent, or specific OpenClaw releases, compare versions, and review categorized upgrade-relevant changes in their language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make GitHub API requests and use GITHUB_TOKEN when it is already set.

Mitigation: Use a low-privilege GitHub token and avoid asking it to process unrelated private repository data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjefferson/skills/openclaw-release-monitor)
- [OpenClaw latest release API](https://api.github.com/repos/openclaw/openclaw/releases/latest)
- [OpenClaw releases API](https://api.github.com/repos/openclaw/openclaw/releases?per_page=10)
- [OpenClaw release page example](https://github.com/openclaw/openclaw/releases/tag/v2026.3.31)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with headings, bullets, tables, release links, and optional shell commands for GitHub API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can translate release notes into the user's language, filter by topic, compare versions, and summarize recent release lists.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
