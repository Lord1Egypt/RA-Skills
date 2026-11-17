## Description:

Provides Amazon Multi-Channel Fulfillment (MCF) Fulfillment Outbound v2026-07-04 workflows for quoting, previewing, creating, reading, updating, canceling, and tracking fulfillment orders, plus listing related invoice headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and developers use this skill to manage Amazon MCF outbound fulfillment for non-Amazon sales channels. It helps compare delivery offers, preview fees and constraints, create or update confirmed orders, retrieve order and shipment status, and inspect invoice headers.

### Deployment Geography for Use:

Global, subject to Amazon SP-API region support for NA, EU, and FE stores.

## Known Risks and Mitigations:

Risk: The package includes account-login, API-key generation, and payment-order tooling outside the advertised Amazon fulfillment purpose.

Mitigation: Review the bundled onboarding code before installation and avoid invoking account, API-key, or payment commands unless those capabilities are intended and trusted.

Risk: The skill sends store, fulfillment, and order data through the LinkFox gateway using a LinkFox API key.

Mitigation: Install only from a trusted publisher, use the minimum necessary store and order data, and do not provide raw Amazon access or refresh tokens.

Risk: Full fulfillment responses are written to local session data files and read or preview responses may be cached.

Mitigation: Run the skill from an appropriate private workspace, manage retention of saved response files and caches, and avoid forcing inline full output when responses contain sensitive customer or order data.

Risk: Confirmed write operations can create, update, cancel, or simulate Amazon fulfillment order state.

Mitigation: Require explicit user confirmation, review the selected store, destination, line items, service tier, fees, and order identifiers before setting confirmWrite true, and query current state before retrying uncertain writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-fulfillment-outbound)
- [Fulfillment Outbound API contract](references/api.md)
- [Fulfillment Outbound workflows](references/workflows.md)
- [Authorization and pre-call checks](references/onboarding.md)
- [Fulfillment Outbound migration guide](references/migration.md)
- [Amazon Fulfillment Outbound API](https://developer-docs.amazon.com/sp-api/docs/fulfillment-outbound-api)
- [Amazon Fulfillment Outbound v2026-07-04 reference](https://developer-docs.amazon.com/sp-api/reference/fulfillment-outbound-v2026-07-04)
- [Amazon Fulfillment Outbound v2026-07-04 OpenAPI model](https://github.com/amzn/selling-partner-api-models/blob/main/models/fulfillment-outbound-api-model/fulfillmentOutbound_2026-07-04.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses or summaries written to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full fulfillment responses are stored under the working directory's linkfox session data path; read and preview calls may use a 24-hour session cache.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
