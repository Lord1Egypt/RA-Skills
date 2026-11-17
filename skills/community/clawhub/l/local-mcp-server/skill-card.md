## Description:

Run a full Model Context Protocol (MCP) server in Termux. Exposes Read, Bash, Grep, glob tools for local Ollama models. Privacy-first, offline-capable, ~10MB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wizelements](https://clawhub.ai/user/wizelements)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy-conscious local AI users use this skill to set up a local MCP server that lets Ollama or compatible clients read files, run shell commands, search code, and match file patterns in Termux or Linux environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local MCP server can give AI tools access to local files and shell execution.

Mitigation: Run it only in a dedicated sandbox or least-privilege account, and restrict allowedPaths to specific project folders.

Risk: Shell access can execute unintended or unsafe commands when exposed to model-driven workflows.

Mitigation: Keep bash disabled unless it is required for the workflow, and review command behavior before enabling it.

Risk: Sensitive files or secrets could be exposed through filesystem access.

Mitigation: Do not expose home directories, SSH keys, tokens, private app data, or secret-containing folders to the server.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wizelements/skills/local-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, health-check, and configuration guidance for a local MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
