## Description:

OpenSEO MCP (openseo.so). Use this skill for ANY OpenSEO MCP request — reading, creating, updating, and deleting data. Whenever a task involves OpenSEO MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SEO practitioners use this skill to discover OpenSEO MCP tools and read or manage SEO data through a connected OpenSEO account. It guides the agent to check each action's live schema and obtain approval before changes, deletion, or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software, and the CLI dependency may install other agent skills; the remote installer contents are unverified.

Mitigation: Review and install the CLI separately, decide whether to allow skill synchronization and disable it if unwanted, connect only the intended OpenSEO account, and retain approval for changes, deletion, and sharing.

## Reference(s):

- [OpenSEO MCP documentation](https://openseo.so/docs/mcp)
- [OpenSEO MCP](https://openseo.so)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the connected OpenSEO account and the selected tool.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
