## Description:

Mayar.id payment integration for generating invoices, payment links, and tracking transactions via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsanatha](https://clawhub.ai/user/ahsanatha)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to connect an agent to Mayar.id payment workflows for Indonesian commerce, including invoice creation, payment links, transaction tracking, membership checks, and customer payment messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured MCP server can access the user's Mayar payment account.

Mitigation: Install only when that account access is acceptable, use sandbox tokens first, and scope production credentials to the minimum account permissions available.

Risk: Unpinned `npx -y` setup can execute a changing MCP bridge package.

Mitigation: Pin or preinstall the MCP bridge before production use.

Risk: Live tokens in shared configuration or process arguments can expose payment credentials.

Mitigation: Store credentials outside shared config, restrict file permissions, and avoid passing live tokens through command arguments where they may be logged or inspected.

Risk: Webhook, polling, and customer-message examples can create payment or messaging errors if copied directly into production.

Mitigation: Add webhook authentication, idempotency, input validation, payment-state checks, and customer consent controls before deployment.

## Reference(s):

- [Mayar MCP Tools Reference](references/mcp-tools.md)
- [Mayar Integration Examples](references/integration-examples.md)
- [Mayar.id API Reference](references/api-reference.md)
- [Mayar Official API Documentation](https://docs.mayar.id/api-reference/introduction)
- [Mayar.id](https://mayar.id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool calls, API request examples, and customer-message templates.]

## Skill Version(s):

1.0.0 (source: server release metadata and README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
