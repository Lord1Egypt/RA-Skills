## Description:

OpenClaw Update helps users assess and execute OpenClaw version upgrades by checking access, release information, issues, backups, update methods, gateway restart, and recovery options in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davis1216](https://clawhub.ai/user/davis1216)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to decide whether an OpenClaw installation should be updated, review release and issue signals, create backups, run the appropriate update path, restart the gateway, and recover from backups when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the local OpenClaw runtime, restart services, copy credentials and workspace data, and restore backups.

Mitigation: Prefer assessment-only use until the user explicitly approves updates, restores, restarts, or scheduling, and create a separate trusted backup before changes.

Risk: The security evidence flags unsafe mutable install or update paths, including curl-to-bash and an unpinned GitHub dependency.

Mitigation: Avoid those paths unless independently verified, and prefer trusted, pinned installation and update sources.

Risk: Optional scheduled checks add persistent automated behavior on the user's system.

Mitigation: Enable scheduling only with explicit consent after reviewing the command, schedule, and report location.

## Reference(s):

- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [OpenClaw releases](https://github.com/openclaw/openclaw/releases)
- [OpenClaw issues](https://github.com/openclaw/openclaw/issues)
- [Example assessment report](references/example-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown assessment reports with inline shell commands and bilingual status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce backup, recovery, update, restart, and scheduled-check instructions after user approval.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
