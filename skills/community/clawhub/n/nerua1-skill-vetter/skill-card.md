## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to review AI agent skills before installation, checking source trust, permissions, suspicious patterns, and install risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect candidate skill files and run GitHub lookup commands while reviewing third-party skills.

Mitigation: Review generated commands before execution, especially when assessing private repositories or sources that may expose sensitive metadata.

Risk: The skill's audit guidance can classify install risk, but it does not replace human approval for high-risk skills.

Mitigation: Require human review before installing skills that request credentials, broad filesystem access, elevated permissions, or access to sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerua1/skills/nerua1-skill-vetter)
- [Publisher profile](https://clawhub.ai/user/nerua1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown checklist and vetting report with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable risk classifications, verdicts, notes, and permission-scope summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
