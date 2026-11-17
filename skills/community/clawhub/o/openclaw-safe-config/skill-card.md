## Description:

Use when editing openclaw.json, adding or changing config keys, troubleshooting a gateway crash after a config change, validating config before restart, or recovering from an unknown key error.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeinonenight](https://clawhub.ai/user/codeinonenight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to safely edit OpenClaw gateway configuration, verify keys before changing them, validate the gateway before restart, and recover from bad configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect OpenClaw gateway settings can affect future agent behavior or prevent the gateway from starting.

Mitigation: Review each proposed configuration change, back up openclaw.json first, verify keys against source, and validate the gateway before restart.

## Reference(s):

- [OpenClaw Safe Config on ClawHub](https://clawhub.ai/codeinonenight/skills/openclaw-safe-config)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides backup, source-verification, validation, restart, and recovery steps for OpenClaw gateway configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
