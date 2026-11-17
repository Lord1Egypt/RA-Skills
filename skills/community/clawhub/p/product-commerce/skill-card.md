## Description:

Search products, check prices and stock, create quotes, place orders - multi-tenant B2B/B2C commerce API

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce agents and buyers use this skill to search heating fuel and wood products, check live prices and availability, draft quotes, place orders, and check order status through the SputnikX commerce API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create quotes and place paid orders, including high-value transactions.

Mitigation: Require explicit user approval that shows price, quantity, destination, and total cost before creating a quote or placing an order.

Risk: The skill interacts with an external commerce service and may disclose order or delivery details to that service.

Mitigation: Use only in workflows where sharing product, quantity, tenant, and delivery information with the commerce provider is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenbymyai-max/skills/product-commerce)
- [Publisher profile](https://clawhub.ai/user/drivenbymyai-max)
- [SputnikX homepage](https://sputnikx.xyz)
- [SputnikX commerce API base URL](https://sputnikx.xyz/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with inline bash examples and commerce API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create quotes and place paid orders through an external commerce API when invoked by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
