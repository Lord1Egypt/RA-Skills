## Description:

Configure a multi-agent Telegram group system with a shared OpenClaw workspace and shared MemOS memory for specialized agent collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure multiple OpenClaw agents in a Telegram group, including shared workspace directories, shared MemOS memory, Telegram bot account bindings, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot privacy may be disabled so configured agents can see broader group messages.

Mitigation: Use tightly scoped group and user allowlists, avoid sensitive real group traffic during testing, and make sure participants understand which bots can read group messages.

Risk: A shared workspace and shared MemOS memory pool can expose files or memory across agents.

Mitigation: Use separate workspaces or memory namespaces for agents handling sensitive content, and keep shared-context files limited to information intended for all agents.

Risk: Bot tokens and configuration secrets may be copied into chats, shared files, or logs during setup.

Mitigation: Keep tokens out of shared chats and files, restrict file access to the configuration owner, and rotate any token that may have been exposed.

## Reference(s):

- [OpenClaw multi-agent setup guide](https://github.com/bozhouDev/openclaw_agent_create_prompt)
- [ClawHub skill page](https://clawhub.ai/huamu668/skills/huamu668-openclaw-multiagent)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, configuration examples, directory structure guidance, and operational checks for a shared multi-agent Telegram deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
