## Description:

Use when diagnosing, repairing, or maintaining an OpenClaw Gateway on the same machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinstein](https://clawhub.ai/user/dinstein)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and rescue agents use this skill to diagnose a down OpenClaw Gateway, repair configuration or dependency issues, restart the service safely, and perform routine health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad repair authority over OpenClaw Gateway configuration, service state, sessions, and workspace data.

Mitigation: Install it only on a trusted rescue agent account that is intended to administer the OpenClaw Gateway.

Risk: Backup procedures can copy OpenClaw tokens, sessions, and workspace data into plaintext backups.

Mitigation: Restrict backup permissions, avoid copying token files unless necessary, and clean up or encrypt backups.

Risk: Upgrade procedures that use registry-selected global updates can introduce unreviewed package changes.

Mitigation: Prefer pinned, verified OpenClaw package versions before running global update or rollback procedures.

## Reference(s):

- [OpenClaw Ops on ClawHub](https://clawhub.ai/dinstein/skills/openclaw-ops)
- [OpenClaw](https://openclaw.ai)
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-by-step operational guidance; destructive actions require user confirmation.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
