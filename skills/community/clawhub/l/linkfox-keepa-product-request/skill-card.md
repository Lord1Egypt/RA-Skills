## Description:

Retrieves structured Amazon product details by ASIN through LinkFox's Keepa product request API, including pricing, title, Item Highlights, images, listing date, dimensions, FBA fees, sales rank, and monthly sales history when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, ecommerce analysts, and agent users use this skill to retrieve and compare ASIN-level product data across supported Amazon marketplaces. It is suited for product-detail lookup, competitor comparison, pricing review, sales trend checks, physical specification review, category checks, and FBA fee inspection when users provide one or more ASINs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle product queries, onboarding data, API credentials, billing actions, local response files, and automatic feedback submissions through LinkFox services.

Mitigation: Install and run it only when those data flows are acceptable for the task and organization.

Risk: Phone/SMS login and payment flows may be initiated through an agent when resolving authentication or billing issues.

Mitigation: Use those flows only after explicit user intent is confirmed, and prefer self-service account management when appropriate.

Risk: API keys and session-related environment variables affect authentication, storage grouping, and outbound requests.

Mitigation: Rotate any API key exposed in transcripts and avoid running with untrusted LINKFOX_* or SESSION_ID environment variables.

Risk: Full API responses are persisted locally in a linkfox session data directory.

Mitigation: Review saved response files for sensitive product or account-adjacent data and manage retention according to local policy.

## Reference(s):

- [Keepa-亚马逊-商品详情 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-keepa-product-request)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown summaries and tables with saved JSON response files and optional inline JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries accept up to 5 ASINs per request, use numeric Amazon marketplace IDs, may include optional history, cache responses for 24 hours, and write full responses under a local linkfox session data directory.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
