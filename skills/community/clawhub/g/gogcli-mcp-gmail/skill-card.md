## Description:

Use when the user asks to read, organize, draft, forward, autoreply, or otherwise work with Gmail in depth. Triggers for requests involving threads, labels, drafts, attachments, bulk archive/trash/mark-read operations, forwarding messages, or any Gmail operation beyond simple search/get/send. Includes auth and Gmail tools only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT

## Use Case:

People using an AI agent with an authenticated Gmail account can search and review messages, manage threads and labels, work with drafts, and carry out Gmail settings and bulk operations. Developers can use it to expose these Gmail workflows through an MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with medium confidence, citing a Gmail forwarding confirmation flaw and capabilities extending beyond its declared Gmail scope; scanning coverage is incomplete.

Mitigation: Review forwarding confirmation behavior, attachment destinations, and tool permissions before connecting sensitive mail. Set GOG_READONLY=1 when read-only access is sufficient.

## Reference(s):

- [gogcli-mcp-gmail project documentation](https://github.com/chrischall/gogcli-mcp)
- [gogcli](https://github.com/openclaw/gogcli)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Links]

**Output Format:** [Gmail tool responses in text or JSON, with attachment content, file, or URL results where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Gmail operation and may include message content, attachments, or account changes.]

## Skill Version(s):

4.12.0 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
