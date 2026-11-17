## Description:

MCP Bridge helps agents configure and use the mcp-bridge-openclaw CLI to connect to and manage Model Context Protocol (MCP) servers with retry and auto-reconnection behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaggu1999](https://clawhub.ai/user/jaggu1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install mcp-bridge-openclaw, connect agents to MCP servers, list configured servers, enable verbose troubleshooting, and prepare secure server configuration examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm and npx package execution can run changed or unreviewed code.

Mitigation: Pin reviewed package versions where possible and prefer a project-local install before running commands.

Risk: GitHub credentials may be exposed if copied into plaintext config files or shell history.

Mitigation: Provide tokens through protected environment variables or a secret manager, and avoid typing real tokens directly into command lines.

## Reference(s):

- [mcp-bridge-openclaw npm package](https://www.npmjs.com/package/mcp-bridge-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands, CLI invocations, MCP server configuration examples, and secure credential-handling guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
