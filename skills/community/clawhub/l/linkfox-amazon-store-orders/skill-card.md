## Description:

Helps agents search Amazon seller orders, retrieve order details, buyer and shipping information, order items, regulated-order information, and manage shipment or verification status through LinkFox-managed Amazon SP-API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, operators, and support agents use this skill to query seller order data, inspect buyer or fulfillment details, and perform supported shipment, verification, or regulated-order workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Amazon seller order data, buyer information, shipping addresses, and regulated-order information.

Mitigation: Install only when the LinkFox gateway is trusted, treat saved output files and logs as sensitive, and require explicit user confirmation before retrieving PII.

Risk: The onboarding flow can handle API keys, phone login codes, payment QR data, and order or billing status.

Mitigation: Use secure secret storage for API keys, avoid persisting secrets in shared shell profiles, and require explicit confirmation before creating paid orders.

Risk: Configurable gateway environment variables can direct credential-bearing requests to alternate endpoints.

Mitigation: Prefer the default LinkFox gateway and review any custom gateway environment variable before use.

Risk: Repeated failed or high-frequency Amazon SP-API requests can trigger store-level protective cooldowns.

Mitigation: Stop automatic retries on repeated 400, 403, 404, or 429 responses, correct parameters or authorization first, and observe retryAfter or blockedUntil values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-orders)
- [API and gateway calling guide](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [Amazon SP-API searchOrders](https://developer-docs.amazon.com/sp-api/reference/searchorders)
- [Amazon SP-API getOrder](https://developer-docs.amazon.com/sp-api/reference/getorder-3)
- [Amazon SP-API getOrderItems](https://developer-docs.amazon.com/sp-api/reference/getorderitems)
- [Amazon SP-API updateShipmentStatus](https://developer-docs.amazon.com/sp-api/reference/updateshipmentstatus)
- [Amazon SP-API getOrderRegulatedInfo](https://developer-docs.amazon.com/sp-api/reference/getorderregulatedinfo)
- [Amazon SP-API updateVerificationStatus](https://developer-docs.amazon.com/sp-api/reference/updateverificationstatus)
- [Amazon SP-API confirmShipment](https://developer-docs.amazon.com/sp-api/reference/confirmshipment)
- [Amazon SP-API createRestrictedDataToken](https://developer-docs.amazon.com/sp-api/reference/createrestricteddatatoken)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Files, Configuration]

**Output Format:** [Markdown guidance with Python shell commands and JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full JSON responses under ./linkfox/<YYYY-MM-DD>/<session>/data and may print summaries for responses over 8 KB.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
