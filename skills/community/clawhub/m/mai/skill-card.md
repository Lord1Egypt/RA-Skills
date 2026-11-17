## Description:

Mai is an AI shopping matchmaking agent for OpenClaw and Hermes that helps merchants publish products and manage stock while helping buyers discover, compare, discuss, review, and create trackable orders with local-first transaction tracking and registry-backed PSP custody records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External buyers and merchants use Mai to manage local-first marketplace catalogs, compare products, exchange buyer-seller messages, track orders, and record payment custody status without claiming that the agent directly holds funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted registry authorization and deployment weaknesses could expose or corrupt order and marketplace data.

Mitigation: Fix /sync/push authorization before hosted use, bind local services to localhost or deploy strictly behind HTTPS, and protect and rotate API keys.

Risk: Registry marketplace data may include buyer, merchant, order, inventory, and local payment-reference records.

Mitigation: Store secrets outside flat registry files for production, restrict access to registry data, and use durable storage with backups, monitoring, and audit retention.

Risk: The bundled demo payment provider is not real money movement or escrow.

Mitigation: Use a licensed payment service provider for live holds, releases, refunds, chargebacks, and disputes, and do not claim payment success without PSP or external evidence.

## Reference(s):

- [Mai Data Schema](references/data-schema.md)
- [Mai Registry API](references/registry-api.md)
- [Mai Transaction Model](references/transaction-model.md)
- [Public Deployment Checklist](references/public-deployment.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product comparisons, merchant operations summaries, order status updates, risk notes, and next actions.]

## Skill Version(s):

1.1.4 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
