## Description:

pctx provides an MCP aggregation and Code Mode execution layer that connects agents to Linear, GitHub, and other MCP servers through one local endpoint for token-efficient tool workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cianbyrne1010](https://clawhub.ai/user/cianbyrne1010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, check, and operate a local pctx layer for aggregating MCP servers and batching Linear, GitHub, or other MCP tool calls through Code Mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and starts high-impact local tooling with persistent access to GitHub, Linear, or similar configured credentials.

Mitigation: Review before installing and only run it when you trust the pctx, Homebrew, npm, GitHub MCP, and Linear MCP supply chain.

Risk: The local pctx service can use configured API tokens through connected MCP servers.

Mitigation: Keep pctx configuration private, use least-privilege tokens, and back up pctx config before rollback or MCP mutation commands.

Risk: Helper commands can start persistent localhost services and execute selected MCP tool calls through Code Mode.

Mitigation: Inspect or recreate the LaunchAgent before starting it, avoid passing untrusted names into the test command, and review generated tool-call code before execution.

## Reference(s):

- [pctx GitHub repository](https://github.com/portofcontext/pctx)
- [ClawHub skill listing](https://clawhub.ai/cianbyrne1010/skills/pctx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, curl, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide local pctx service setup, MCP configuration changes, daemon management, and Code Mode tool-call testing.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
