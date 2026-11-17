## Description:

Provides Temu EU fulfillment and shipping API workflows for buy-shipping labels, co-warehouse fulfillment, self-fulfilled shipments, tracking, and self-delivery POD upload and audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu sellers, operations teams, and developers use this skill to run EU order-shipping fulfillment workflows, including label purchase, shipment confirmation, warehouse fulfillment, tracking lookup, and POD handling.

### Deployment Geography for Use:

Europe (Temu EU seller workflows)

## Known Risks and Mitigations:

Risk: The skill handles powerful Temu seller credentials and sensitive order or shipment data.

Mitigation: Use a dedicated workspace, avoid shared machines, grant only the Temu permissions needed for the task, and treat saved tokens and response files as sensitive.

Risk: Shipment confirmation, cancellation, payment-related, or POD upload actions can affect real seller operations.

Mitigation: Review generated requests and confirm business-critical actions before running scripts in a real Temu seller environment.

Risk: Endpoint override environment variables could redirect requests away from expected LinkFox or Temu services.

Mitigation: Avoid endpoint overrides unless they are required and have been reviewed for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-fulfillment-eu)
- [Partner EU fulfillment catalog](artifact/references/partner-eu-catalog.md)
- [API reference](artifact/references/api.md)
- [Temu access token guide](artifact/references/access-token.md)
- [Authorization flow](artifact/references/authorization-flow.md)
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API request or response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts write full API responses under the current workspace linkfox data directory and may print either complete JSON or summarized output depending on response size.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
