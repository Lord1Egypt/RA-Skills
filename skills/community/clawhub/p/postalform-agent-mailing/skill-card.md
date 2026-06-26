## Description: <br>
Send real postal mail through PostalForm using machine payments: prepare and validate print-and-mail payloads, submit orders, settle x402 payment with a compatible wallet client, and poll fulfillment through completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggaabe](https://clawhub.ai/user/ggaabe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare, validate, pay for, and track real physical mail sent through PostalForm. It is intended for workflows that need reliable payload construction, idempotent retries, quote checks, payment settlement, and fulfillment polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to send real physical mail and share document contents with PostalForm. <br>
Mitigation: Install and invoke it only for workflows that intentionally require physical mail, and verify the document, sender, recipient, and mailing options before order submission. <br>
Risk: The order flow requires payment settlement and could spend funds if wallet access is misconfigured or uncapped. <br>
Mitigation: Use a limited wallet or capped payment client, protect wallet credentials, verify the quote and requested network, and set a maximum payment amount before submitting a paid order. <br>
Risk: Changing the payload while reusing a request identifier can create idempotency failures. <br>
Mitigation: Keep the request ID and payload bytes stable for retries, and generate a new request ID for any changed order. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ggaabe/postalform-agent-mailing) <br>
- [Payload Templates](references/payload_templates.md) <br>
- [PostalForm Machine Order Validation API](https://postalform.com/api/machine/orders/validate) <br>
- [PostalForm Machine Order API](https://postalform.com/api/machine/orders) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns order identifiers, quote details, payment settlement details, latest fulfillment status, and the order completion URL when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
