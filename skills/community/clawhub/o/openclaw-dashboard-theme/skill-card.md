## Description:

Change OpenClaw Dashboard accent color with one sentence. Dynamically finds CSS/JS files and updates all accent CSS variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhaoxuan0](https://clawhub.ai/user/chenzhaoxuan0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to change the OpenClaw Dashboard accent color by providing a hex color or supported color name. The skill produces shell-command guidance for updating installed Dashboard CSS variables and JavaScript accent colors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites installed OpenClaw Dashboard CSS and JavaScript assets in place without creating backups.

Mitigation: Back up the OpenClaw installation or be prepared to reinstall or update OpenClaw before running the skill.

Risk: An unintended or unreviewed color value could change the dashboard appearance across themes.

Mitigation: Run the skill only for explicit dashboard theme changes and review the target #RRGGBB color before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenzhaoxuan0/skills/openclaw-dashboard-theme)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a single target hex color or supported color name; validates #RRGGBB input before editing OpenClaw Dashboard assets.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
