## Description:

Installs and wires Mnemo Cortex (local-first persistent memory) into OpenClaw and other MCP-capable agents for cross-session recall, decision history, or multi-agent shared memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guymanndude](https://clawhub.ai/user/guymanndude)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install a local-first memory service and connect it to MCP-capable agent hosts for cross-session recall, decision history, and optional shared memory across agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs third-party code from a mutable remote repository.

Mitigation: Pin and review a specific upstream commit or release before installation.

Risk: Persistent local memory may retain sensitive project or user information across sessions.

Mitigation: Avoid saving credentials or confidential data, and confirm how to inspect and delete the local memory store before use.

Risk: Cross-agent memory sharing can expose saved context beyond the originating agent.

Mitigation: Keep cross-agent sharing disabled unless it is explicitly intended and reviewed.

## Reference(s):

- [Mnemo Cortex project](https://github.com/GuyMannDude/mnemo-cortex)
- [Mnemo Plan brain repo template](https://github.com/GuyMannDude/mnemo-plan)
- [THE-LANE-PROTOCOL.md](https://github.com/GuyMannDude/mnemo-cortex/blob/master/THE-LANE-PROTOCOL.md)
- [SESSION-GUIDE.md](https://github.com/GuyMannDude/mnemo-cortex/blob/master/SESSION-GUIDE.md)
- [MONITORING.md](https://github.com/GuyMannDude/mnemo-cortex/blob/master/MONITORING.md)
- [ClawHub skill page](https://clawhub.ai/guymanndude/skills/mnemo-cortex)
- [Publisher profile](https://clawhub.ai/user/guymanndude)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, host-specific configuration guidance, and verification prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and troubleshooting guidance for a local Mnemo Cortex service and MCP-capable agent host integrations.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
