## Description:

Use Notion through mcporter-backed MCP tools for pages, databases, search, content updates, and workspace lookups via an MCP-integrated Notion server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dam1k](https://clawhub.ai/user/dam1k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read, search, and update Notion workspace pages and databases through MCP-backed tools. It is intended for user-authorized Notion workspaces with credentials supplied by the runtime environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can access a Notion workspace through the user's Notion token.

Mitigation: Install only for intended Notion access, keep the token in the runtime environment, and scope it as narrowly as practical.

Risk: The skill can support updates to important Notion pages or databases.

Mitigation: Inspect the target page or database before writes and review proposed changes before approving them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dam1k/skills/notion-remote-mcp)
- [Publisher profile](https://clawhub.ai/user/dam1k)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed Notion page or database changes for user review before execution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
