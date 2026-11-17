## Description:

Connects OAuth-capable agents to Meo Mai Moi through its MCP gateway to manage pet profiles, care and health records, habits, microchips, sharing, placement, helpers, messages, groups, finances, notifications, and account workflows with scoped authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troioi-vn](https://clawhub.ai/user/troioi-vn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OAuth-capable agent to Meo Mai Moi, choose appropriate scopes or presets, and perform pet-care workflows through the MCP gateway. It is especially useful for Codex, Cursor, OpenClaw, and similar clients that can configure MCP and complete OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request write-capable OAuth scopes by default for broad connections.

Mitigation: Review requested scopes before authorization, prefer narrow read-only scopes for initial connection when possible, and grant write scopes only for specific tasks.

Risk: A headless authorization code exchange can expose a single-use OAuth code if handled through an unsafe shell or durable log.

Mitigation: Use the client's native OAuth flow when possible; if a code must be pasted privately, parse only the code, pass it as a literal argument, exchange it immediately, and do not log or repeat it.

Risk: Consequential writes involving pet records, access, placement, messages, health data, finances, or invitations can affect people, records, permissions, or money.

Mitigation: Read the target immediately before changes, use stable IDs, preserve versions, use a fresh idempotency key, and verify the completed write with a read.

## Reference(s):

- [Connection and scope selection](references/connection.md)
- [OpenClaw native MCP onboarding](references/openclaw.md)
- [Safety and error handling](references/safety.md)
- [Meo MCP clients documentation](https://github.com/troioi-vn/meo-mcp/blob/main/docs/clients.md)
- [Meo MCP tools documentation](https://github.com/troioi-vn/meo-mcp/blob/main/docs/tools.md)
- [Meo MCP OAuth documentation](https://github.com/troioi-vn/meo-mcp/blob/main/docs/oauth.md)
- [Meo MCP errors documentation](https://github.com/troioi-vn/meo-mcp/blob/main/docs/errors.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth scope presets, MCP endpoint details, readiness checks, and safety constraints.]

## Skill Version(s):

0.3.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
