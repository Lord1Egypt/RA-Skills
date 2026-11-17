## Description:

Explains, validates, converts, and audits cron expressions across Unix, GitHub Actions, Kubernetes, AWS EventBridge, Spring, and related cron formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to translate cron expressions into plain English, validate schedules, calculate upcoming run times, convert simple English schedules to cron, and audit cron schedules in GitHub Actions, Kubernetes YAML, and crontab-style files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently install an unpinned Python package at runtime when croniter is unavailable.

Mitigation: Review before installation, especially for agents with network access or writable shared Python environments; prefer a release that declares and pins dependencies or fails with setup guidance instead of auto-installing packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-cron-explainer)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Canlah AI](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with cron expressions, validation findings, next-run times, code snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scan local project configuration files for cron schedules; no external API use is claimed, but security evidence reports possible runtime package installation.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
