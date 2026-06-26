## Description: <br>
Send messages to a local OpenClaw/Rook gateway and receive responses directly from Claude Code through the `openclaw agent --message` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate work, request second opinions, trigger OpenClaw skills, and hand off context between Claude Code and a local OpenClaw/Rook gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send authenticated messages to a local OpenClaw gateway and configured agents, which may expose sensitive context or trigger actions outside Claude Code. <br>
Mitigation: Install only when the local gateway, configured agents, and OpenClaw account or token are trusted; avoid sending secrets or whole files. <br>
Risk: Agent handoffs and second-opinion responses can cross data-sharing boundaries and may return misleading or action-oriented guidance. <br>
Mitigation: Use explicit OpenClaw commands, review handoff content before forwarding it, and review returned guidance before acting on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nerua1/openclaw-bridge) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and parsed agent response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON-derived text payloads from the local OpenClaw gateway; responses are non-streaming and may need payload concatenation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
