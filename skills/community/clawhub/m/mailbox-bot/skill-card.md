## Description:

Postal mail API and MCP server for AI agents: send letters, certified mail and postcards, and give an agent its own street address + PMB with webhooks, OCR search and human-approved scan, forward or discard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbengine](https://clawhub.ai/user/arbengine)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use mailbox.bot through REST or MCP to send physical mail, read inbound mail context, and propose mailbox actions such as scanning, forwarding, or discarding. Humans review costs and approve funded sends or inbound mailbox actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the skill suspicious because the README recommends an installation command that is not pinned to a fixed version; the scan was partial and its result is incomplete.

Mitigation: Review the installation instructions and verify the intended release before installing; treat the partial scan as incomplete.

Risk: Live outbound mail can create postage and service charges, and mailbox actions can affect physical mail.

Mitigation: Use dry-run quotes and a cost cap, show the human review details, and require owner approval for funded sends and scan, forward, or discard actions.

Risk: API credentials can authorize account operations if exposed.

Mitigation: Keep keys out of URLs, command-line arguments, copied prompts, and logs; use sandbox keys for testing.

## Reference(s):

- [MCP Install Guide](https://mailbox.bot/mcp-install)
- [API Documentation](https://mailbox.bot/api-docs)
- [OpenAPI Specification](https://mailbox.bot/openapi.json)
- [Public MCP Tool Catalog](https://mailbox.bot/api/mcp/tools-public)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON and shell examples, plus REST or MCP requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can send physical mail or incur charges; the skill documents dry runs, cost caps, and human approval steps.]

## Skill Version(s):

5.3.2 (source: frontmatter, changelog released 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
