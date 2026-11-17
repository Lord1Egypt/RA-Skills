## Description:

Install Open Agent Search skills and connect its local stdio MCP server to an AI agent using uv and managed Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayanth-mkv](https://clawhub.ai/user/jayanth-mkv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to install Open Agent Search, connect its local MCP search tools to a coding agent, and troubleshoot the connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing search tooling and changing local agent configuration may affect existing integrations.

Mitigation: Review MCP configuration changes before applying them, preserve existing settings, and prefer project scope.

Risk: The skills installer can run a package that is not pinned in the setup command.

Mitigation: Pin or separately verify the skills installer package before running the npx command.

Risk: Optional HTTP hosting listens on all interfaces and may expose the service unnecessarily.

Mitigation: Avoid HTTP hosting unless needed for the task; use local stdio MCP for a local connection.

Risk: Search queries and fetched URLs are sent to upstream providers and websites.

Mitigation: Use non-sensitive test queries and avoid submitting confidential URLs or search terms.

## Reference(s):

- [Open Agent Search on ClawHub](https://clawhub.ai/jayanth-mkv/skills/open-agent-search-setup)
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and MCP configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP connection checks and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
