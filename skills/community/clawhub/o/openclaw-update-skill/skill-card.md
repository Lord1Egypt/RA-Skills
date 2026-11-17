## Description:

Check for OpenClaw updates, perform updates, and manage version status. Provides automatic update checking, version comparison, and seamless updating of the OpenClaw agent platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rothcold](https://clawhub.ai/user/rothcold)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check OpenClaw version status, apply pnpm-based updates, and restart or verify the OpenClaw gateway after maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global OpenClaw update commands can change the installed agent platform on the target machine.

Mitigation: Confirm the package source, current version, and target machine before running update commands, and keep a rollback path available.

Risk: Restarting the OpenClaw gateway can briefly interrupt service.

Mitigation: Plan the restart for an acceptable maintenance window and verify gateway status after the update.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rothcold/skills/openclaw-update-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw status, update, gateway restart, and optional environment variable guidance.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
