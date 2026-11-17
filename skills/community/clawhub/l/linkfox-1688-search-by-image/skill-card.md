## Description:

Searches 1688 by product image to help cross-border sellers find visually similar supplier listings with prices, minimum order quantities, sales, repurchase rates, scores, and seller badges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, cross-border sellers, and sourcing agents use this skill to search 1688 with a product image URL or uploaded local image, compare visually similar supplier listings, and apply supported filters or sorting during supplier discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox credentials for authenticated API calls and bundled account onboarding flows.

Mitigation: Install and run it only when you trust LinkFox as the service provider, keep API keys scoped to this use case, and avoid sharing SMS codes unless you initiated the login flow.

Risk: Local image inputs may be uploaded to a public URL for search.

Mitigation: Use only images that are acceptable to expose publicly for the upload validity window, and avoid confidential product images unless disclosure is approved.

Risk: Full search responses are saved locally and may include supplier, product, pricing, and query context.

Mitigation: Review the LinkFox session output directory after use and remove retained JSON files when they are no longer needed.

Risk: Searches consume LinkFox compute credits and billing flows may be triggered for insufficient balance.

Mitigation: Confirm additional searches, pagination, and recharge actions with the user before proceeding.

Risk: Custom LINKFOX_* endpoint environment variables can redirect traffic to alternate destinations.

Mitigation: Leave default endpoints in place unless the destination is explicitly trusted and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-1688-search-by-image)
- [1688-以图搜图 API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown tables or JSON summaries, with complete API responses saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may upload local images to public URLs, consumes LinkFox compute credits, uses 24-hour local caching for repeated parameter sets, and persists full search responses under a LinkFox session directory.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
