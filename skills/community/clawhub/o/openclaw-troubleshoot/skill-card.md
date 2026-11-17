## Description:

Provides step-by-step diagnostics and command-line fixes for common OpenClaw issues including memory plugin faults, Feishu disconnections, LLM timeouts, and Telegram errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wayne19820905](https://clawhub.ai/user/wayne19820905)

### License/Terms of Use:


## Use Case:

Developers and operators maintaining OpenClaw installations use this skill to diagnose common runtime, plugin, channel, and configuration issues and apply manual command-line repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual repair commands can disrupt the OpenClaw gateway or damage configuration if run carelessly.

Mitigation: Back up ~/.openclaw/openclaw.json, avoid gateway restart or kill commands during active sessions, and review commands before execution.

Risk: The /tmp/oc.json repair path can be unsafe for configuration updates.

Mitigation: Use a secure mktemp-based configuration update path before applying that repair.

## Reference(s):

- [Openclaw Troubleshoot ClawHub page](https://clawhub.ai/wayne19820905/skills/openclaw-troubleshoot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended as manual troubleshooting steps and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
