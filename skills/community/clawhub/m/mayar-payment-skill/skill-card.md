## Description: <br>
Mayar.id payment integration for generating invoices, payment links, and tracking transactions via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsanatha](https://clawhub.ai/user/ahsanatha) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Mayar.id for Indonesian payment workflows, including invoice creation, payment links, transaction checks, and subscription or membership lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to a Mayar payment API token and production payment-account actions. <br>
Mitigation: Start in sandbox, keep tokens out of shared configuration and logs, and require human approval before creating invoices or messaging customers. <br>
Risk: Incorrect recipient, amount, or invoice details could create payment requests for the wrong customer or value. <br>
Mitigation: Verify recipient, amount, item, expiry, and redirect details before sending payment links or customer messages. <br>
Risk: Example snippets use command execution patterns that may be unsafe if copied directly into production automation. <br>
Mitigation: Replace shell-string execution examples with safer argument-based tool calls before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsanatha/mayar-payment-skill) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [Integration Examples](references/integration-examples.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Mayar API documentation](https://docs.mayar.id/api-reference/introduction) <br>
- [Mayar.id](https://mayar.id) <br>
- [Mayar MCP endpoint](https://mcp.mayar.id/sse) <br>
- [Mayar production dashboard](https://web.mayar.id) <br>
- [Mayar sandbox dashboard](https://web.mayar.club) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing setup and workflow guidance for Mayar MCP payment operations; Mayar tool responses may include invoice IDs, transaction IDs, payment links, balances, customer records, and transaction status data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
