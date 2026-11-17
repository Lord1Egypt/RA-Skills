## Description:

Queries Sorftime data by Amazon ASIN to return product details, marketplace metrics, and historical trends across 14 Amazon marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce analysts use this skill to look up ASIN-level product details, pricing, BSR, sales, profit, FBA fee, and promotion trends for product checks and competitor comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASIN queries and account-related data may be sent to LinkFox and Sorftime services.

Mitigation: Install only if that data sharing is acceptable for the intended workflow and avoid submitting sensitive account or product information unnecessarily.

Risk: The skill can guide SMS login, API key setup, and payment-order flows.

Mitigation: Use those flows only when explicitly intended, treat printed API keys as exposed, and prefer a managed secret store instead of shell startup files.

Risk: Product detail and trend queries consume LinkFox/Sorftime credits, and longer trend ranges can cost more.

Mitigation: Confirm cost-sensitive calls with the user, use cached results when appropriate, and avoid repeated probing after failures or empty results.

Risk: Automatic feedback reporting may send usage feedback to LinkFox.

Mitigation: Review or disable feedback reporting where policy requires user approval before transmitting feedback.

## Reference(s):

- [Sorftime Product Detail API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sorftime-amazon-product-detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, shell commands, and JSON API response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved as JSON under a LinkFox session directory; large responses print a summary unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
