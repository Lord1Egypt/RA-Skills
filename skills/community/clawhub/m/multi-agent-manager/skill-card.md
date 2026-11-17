## Description:

Monitor and visualize multiple agents across projects in real time with JSON output for debugging and performance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victory2694](https://clawhub.ai/user/victory2694)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams running multiple OpenClaw agents use this skill to inspect agent status, active sessions, workspaces, task flow, and basic named-agent communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can display local OpenClaw agent, workspace, status, and session information.

Mitigation: Use it only with agents and workspaces you control, and avoid sharing generated output when workspace or session details are sensitive.

Risk: The communication helper can send a message to a named agent.

Mitigation: Verify the target agent and message content before running the communication command.

Risk: The watch mode runs as a foreground monitoring loop.

Mitigation: Stop the watch process when active monitoring is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/victory2694/skills/multi-agent-manager)
- [README](artifact/README.md)
- [Development Notes](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus optional text or JSON command output from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper scripts can emit human-readable terminal output or JSON for agent lists, status, sessions, and task-flow inspection.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
