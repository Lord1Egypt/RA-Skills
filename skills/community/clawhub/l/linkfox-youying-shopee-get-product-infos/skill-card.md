## Description:

Helps agents query and filter Shopee product data across 11 marketplaces for product discovery and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and commerce analysts use this skill to search Shopee products, filter by marketplace, keyword, price, sales, category, shop, and listing attributes, and review structured product results. Agents can also guide users through LinkFox authentication or billing steps when API access or credits are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox external services for Shopee search, authentication, billing, and feedback.

Mitigation: Install and use it only when LinkFox service use is acceptable for the workspace and task.

Risk: The skill handles API keys during search and onboarding flows.

Mitigation: Use a limited API key, keep it out of shared logs and shell history, and rotate or remove it when no longer needed.

Risk: Paid credit flows can create orders and display payment QR codes.

Mitigation: Review plan, price, payment method, and order details before scanning any QR code or completing payment.

Risk: Search responses and cache files may persist locally under linkfox directories.

Mitigation: Clear stored response, session, and cache files when they are no longer needed, especially after sensitive product research.

Risk: The skill may report feedback to a separate LinkFox feedback endpoint.

Mitigation: Avoid including confidential business context in feedback content and review any automatically prepared feedback before submission where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-youying-shopee-get-product-infos)
- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API parameters, shell commands, and structured Shopee product result summaries or saved JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses may be persisted under a local linkfox session directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
