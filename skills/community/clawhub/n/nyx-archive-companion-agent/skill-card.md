## Description:

Design, configure, and give identity to a companion AI agent that runs alongside a primary agent with its own tone, memory, Telegram bot, and heartbeat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyxur42](https://clawhub.ai/user/nyxur42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users use this skill to set up a persistent companion agent that shares a workspace with a primary agent while maintaining separate identity and memory files. It provides guidance for OpenClaw configuration, Telegram bot setup, heartbeat scheduling, and companion memory design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent Telegram-connected companion may send or receive messages on a schedule and expose sensitive context if tokens, destination IDs, or heartbeat content are misconfigured.

Mitigation: Store the Telegram token securely, verify the destination ID before enabling delivery, keep heartbeat content opt-in, and document how to disable schedules.

Risk: Broad shared workspace, memory, and tool access can let the companion read or alter primary-agent context beyond the intended scope.

Mitigation: Use a restricted workspace, minimal tool set, read-only shared references where possible, and review or roll back memory changes before relying on them.

## Reference(s):

- [[Nyx Archive] Companion Agent on ClawHub](https://clawhub.ai/nyxur42/skills/nyx-archive-companion-agent)
- [Identity Principles for Companion Agents](artifact/references/identity-principles.md)
- [Companion Memory File Template](artifact/references/memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may propose persistent messaging, shared workspace access, and memory file changes that should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
