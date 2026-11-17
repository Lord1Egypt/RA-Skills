## Description:

Lists the in-store products for a TikTok Shop seller by sellerId, including product titles, prices, sales and GMV across multiple time windows, ratings, reviews, commission rate, listing date, channel, and category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and commerce analysts use this skill to inspect a known TikTok Shop store's product catalog and compare product performance by sales, GMV, price, rating, reviews, and commission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LinkFox API access and may expose account credentials or billing flows if handled in chat-visible contexts.

Mitigation: Prefer manual API-key setup outside shared logs, confirm that the user intentionally trusts the LinkFox service, and avoid entering SMS codes or creating payment orders unless explicitly requested.

Risk: Full seller-query responses are saved locally and may include commercially sensitive product analytics.

Mitigation: Run the skill only in an appropriate workspace and review saved JSON files before sharing or retaining them.

Risk: Repeated calls consume compute credits and may trigger billing-sensitive workflows.

Mitigation: Tell users when additional calls will consume credits and ask before continuing with extra pagination, retries, or payment-related steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-list-seller-product)
- [EchoTik Seller Product API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a sellerId and LinkFox API key; pageSize must be a multiple of 10 up to 100, and the skill consumes 5 compute credits per call.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
