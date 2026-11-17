## Description:

Searches and filters SellerSprite Amazon product data across supported marketplaces using dimensions such as price, monthly sales, BSR rank, gross margin, ratings, fulfillment, tags, and seller origin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce researchers use this skill to query SellerSprite product data for product selection, niche discovery, competitive analysis, sales and BSR filtering, and market opportunity assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon product-research queries and optional session metadata are sent to LinkFox services.

Mitigation: Use the skill only when the user accepts sending those queries and metadata to LinkFox, and review endpoint environment variables before execution.

Risk: Generated or configured LinkFox API keys can be exposed through shell history, transcripts, or shared files.

Mitigation: Treat API keys as secrets, avoid pasting them into visible command history or logs, and rotate any key that may have been exposed.

Risk: Full API responses are persisted locally and may contain business-sensitive product research data.

Mitigation: Store outputs only in intended workspaces, avoid committing LinkFox response files, and delete local response data when it is no longer needed.

Risk: Search calls consume paid LinkFox compute credits and the onboarding flow can create payment orders.

Mitigation: Warn users about credit consumption before repeated calls and require explicit user approval before using account, plan, or payment actions.

Risk: Automatic feedback reporting could include sensitive context if reported too broadly.

Mitigation: Send feedback only when relevant to skill quality and exclude credentials, private product strategy, and unnecessary session details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sellersprite-product-search)
- [SellerSprite product search API reference](artifact/references/api.md)
- [Authentication and billing onboarding guide](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON, markdown]

**Output Format:** [Markdown guidance with JSON request examples, shell commands, and saved JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses to a local LinkFox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
