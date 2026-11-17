## Description:

iccn-erp helps agents query the Lingyi Wenjie IC ERP foreign-trade management system for orders, purchase orders, demand records, inbound and outbound records, customers, suppliers, inventory, and stock availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jexm](https://clawhub.ai/user/jexm)

### License/Terms of Use:


## Use Case:

Agents serving ERP users use this skill to route natural-language business data lookup requests to a configured ERP API and present matching business records. It is intended for order, purchasing, customer, supplier, and inventory lookup workflows where the operator controls the ERP endpoint and token scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a bearer token to query sensitive ERP business records.

Mitigation: Install it only for controlled ERP endpoints and configure a narrowly scoped read-only token.

Risk: Broad automatic lookups may expose customer, supplier, order, or inventory data beyond the user's intent.

Mitigation: Ask for confirmation before broad or ambiguous lookups involving sensitive business records.

Risk: The reference UI includes a dev.iccn.cc endpoint that is not suitable for production business data.

Mitigation: Use a trusted HTTPS ERP base URL from configuration and do not reuse the dev.iccn.cc reference endpoint for production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jexm/skills/iccn-erp)
- [Order detail UI reference](references/order-detail-ui.md)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown tables and concise text based on JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ERP_API_TOKEN and ERP_API_BASE_URL environment variables.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
