## Description:

PO6 Mailbox helps agents manage PO6 email aliases, mailbox workflows, custom domains, and landing pages through the PO6 MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winstein](https://clawhub.ai/user/winstein)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to a PO6 account for email, alias, custom-domain, and landing-page management. Typical tasks include reading and searching email, drafting or sending messages, updating forwarding settings, publishing landing pages, and reviewing leads or analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped PO6 API key can allow sensitive mailbox, sending, deletion, publishing, lead, or domain-management actions.

Mitigation: Create a PO6 API key with only the scopes needed for the intended workflow, starting with read-only scopes where possible.

Risk: Persisting PO6_API_KEY in a shell profile makes the credential available to future sessions on the same machine.

Mitigation: Store the key only where needed, rotate it if exposed, and use PO6 key controls such as expiration, IP allowlists, and mailbox-specific scope isolation when appropriate.

Risk: The skill can perform account-changing operations such as sending mail, deleting mail, publishing pages, assigning domains, or accessing leads when granted matching scopes.

Mitigation: Review proposed actions before execution and reserve send, delete, publish, leads, and domain scopes for workflows that explicitly require them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/winstein/skills/po6-mailbox)
- [PO6 MCP Documentation](https://po6.com/docs/mcp)
- [PO6 Homepage](https://po6.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PO6_API_KEY environment variable and a configured PO6 MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
