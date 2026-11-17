## Description:

Mayar.id payment integration for generating invoices, payment links, and tracking transactions via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsanatha](https://clawhub.ai/user/ahsanatha)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect agents to Mayar.id payment workflows, including invoice creation, payment-link generation, transaction tracking, subscription checks, WhatsApp payment messaging, and Indonesian payment method handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent access to a live Mayar payment account and customer transaction data.

Mitigation: Use least-privilege credentials where possible, restrict agent access to trusted environments, and review account permissions before installation.

Risk: Payment tokens may be exposed if placed directly in command arguments or committed configuration.

Mitigation: Store tokens outside committed files, avoid passing live tokens inline, protect credential files, and rotate credentials if exposure is suspected.

Risk: Payment fulfillment can be incorrect if webhook or polling results are trusted without verification.

Mitigation: Verify webhook behavior before production fulfillment, persist invoice IDs, and reconcile payment status before releasing goods or services.

Risk: Shell-string examples can become unsafe when populated with user-controlled fields.

Mitigation: Escape or validate customer-provided values and prefer structured API calls over interpolated shell commands in production implementations.

Risk: WhatsApp and reporting workflows can expose customer payment details.

Mitigation: Add consent, access control, and redaction controls before sending or storing customer-facing payment messages and reports.

## Reference(s):

- [Mayar.id API Reference](references/api-reference.md)
- [Mayar Integration Examples](references/integration-examples.md)
- [Mayar MCP Tools Reference](references/mcp-tools.md)
- [Official Mayar API Documentation](https://docs.mayar.id/api-reference/introduction)
- [Mayar API Keys](https://web.mayar.id/api-keys)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with shell, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP tool names, request fields, payment workflow patterns, and production checklist guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
