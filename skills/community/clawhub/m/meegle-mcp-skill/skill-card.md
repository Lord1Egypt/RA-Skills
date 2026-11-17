## Description:

Interact with Meegle project management system via MCP protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkycy](https://clawhub.ai/user/pkycy)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to connect OpenClaw to Meegle through MCP so an agent can manage projects, tasks, workflows, team membership, and reporting with natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can store live Meegle credentials in shell startup files, and crafted key values may enable persistent shell command execution.

Mitigation: Prefer OpenClaw config or a secret store for credentials, avoid running the setup script with untrusted values, and review shell profile changes before restarting the shell.

Risk: Natural-language requests can create, update, or change permissions and membership in a live Meegle workspace.

Mitigation: Use a narrowly scoped Meegle account or service account and review create, update, permission, and member-management requests before execution.

## Reference(s):

- [Meegle Official Website](https://www.meegle.com/)
- [Meegle Documentation](https://www.larksuite.com/hc/en-US/articles/040270863407-meegle-overview)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [ClawHub Skill Page](https://clawhub.ai/pkycy/skills/meegle-mcp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate authenticated MCP operations against the user's authorized Meegle workspace.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
