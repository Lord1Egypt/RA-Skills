## Description:

Accept crypto payments, manage a digital storefront, and track balances through the InventPay REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jams24](https://clawhub.ai/user/jams24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and merchants use this skill to let an agent create crypto payment links and invoices, manage InventPay storefront products and key pools, check balances, and track orders through the InventPay REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The merchant API key enables live payment, storefront, product, order, and balance operations.

Mitigation: Install only if you trust InventPay with the merchant API key, store the key in INVENTPAY_API_KEY, and rotate or revoke it from the dashboard when needed.

Risk: Product deletion, bulk key removal, order status changes, and product content updates can affect real business records or customer delivery.

Mitigation: Require the agent to show the exact target and get confirmation before destructive, bulk, or state-changing merchant actions.

Risk: Product delivery content can expose secrets if credentials or private keys are included.

Mitigation: Do not pass credentials, secrets, or private keys as product delivery content; use hosted file URLs for delivery material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jams24/skills/inventpay-api)
- [InventPay](https://inventpay.io)
- [InventPay API Docs](https://docs.inventpay.io)
- [InventPay JavaScript SDK](https://www.npmjs.com/package/inventpay)
- [InventPay Python SDK](https://pypi.org/project/inventpay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST endpoint examples, JSON request bodies, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INVENTPAY_API_KEY for authenticated merchant operations.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
