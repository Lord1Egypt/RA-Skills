## Description:

Teach an agent to install ProofTrail's governed stdio MCP server, use the safest read and proof tools first, and keep future package or listing claims honest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to attach ProofTrail as a local stdio MCP server, inspect browser evidence through safe read-first tools, and avoid overclaiming unpublished package or hosted-service surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run an unpinned external repository as a local MCP server.

Mitigation: Review the ProofTrail repository before installing, pin it to a trusted commit, and run pnpm with normal supply-chain precautions.

Risk: The local MCP process could receive unrelated credentials or broader filesystem access than the task requires.

Mitigation: Avoid passing unrelated credentials to the MCP process and scope filesystem and environment access to the ProofTrail task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/prooftrail-mcp)
- [Install And Attach ProofTrail MCP](references/INSTALL.md)
- [ProofTrail MCP Capabilities](references/CAPABILITIES.md)
- [First-Success Path](references/DEMO.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenHands MCP configuration](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP configuration](references/OPENCLAW_MCP_CONFIG.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents toward catalog, read, quality-read, and proof tools before broader run tools.]

## Skill Version(s):

0.1.1 (source: frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
