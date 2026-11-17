## Description:

Ovra Payments enables AI agents to complete online checkouts, manage spending, and track purchases through Ovra payment tools without exposing real card data to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovra](https://clawhub.ai/user/ovra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an MCP-compatible agent make online payments, handle HTTP 402 paywalls, manage payment intents, upload transaction receipts, and review payment records while keeping real card data out of agent context.

### Deployment Geography for Use:

Global, with service data residency stated as EU (Germany).

## Known Risks and Mitigations:

Risk: The skill can initiate payments and perform account-changing actions, including admin, credential, card, customer, and deletion operations.

Mitigation: Use sandbox keys first, require explicit user confirmation for payments and account-changing actions, and enable only least-privilege tools needed for the task.

Risk: Production bearer tokens could authorize financial or administrative actions if stored or exposed insecurely.

Mitigation: Store live OVRA_API_KEY values in a secure secret store, avoid plaintext agent configs where possible, and rotate or revoke keys that may have been exposed.

Risk: Receipt upload can transmit PDF or PNG files to the Ovra MCP endpoint.

Mitigation: Upload only receipts or invoices from the current transaction and avoid sending arbitrary or unrelated files.

Risk: Customer deletion and card close actions can be irreversible.

Mitigation: Keep destructive tools behind separate approval, policy checks, and human confirmation before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ovra/skills/ovrapay)
- [Ovra publisher profile](https://clawhub.ai/user/ovra)
- [Ovra website](https://getovra.com)
- [Ovra documentation](https://docs.getovra.com)
- [Ovra MCP endpoint](https://api.getovra.com/api/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API calls, Shell commands]

**Output Format:** [Markdown with JSON configuration and MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OVRA_API_KEY and a connection to the Ovra MCP endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
