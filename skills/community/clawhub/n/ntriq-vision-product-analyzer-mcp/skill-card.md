## Description:

Analyze product images: identify items, extract specs, compare features, generate descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and e-commerce operators use this skill to analyze product images, extract specifications, compare variants or competitor products, and draft product descriptions for catalogs, returns, and feature research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images may be sent to the documented paid external service even though the skill text also describes local analysis.

Mitigation: Confirm whether local and hosted modes are separate before use, and avoid submitting confidential, prototype, inventory, competitor, private URL, or signed-link images unless external transmission is acceptable.

Risk: Using the documented endpoint may incur the stated per-call USDC payment.

Mitigation: Review payment controls and expected usage volume before enabling the endpoint in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-vision-product-analyzer-mcp)
- [Publisher profile](https://clawhub.ai/user/ntriq-gh)
- [ntriq x402 homepage](https://x402.ntriq.co.kr)
- [ntriq service catalog](https://x402.ntriq.co.kr/services)
- [Vision product endpoint](https://x402.ntriq.co.kr/vision-product)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON and text product analysis with identified products, specifications, comparisons, descriptions, and SEO tags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts up to 10 product images, optional task selections, category hints, and competitor images.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
