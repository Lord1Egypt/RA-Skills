## Description:

This skill helps agents manage Shopee store listings through LinkFox scripts for Shopee Product APIs, including category lookup, item creation and updates, pricing, stock, promotion boosts, search, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to query and manage authorized Shopee store product listings, SKUs, prices, stock, comments, and related Product API resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live Shopee listing changes, including item creation, deletion, price changes, stock changes, comment replies, and promotion boosts.

Mitigation: Review write, delete, billing, and feedback actions explicitly before execution and use least-privilege Shopee and LinkFox credentials.

Risk: The skill handles LinkFox API keys, login material, and store authorization context.

Mitigation: Run it only in trusted workspaces with trusted environment variables and avoid exposing saved outputs or command arguments that contain credentials.

Risk: The skill stores full API responses locally, which may include store or listing data.

Mitigation: Treat local response files as sensitive operational data and clean or protect the linkfox session directory according to the user's data-retention needs.

Risk: The security scan verdict is suspicious because the skill includes credential, billing, feedback, and persistent local-data behavior.

Mitigation: Review the skill before installing or using it with real Shopee stores, following the security guidance from server evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-product)
- [Shopee Product API index](https://open.shopee.com/documents/v2/v2.product.get_category?module=89&type=1)
- [Product API reference](references/api.md)
- [Onboarding and authentication guidance](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses or saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full API responses under a local linkfox session data directory and may print summaries for large responses.]

## Skill Version(s):

1.0.6 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
