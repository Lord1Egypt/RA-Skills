## Description:

Automatically manages OpenClaw memory files across working, short-term, and long-term tiers, including cleanup, tier movement, archiving, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyblhl](https://clawhub.ai/user/wyblhl)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to organize local memory records, rotate older files into longer-term tiers, and generate basic memory reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently delete conversation records and move memory-tier files.

Mitigation: Review the configured memory paths before execution, keep independent backups, and test on noncritical memory data first.

Risk: The documented backup and confirmation protections are not fully implemented.

Mitigation: Do not rely on the stated safety protections as automatic safeguards; require manual review before cleanup operations.

## Reference(s):

- [Memory Manager on ClawHub](https://clawhub.ai/wyblhl/skills/memory-manager-wyblhl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file-management actions and console/log output when executed.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
