## Description:

Use when an AI agent needs to start, drive, or monitor an OpenCode CLI session programmatically over the Agent Client Protocol (ACP).

This skill is ready for commercial/non-commercial use.

## Publisher:

[berriosb](https://clawhub.ai/user/berriosb)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to start, control, resume, and monitor OpenCode CLI sessions over ACP JSON-RPC from another AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to spawn OpenCode with filesystem-write and terminal authority.

Mitigation: Use it only in a workspace where that authority is acceptable, preferably with sandboxing and without sensitive secrets.

Risk: The demo auto-approves OpenCode permission requests, which can allow tool actions without case-by-case human review.

Mitigation: Avoid running the demo in sensitive workspaces and review permission decisions manually for real sessions.

Risk: The documented update path includes a curl-to-bash installer fallback.

Mitigation: Independently inspect and verify installer content before executing it, or use a reviewed installation method.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/berriosb/skills/opencode-acp-control-3)
- [Publisher profile](https://clawhub.ai/user/berriosb)
- [Project repository](https://github.com/berriosb/Opencode-Acp-Control)
- [Agent Client Protocol](https://agentclientprotocol.com/llms.txt)
- [OpenCode](https://opencode.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with JSON-RPC examples, shell commands, and Python demo code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for an agent controlling an OpenCode ACP subprocess and handling permission prompts.]

## Skill Version(s):

0.3.1 (source: server release metadata; artifact source metadata remains 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
