## Description:

Runtime safety guard for OpenClaw multi-agent workflows that blocks destructive tools for controlled agents and redirects those operations to sub-agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifeel-is-a-mouse](https://clawhub.ai/user/ifeel-is-a-mouse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Mainctrl to manage runtime tool access for OpenClaw multi-agent workflows. It helps keep orchestration agents in a read-and-delegate posture while allowing configured sub-agents to perform execution tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blocked destructive actions are automatically delegated to sub-agents, which may still have broad permissions.

Mitigation: Review sub-agent permissions before enabling Mainctrl and restrict controlled agents and blocked tools to the workflow policy you intend to enforce.

Risk: The exec allow-except feature is a convenience control and should not be treated as a strong security boundary.

Mitigation: Keep exec blocked for sensitive workflows, minimize allow-except entries, and verify status before relying on command filtering.

Risk: The refresh-memory command writes Mainctrl state into persistent future agent context.

Mitigation: Use refresh-memory only when persistent state is desired and review the memory file after running it.

Risk: If the plugin state file is missing or corrupted, the plugin falls back to allowing tool calls.

Mitigation: Run the status command after installation or configuration changes and verify blocking behavior before depending on the guardrail.

## Reference(s):

- [Mainctrl ClawHub skill page](https://clawhub.ai/ifeel-is-a-mouse/skills/mainctrl)
- [Publisher profile](https://clawhub.ai/user/ifeel-is-a-mouse)
- [Skill README](artifact/README.md)
- [Plugin README](artifact/plugin/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for toggling tool blocking, configuring controlled agents, managing exec allow-except rules, and installing or removing the companion plugin.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
