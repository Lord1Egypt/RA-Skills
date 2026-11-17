## Description:

Analyzes product listing images with LinkFox multimodal AI to extract structured visual attributes such as color, material, shape, style, and image prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, operators, and agents use this skill to turn product image URLs and prompts into structured product attributes and attribute-group summaries. It supports image-based listing analysis workflows where product data is explicitly supplied by the current pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, prompts, product records, and related context may be sent to LinkFox services for multimodal analysis.

Mitigation: Use only product data approved for LinkFox processing, and avoid confidential catalog data unless third-party processing is approved.

Risk: The skill uses LinkFox API credentials, and onboarding guidance can place API keys in shell startup files.

Mitigation: Store credentials only in approved user-local or managed secret locations, and avoid shared or logged shell environments.

Risk: Full responses and cached results are persisted locally in LinkFox session and cache directories.

Mitigation: Run the skill from an appropriate workspace and delete response or cache files when local retention is not acceptable.

Risk: Image analysis consumes LinkFox compute credits, and the onboarding helper can create payment orders.

Mitigation: Confirm user intent before additional analysis or billing actions, and avoid automatic retries that may increase cost.

Risk: Feedback reporting can send issue, sentiment, or improvement details to LinkFox.

Mitigation: Keep feedback free of confidential details and disclose external reporting when relevant to the user's workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-multimodal-extract-attributes)
- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses saved to local files, concise stdout summaries for large responses, and Markdown tables or summaries for presentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are written under a LinkFox session data directory; repeated calls with the same parameters may use a 24-hour local cache unless disabled.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
