## Description:

Provides Amazon FBA management workflows for checking inbound eligibility and inventory, managing inbound plans, shipments, labels, and legacy MCF fulfillment orders through LinkFox's SP-API gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to perform Amazon FBA eligibility, inventory, inbound shipment, label, bill-of-lading, and legacy MCF fulfillment workflows from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full Amazon FBA operation responses may be stored as plaintext local JSON files.

Mitigation: Run the skill only in trusted workspaces, restrict access to the local linkfox output folder, and remove or secure response files that contain seller, inventory, shipment, fulfillment, or customer data.

Risk: Onboarding can involve LinkFox phone login, SMS codes, and payment QR or payment URL flows.

Mitigation: Enter phone numbers, SMS codes, or payment approvals only when deliberately onboarding with a trusted LinkFox account and after confirming the action with the user.

Risk: Write operations can change Amazon FBA inbound, shipment, inventory, fulfillment, return, or tracking state.

Mitigation: Review seller, region, path parameters, request bodies, and operation intent before execution; for uncertain write results, query status before replaying the operation.

Risk: Repeated failed requests or high-frequency polling can trigger Amazon SP-API protection or rate-limit responses.

Mitigation: Avoid automatic retries and concurrent probing; follow retryAfter or blockedUntil signals, fix parameters or authorization issues before retrying, and ask before continuing cost- or rate-sensitive pagination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-fba)
- [API and gateway notes](references/api.md)
- [Capabilities](references/capabilities.md)
- [Onboarding](references/onboarding.md)
- [Operations registry](references/operations.json)
- [Amazon getItemEligibilityPreview](https://developer-docs.amazon.com/sp-api/reference/getitemeligibilitypreview)
- [Amazon FBA Inventory v1](https://developer-docs.amazon.com/sp-api/reference/fba-inventory-v1)
- [Amazon Fulfillment Inbound v2024-03-20](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v2024-03-20)
- [Amazon Fulfillment Inbound v0](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v0)
- [Amazon Fulfillment Outbound 2020-07-01](https://developer-docs.amazon.com/sp-api/reference/fulfillment-outbound-2020-07-01)

## Skill Output:

**Output Type(s):** [API Calls, Files, JSON, Guidance, Shell commands]

**Output Format:** [JSON responses saved to local files, with concise text summaries for large responses and optional inline JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are written under a local linkfox session data folder and may contain sensitive Amazon seller, shipment, inventory, fulfillment, or customer operation data.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
