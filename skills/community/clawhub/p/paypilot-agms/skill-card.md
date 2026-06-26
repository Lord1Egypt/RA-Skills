## Description: <br>
PayPilot by AGMS helps agents process payments, send invoices, issue refunds, manage subscriptions, review sales, and work with fraud controls through a secure payment gateway proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agmsyumet](https://clawhub.ai/user/agmsyumet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchants and their agents use this skill to create invoices or payment links, process vaulted-card charges, issue refunds and voids, manage subscriptions, review transaction summaries, and configure fraud rules while avoiding raw card handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real financial changes with a saved token, including charges, refunds, voids, subscription changes, gateway configuration, and fraud-rule changes. <br>
Mitigation: Require explicit final user approval before each high-impact payment, subscription, gateway, or fraud-rule action, and prefer invoice links over direct vaulted-card charges when practical. <br>
Risk: Payment tokens, gateway keys, merchant data, or customer payment data could be mishandled if the agent or user bypasses the documented security practices. <br>
Mitigation: Keep tokens and gateway keys in protected config files, rotate saved tokens when needed, never collect raw card numbers or sensitive merchant PII in chat, and use hosted payment forms or vault tokens. <br>
Risk: The server security verdict is suspicious because the payment workflow depends on a third-party PayPilot/AGMS service for payment operations and merchant data. <br>
Mitigation: Install only if PayPilot/AGMS is trusted for payment operations, and independently verify its compliance, support practices, and account controls before using it with a real merchant account. <br>


## Reference(s): <br>
- [PayPilot Homepage](https://agms.com/paypilot/) <br>
- [ClawHub Listing](https://clawhub.ai/agmsyumet/paypilot-agms) <br>
- [Gateway API Reference](references/gateway-api.md) <br>
- [Payment Flows](references/payment-flows.md) <br>
- [PCI Compliance & Data Security](references/pci-compliance.md) <br>
- [PayPilot OpenAPI Spec](https://paypilot.agms.com/openapi.json) <br>
- [PayPilot AI Plugin Manifest](https://paypilot.agms.com/.well-known/ai-plugin.json) <br>
- [PayPilot LLM Resource Index](https://paypilot.agms.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uses a local PayPilot config file and the PayPilot HTTPS API.] <br>

## Skill Version(s): <br>
1.3.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
