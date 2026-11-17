## Description:

This skill helps agents manage Amazon FBA inbound workflows, including inbound plans, packing, placement, shipments, transportation options, labels, documents, compliance, appointments, and asynchronous operation status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, operators, and developers use this skill to create, inspect, and update FBA inbound workflows through LinkFox-authenticated Amazon SP-API operations. It supports guided handling of workflow IDs, user confirmations for write operations, asynchronous status checks, marketplace constraints, labels, and shipment documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Amazon seller fulfillment data, account authorization context, and LinkFox billing flows.

Mitigation: Install only if you trust LinkFox with this data and review authorization or billing prompts before continuing.

Risk: API keys or seller identifiers could be exposed through shared logs, shell history, or copied command output.

Mitigation: Use a secret manager or protected environment variables and avoid pasting API keys or sensitive seller data into shared channels.

Risk: Configurable gateway URL environment variables can redirect requests away from the default LinkFox endpoint.

Mitigation: Do not set gateway override variables unless you control and trust the destination.

Risk: Full Amazon SP-API responses may be written to the local LinkFox output directory.

Mitigation: Keep generated output out of shared or synced workspaces and remove retained seller data when it is no longer needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-fulfillment-inbound)
- [Fulfillment Inbound API reference](references/api.md)
- [Fulfillment Inbound workflows](references/workflows.md)
- [ID source and cross-version rules](references/identifiers.md)
- [Marketplace constraints](references/marketplace-constraints.md)
- [Authentication, authorization, and billing guidance](references/onboarding.md)
- [Amazon Fulfillment Inbound API overview](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api)
- [Amazon Fulfillment Inbound v2024-03-20 reference](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v2024-03-20)
- [Amazon Fulfillment Inbound v2024-03-20 OpenAPI model](https://github.com/amzn/selling-partner-api-models/blob/main/models/fulfillment-inbound-api-model/fulfillmentInbound_2024-03-20.json)
- [Amazon Fulfillment Inbound v0 OpenAPI model](https://github.com/amzn/selling-partner-api-models/blob/main/models/fulfillment-inbound-api-model/fulfillmentInboundV0.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Files, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON API responses written to local files or stdout summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are persisted locally; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
