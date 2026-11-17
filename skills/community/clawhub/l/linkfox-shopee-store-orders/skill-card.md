## Description:

Helps agents work with authorized Shopee store orders through LinkFox scripts covering order lookup, package and shipment views, cancellations, notes, buyer cancellation handling, bookings, invoices, and related Shopee Order APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and ecommerce support agents use this skill to inspect and manage authorized Shopee store orders, packages, buyer invoice data, FBS invoices, booking records, cancellations, order notes, and related order workflows.

### Deployment Geography for Use:

Global, with Shopee API feature availability varying by marketplace for invoice-related endpoints.

## Known Risks and Mitigations:

Risk: The skill handles Shopee order, buyer, invoice, billing, and credential-related data.

Mitigation: Install and run it only when LinkFox is trusted for that data, keep API keys out of shared logs or shell history, and rotate any exposed key.

Risk: Several operations can change live order state, including cancellation, notes, split or unsplit actions, and buyer-cancellation handling.

Mitigation: Require explicit user confirmation before running order-changing scripts and review the target shop, order identifiers, and request body before execution.

Risk: Gateway configuration controls where order and credential-bearing requests are sent.

Mitigation: Verify gateway environment variables resolve only to trusted LinkFox HTTPS hosts before use.

Risk: Automatic feedback can include conversation or order context if enabled by the agent workflow.

Mitigation: Avoid sending feedback that contains sensitive order, buyer, credential, or billing details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-orders)
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai)
- [Shopee Open Platform Order Module](https://open.shopee.com/documents/v2/v2.order.get_order_list?module=94&type=1)
- [Order API Reference](references/api.md)
- [Onboarding Reference](references/onboarding.md)
- [Cancel Order Reference](references/apis/cancel-order.md)
- [Get Order List Reference](references/apis/get-order-list.md)
- [Get Order Detail Reference](references/apis/get-order-detail.md)
- [Search Package List Reference](references/apis/search-package-list.md)
- [Upload Invoice Document Reference](references/apis/upload-invoice-doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON request parameters, stdout summaries, and saved JSON response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full API responses under a local linkfox data directory and may print either full JSON or a concise summary depending on response size.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
