## Description:

MCP server for the Lawmatics legal CRM API. Exposes Lawmatics' REST API as read-only MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjquinlan2000](https://clawhub.ai/user/mjquinlan2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal operations teams use this skill to let an agent list and call read-only Lawmatics CRM API tools through mcporter over stdio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose Lawmatics CRM data returned by read-only tools to the active agent session.

Mitigation: Install only when agent access to Lawmatics CRM data is intended, and use a dedicated least-privilege or read-only credential where possible.

Risk: The skill depends on external mcporter and lawmatics-mcp binaries or packages.

Mitigation: Verify the package or binary source before trusting it in an agent environment.

Risk: The NODE_MCP_SECRET_KEY credential is required for authentication.

Mitigation: Store the secret outside prompts and source files, scope it narrowly, and rotate it if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjquinlan2000/skills/lawmatics-mcp)
- [npm package @mjquinlan2000/lawmatics-mcp](https://www.npmjs.com/package/@mjquinlan2000/lawmatics-mcp)
- [Publisher profile](https://clawhub.ai/user/mjquinlan2000)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Lawmatics CRM API access via stdio; requires NODE_MCP_SECRET_KEY, mcporter, and lawmatics-mcp.]

## Skill Version(s):

1.0.0 (source: release evidence, created 2026-03-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
