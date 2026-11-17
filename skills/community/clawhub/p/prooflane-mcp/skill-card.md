## Description:

Helps an agent clone, install, configure, verify, and use Prooflane's repo-native stdio MCP server and local product surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to evaluate Prooflane locally, attach a repo-native MCP server to an MCP-capable host, and run verification commands before relying on proof or run-review surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path can run mutable external repository code.

Mitigation: Use a disposable or least-privilege environment, inspect setup scripts before execution, and pin the cloned repository to a trusted commit.

Risk: The documented future package command is unpinned and not currently published.

Mitigation: Use the repo-native MCP start path for current evaluation and avoid unpinned package execution unless a reviewed version is available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaojiou176/skills/prooflane-mcp)
- [Install And Attach Prooflane MCP](references/INSTALL.md)
- [Prooflane MCP Capabilities](references/CAPABILITIES.md)
- [First-Success Path](references/DEMO.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenHands MCP Config](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP Config](references/OPENCLAW_MCP_CONFIG.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
