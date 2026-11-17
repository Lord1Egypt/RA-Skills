## Description:

Helps agents manage Shopee Shop Category data through LinkFox's Shopee developer proxy, including creating, updating, listing, and deleting shop categories and category item lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee sellers, store operators, and developers use this skill to manage authorized store categories and the products assigned to those categories. It is intended for agents that need to call LinkFox scripts or produce guidance for Shopee shop-category workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses credential-bearing LinkFox and Shopee API calls and can guide API-key generation.

Mitigation: Use a secure secret manager for API keys, avoid exposing phone or SMS codes in shared logs, and install only when the LinkFox publisher and workflow are trusted.

Risk: Custom LINKFOX_* gateway URL environment variables can change where credential-bearing requests are sent.

Mitigation: Leave gateway URL overrides unset unless the destination is explicitly trusted and reviewed.

Risk: The skill can assist with billing orders and payment flows.

Mitigation: Verify the selected plan, payment method, and order details before proceeding with payment.

Risk: Full API responses are persisted under local linkfox output directories and may include sensitive store or business data.

Mitigation: Restrict access to the workspace output directory and delete saved response files when they are no longer needed.

## Reference(s):

- [Shop Category API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [Shopee Open Platform Shop Category documentation](https://open.shopee.com/documents/v2/v2.shop_category.add_shop_category?module=101&type=1)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-shop-category)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full responses under a linkfox session directory and print either the full JSON response or a summary depending on response size.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
