## Description:

OpenClaw MCP Debugger provides MCP environment diagnostics, health checks, latency audits, and automated repair paths for local MCP servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect and troubleshoot MCP connections between agents and external tools, including handshake, latency, and local server health issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic repair actions may restart local MCP services without clear scoping.

Mitigation: Run the skill first in a limited environment and avoid `--all` unless the affected servers are understood.

Risk: The documented `npx` command may resolve an unpinned OpenClaw CLI version.

Mitigation: Pin or preinstall a trusted OpenClaw CLI version before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmstudio667-commits/skills/openclaw-mcp-debugger)
- [Publisher profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic findings, latency observations, protocol audit notes, and repair suggestions for local MCP services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
