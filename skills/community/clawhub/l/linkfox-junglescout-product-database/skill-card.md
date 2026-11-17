## Description:

Queries the Jungle Scout Product Database through LinkFox to filter Amazon products across 10 marketplaces by category, price, sales, revenue, reviews, rating, BSR rank, LQS, seller type, and related product attributes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, e-commerce operators, and agent users use this skill to discover and compare Amazon product opportunities with structured filters such as marketplace, category, price, monthly sales, revenue, reviews, rating, BSR rank, LQS, seller type, and product dimensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product-query data and conversation-derived feedback may be sent to LinkFox services.

Mitigation: Install only if sharing those queries with LinkFox is acceptable, and avoid including sensitive business information unless required.

Risk: Endpoint override environment variables can redirect API, login, or billing traffic.

Mitigation: Use default endpoints or only set override variables to services you control and trust.

Risk: Authentication and billing flows involve API keys, SMS login, and payment-order steps.

Mitigation: Review login, API key storage, and payment details before proceeding; do not store keys in shared shell startup files.

Risk: The skill persists complete API responses and session metadata under a local linkfox directory.

Mitigation: Review saved files for sensitive data and manage retention according to the user's workspace policy.

## Reference(s):

- [Jungle Scout Product Database API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-junglescout-product-database)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved as local JSON files; small responses can be printed inline, while larger responses are summarized.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
