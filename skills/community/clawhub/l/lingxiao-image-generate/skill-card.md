## Description:

Guides agents through e-commerce product image generation with Lingxiao MCP, including prompts for main, scene, model, and white-background images plus pricing and billing checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeli20221102-ux](https://clawhub.ai/user/mikeli20221102-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, marketers, and developers use this skill to prepare and execute paid product-image generation workflows for listing images, scene variants, model images, and white-background images. It helps agents check model pricing and account balance before generation and decide when AI-generated images are appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects a personal Lingxiao account key to the MCP server for paid image generation.

Mitigation: Install only when comfortable using that account key, check model pricing and balance first, and use confirm true only when intentionally generating a paid image.

Risk: Generated product images can create compliance or customer-trust issues when they misrepresent real materials, brand elements, or likenesses.

Mitigation: Use real photography for listings that depend on exact material details, and review generated images for platform rules, brand usage, and likeness concerns before publishing.

Risk: Automatic model fallback can produce images at a different quality tier than requested.

Mitigation: Use strictModel true when consistent quality matters, and reconcile charges against the returned billing details.

## Reference(s):

- [Lingxiao Membership and API Key](https://www.lingxiaochuhai.com/app/membership?from=mcp-trial)
- [Lingxiao Visual Factory](https://www.lingxiaochuhai.com/tools/visual-factory)
- [Lingxiao One-Click Outfit](https://www.lingxiaochuhai.com/tools/one-click-outfit)
- [Lingxiao Link Builder](https://www.lingxiaochuhai.com/tools/link-builder)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration, Markdown]

**Output Format:** [Markdown guidance with JSON configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, balance checks, billing details, and prompt guidance for single-image generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
