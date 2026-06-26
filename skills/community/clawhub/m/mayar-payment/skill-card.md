## Description: <br>
Mayar.id payment integration for generating invoices, payment links, and tracking transactions via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsanatha](https://clawhub.ai/user/ahsanatha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Mayar.id payment workflows for Indonesian commerce, including invoice creation, payment links, transaction checks, subscriptions, webhooks, and customer payment messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live payment-account authority, including invoice creation, payment links, webhook registration, and customer messaging. <br>
Mitigation: Use sandbox credentials first, store the API token as a secret, verify and preferably pin the MCP helper, and require explicit confirmation before payment-account or customer-facing actions. <br>
Risk: Payment workflows handle customer names, emails, mobile numbers, payment status, and transaction details. <br>
Mitigation: Limit customer data shared with the agent, avoid logging secrets or unnecessary personal data, and review generated messages before sending them to customers. <br>


## Reference(s): <br>
- [Mayar.id API Reference](references/api-reference.md) <br>
- [Mayar Integration Examples](references/integration-examples.md) <br>
- [Mayar MCP Tools Reference](references/mcp-tools.md) <br>
- [Mayar Official API Documentation](https://docs.mayar.id/api-reference/introduction) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mayar API or MCP command outputs such as invoice IDs, transaction IDs, payment links, balances, and webhook results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
