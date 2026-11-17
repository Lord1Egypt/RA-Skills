## Description:

Persistent cross-session memory and verifiable agent identity via the Lithtrix MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[learningloons-hash](https://clawhub.ai/user/learningloons-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to connect an agent to Lithtrix for storing, retrieving, and searching cross-session memory, and for checking Lithtrix agent passports when interacting with registered agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send memory contents, search queries, task summaries, and user preferences to an external Lithtrix service for persistence.

Mitigation: Avoid storing secrets or sensitive personal, financial, legal, health, proprietary, or credential data, and make stored memories reviewable and deletable.

Risk: The setup recommends installing the MCP server with an unpinned npx package command.

Mitigation: Use a pinned and reviewed lithtrix-mcp package version before deployment.

Risk: Persistent memory can affect future sessions without restating the original user context.

Mitigation: Require user approval for meaningful memory writes and review retrieved memories before relying on them.

## Reference(s):

- [Lithtrix documentation](https://docs.lithtrix.ai)
- [Lithtrix homepage](https://lithtrix.ai)
- [Lithtrix MCP package](https://www.npmjs.com/package/lithtrix-mcp)
- [Lithtrix trust overview](https://lithtrix.ai/trust.html)
- [ClawHub skill page](https://clawhub.ai/learningloons-hash/skills/lithtrix-memory)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with API examples, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LITHTRIX_API_KEY and use of the Lithtrix MCP server or Lithtrix HTTP API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
