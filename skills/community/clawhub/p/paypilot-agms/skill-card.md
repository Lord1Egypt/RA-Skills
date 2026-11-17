## Description:

Process payments, send invoices, issue refunds, manage subscriptions, and detect fraud via a secure payment gateway proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agmsyumet](https://clawhub.ai/user/agmsyumet)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and payment operators use this skill to set up PayPilot access, send payment links, process vaulted-card charges, issue refunds or voids, manage subscriptions, review sales activity, and configure fraud rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through live payment, refund, void, subscription, and fraud-rule changes.

Mitigation: Require explicit manual confirmation before every money-moving or account-changing action.

Risk: Payment credentials, gateway keys, bearer tokens, card data, and merchant passwords could be exposed through chat or local files.

Mitigation: Do not paste secrets or card data into chat; prefer browser or secret-manager setup, least-privilege short-lived tokens, hosted payment pages, and vaulted card tokens.

Risk: The server security verdict is suspicious because the skill asks agents to handle payment workflows without strong confirmation and scoping controls.

Mitigation: Install only if the PayPilot/AGMS service is trusted and confirm local operating controls before enabling production use.

## Reference(s):

- [PayPilot Homepage](https://agms.com/paypilot/)
- [Gateway API Reference](references/gateway-api.md)
- [Payment Flows](references/payment-flows.md)
- [PCI Compliance & Data Security](references/pci-compliance.md)
- [PayPilot OpenAPI Specification](https://paypilot.agms.com/openapi.json)
- [PayPilot LLM Resource Index](https://paypilot.agms.com/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; produces payment workflow guidance and API command examples for user-approved actions.]

## Skill Version(s):

1.3.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
