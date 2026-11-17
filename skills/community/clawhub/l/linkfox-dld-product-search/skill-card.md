## Description:

Searches and analyzes product listings on China's 1688 wholesale marketplace using DianLeiDa data to help agents compare suppliers, prices, sales metrics, and fulfillment options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, sourcing professionals, and agent users use this skill to research 1688 wholesale products, discover suppliers, compare pricing, and filter listings by sales, factory status, fulfillment speed, and product tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send search terms, account identifiers, phone-login data, payment actions, and feedback summaries to LinkFox services.

Mitigation: Use the skill only when that data sharing is acceptable, avoid including sensitive information in search or feedback content, and review LinkFox account actions before proceeding.

Risk: Authentication and onboarding flows can involve OTPs, API keys, and shell-profile credential persistence.

Mitigation: Do not paste OTPs or API keys unless the workflow is trusted, prefer a dedicated secret store, and avoid persisting keys in shell profiles when stronger credential management is available.

Risk: The skill supports purchase-plan and payment flows for additional LinkFox capacity.

Mitigation: Confirm the selected plan, payment method, and expected cost with the user before creating an order or displaying payment QR codes.

Risk: Custom endpoint environment variables could redirect requests away from expected LinkFox services.

Mitigation: Avoid custom endpoint environment variables unless the destination is trusted and intentionally configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-dld-product-search)
- [API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, shell command examples, and structured product-search results or summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses may be written as JSON data files while concise summaries are returned for larger result sets.]

## Skill Version(s):

1.0.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
