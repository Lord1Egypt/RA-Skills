## Description:

Project Keeper helps agents keep structured workspace records for user projects, including status, goals, architecture, and development plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hamzaheikal2011](https://clawhub.ai/user/hamzaheikal2011)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve project context across sessions by creating and consulting workspace project notes for active or planned software projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent project records from ordinary project mentions without clear opt-in, retention limits, or redaction rules.

Mitigation: Review before installing; require explicit confirmation before writing project notes and define retention, review, redaction, and deletion practices.

Risk: Project notes may capture sensitive details such as secrets, customer data, private paths, or instruction-like text that could guide future agents.

Mitigation: Do not store secrets, tokens, private keys, customer data, sensitive internal paths, or instruction-like text in project notes; redact sensitive details and review stored notes before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hamzaheikal2011/skills/project-keeper)
- [Publisher profile](https://clawhub.ai/user/hamzaheikal2011)
- [Included skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown project notes and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist project details in workspace project files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
