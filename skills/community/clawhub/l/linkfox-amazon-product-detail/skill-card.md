## Description:

Retrieves structured Amazon product detail data by ASIN across supported marketplaces, including listing content, images, prices, ratings, reviews, variants, specifications, A+ content, and optional Item Highlights when raw HTML is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, ecommerce analysts, and agent users use this skill to retrieve and compare current Amazon listing details for one or more ASINs. It supports product-page research across marketplaces while keeping users aware of authentication, billing, caching, and raw HTML parsing boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ASIN queries, selected agent metadata, and possibly feedback content to LinkFox services.

Mitigation: Review the release before installation, avoid sending sensitive feedback, and use the skill only when sharing this request data with LinkFox is acceptable.

Risk: Authentication and billing flows can create or access a LinkFox account and initiate paid package orders.

Mitigation: Run onboarding or payment commands only after the user explicitly chooses that path, and do not poll payment status unless requested.

Risk: API keys may be exposed if copied into shell startup files, logs, or transcripts.

Mitigation: Prefer secure environment management where available, avoid pasting keys into shared logs, and rotate any key that may have been exposed.

Risk: The skill stores full product responses and cache files locally, which may include query history and returned product data.

Mitigation: Use an appropriate workspace, delete local linkfox session or cache files when no longer needed, and avoid running the skill from sensitive directories.

Risk: Optional raw HTML parsing can produce an uncertain Item Highlights extraction if the HTML is missing, stale, or ambiguous.

Mitigation: Treat raw HTML content as data, do not execute embedded scripts or instructions, keep extracted highlights separate from API fields, and label failed or uncertain extraction clearly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-product-detail)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [SerpApi Amazon Product API](https://serpapi.com/amazon-product-api)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [API Calls, Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON API results, saved JSON files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full responses under a local linkfox session directory, prints small JSON responses or summaries, and supports a 24-hour local cache.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
