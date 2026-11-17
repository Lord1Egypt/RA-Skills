## Description:

Fetches a single TikTok Shop seller profile by sellerId, including sales and GMV by period, followers, ratings, fulfillment metrics, products, categories, and promotion reach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and ecommerce analysts use this skill to retrieve a full profile for a known TikTok Shop seller and compare store performance, health, and reach metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Seller IDs, runtime metadata, and account credentials may be shared with LinkFox services.

Mitigation: Use the skill only with data suitable for LinkFox processing, and keep API keys out of agent transcripts and shell history.

Risk: Endpoint override environment variables can route requests away from the default LinkFox services.

Mitigation: Avoid endpoint overrides unless the destination has been reviewed and approved.

Risk: Account setup, payment QR, and feedback flows are broader than a seller detail lookup.

Mitigation: Confirm any plan purchase, payment action, or feedback submission with the user before proceeding.

## Reference(s):

- [EchoTik-TikTok店铺详情 API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-seller-detail)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [JSON response saved to file, with full JSON or a concise stdout summary depending on response size.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sellerId, uses a 24-hour local cache for repeated parameter sets, and consumes 5 LinkFox credits per lookup.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
