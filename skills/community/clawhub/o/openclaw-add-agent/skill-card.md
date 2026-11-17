## Description:

Add a new agent to OpenClaw configuration for a Telegram bot binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoxiaowei2117](https://clawhub.ai/user/gaoxiaowei2117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add a Telegram bot-backed agent to an OpenClaw configuration, create the agent workspace, and prepare the service restart step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits live OpenClaw configuration using Telegram bot tokens and user-provided agent identifiers.

Mitigation: Validate agent IDs, protect bot tokens as credentials, back up and validate openclaw.json before changes, and ask for explicit confirmation before modifying live configuration.

Risk: User-provided agent identifiers can affect workspace paths and shell commands.

Mitigation: Avoid shell-style interpolation, constrain identifiers to a safe character set, and review workspace directory creation before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoxiaowei2117/skills/openclaw-add-agent)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live configuration guidance for OpenClaw and Telegram bot credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
