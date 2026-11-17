## Description:

Manages Amazon External Fulfillment workflows for LinkFox users, including location-level inventory, shipments, packages, package status, shipping options, invoices, labels, and returns for Seller Flex, FBA Onsite, Easy Ship, Self Ship, MFN Self Delivery, and related programs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and commerce operations teams use this skill through an agent to run Amazon SP-API External Fulfillment tasks for authorized LinkFox seller stores, including inventory publishing or retrieval, shipment processing, package updates, label and invoice generation, shipping option retrieval, and return lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real LinkFox and Amazon seller operations, including write-capable inventory, package, shipment, invoice, label, and return workflows.

Mitigation: Review seller, region, resource IDs, request bodies, and current fulfillment state before running write actions; stop and correct inputs rather than retrying repeated failures.

Risk: Phone-based login, API-token setup, and billing recovery flows can expose credentials or initiate payment-related actions from the agent.

Mitigation: Prefer secure credential storage, avoid sharing phone codes or API keys in unnecessary contexts, and require explicit user confirmation before ordering or querying payment plans.

Risk: Endpoint override environment variables can redirect requests while real credentials are configured.

Mitigation: Use the default trusted LinkFox gateway for production seller accounts and reserve endpoint overrides for controlled testing without production credentials.

Risk: Saved linkfox response files may contain sensitive seller, shipment, inventory, invoice, label, or return data.

Mitigation: Treat saved response files as sensitive business data, limit workspace access, and remove local data files when they are no longer needed.

## Reference(s):

- [API and gateway reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [Amazon SP-API batchInventory reference](https://developer-docs.amazon.com/sp-api/reference/batchinventory)
- [Amazon SP-API publish location-level inventory](https://developer-docs.amazon.com/sp-api/docs/publish-location-level-inventory)
- [Amazon SP-API retrieve location-level inventory](https://developer-docs.amazon.com/sp-api/docs/retrieve-location-level-inventory)
- [Amazon SP-API getShipments reference](https://developer-docs.amazon.com/sp-api/reference/getshipments-1)
- [Amazon SP-API getShipment reference](https://developer-docs.amazon.com/sp-api/reference/getshipment-1)
- [Amazon SP-API processShipment reference](https://developer-docs.amazon.com/sp-api/reference/processshipment)
- [Amazon SP-API createPackages reference](https://developer-docs.amazon.com/sp-api/reference/createpackages)
- [Amazon SP-API updatePackage reference](https://developer-docs.amazon.com/sp-api/reference/updatepackage)
- [Amazon SP-API updatePackageStatus reference](https://developer-docs.amazon.com/sp-api/reference/updatepackagestatus)
- [Amazon SP-API retrieveShippingOptions reference](https://developer-docs.amazon.com/sp-api/reference/retrieveshippingoptions)
- [Amazon SP-API generateInvoice reference](https://developer-docs.amazon.com/sp-api/reference/generateinvoice)
- [Amazon SP-API retrieveInvoice reference](https://developer-docs.amazon.com/sp-api/reference/retrieveinvoice)
- [Amazon SP-API generateShipLabels reference](https://developer-docs.amazon.com/sp-api/reference/generateshiplabels)
- [Amazon SP-API listReturns reference](https://developer-docs.amazon.com/sp-api/reference/listreturns)
- [Amazon SP-API getReturn reference](https://developer-docs.amazon.com/sp-api/reference/getreturn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON responses saved to local files; small responses may also be printed as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses under linkfox/<date>/<session>/data and summarizes larger responses unless inline output is requested.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
