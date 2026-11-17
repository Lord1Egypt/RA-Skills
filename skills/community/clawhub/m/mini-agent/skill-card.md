## Description:

Mini-Agent is a MiniMax M2.5-based coding assistant for OpenClaw that can read and edit files, run shell commands, write code, and manage processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1-m1ng](https://clawhub.ai/user/l1-m1ng)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use Mini-Agent to carry out coding, file-management, configuration, command execution, and system-management tasks through natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can pull mutable remote code from the upstream MiniMax-AI/Mini-Agent repository.

Mitigation: Install only from a trusted reviewed release or pinned commit.

Risk: The agent can read and write files, execute shell commands, and manage background processes.

Mitigation: Run it in a constrained workspace and review destructive file or process operations before allowing them.

Risk: Detailed session logs may contain prompts, tool calls, tool results, and sensitive content.

Mitigation: Avoid using it with secrets unless logs are disabled, protected, or routinely reviewed and cleaned.

## Reference(s):

- [Mini-Agent ClawHub release](https://clawhub.ai/l1-m1ng/skills/mini-agent)
- [MiniMax](https://www.minimaxi.com)
- [MiniMax Open Platform](https://platform.minimaxi.com)
- [OpenClaw](https://github.com/openclaw)
- [Mini-Agent upstream install source](https://github.com/MiniMax-AI/Mini-Agent.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language responses with code, shell commands, and configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed file edits, executed command results, process-management steps, and session logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
