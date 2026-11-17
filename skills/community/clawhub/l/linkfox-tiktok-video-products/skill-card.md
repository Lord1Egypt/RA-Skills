## Description:

Helps agents query TikTok creator shop, showcase, and live-bag product lists through LinkFox and return product IDs for shoppable video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and agents use this skill to search a creator's linked shop products or list showcase and live-bag products. It returns product IDs and pagination data needed by downstream shoppable video precheck and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles TikTok creator product data, account onboarding data, API keys, and billing interactions.

Mitigation: Install only if you trust linkfox-ai; prefer a dedicated authentication or billing skill, or the first-party LinkFox site, for login and payments.

Risk: Endpoint override environment variables can redirect requests away from the documented LinkFox services.

Mitigation: Avoid endpoint override environment variables unless testing intentionally in a controlled environment.

Risk: Plaintext shell-profile API key setup can expose credentials.

Mitigation: Use temporary environment variables or a secrets manager where possible, and avoid storing API keys in shell startup files.

Risk: Automatic feedback reporting can send user-provided context outside the current agent session.

Mitigation: Review feedback payloads before allowing them to be submitted.

## Reference(s):

- [API Reference](references/api.md)
- [Onboarding Guide](references/onboarding.md)
- [TikTok Shop Get Shop Products API](https://partner.tiktokshop.com/docv2/page/get-shop-products-202509)
- [TikTok Shop Get Showcase Products API](https://partner.tiktokshop.com/docv2/page/get-showcase-products-202405)
- [Shoppable Video Integration Solutions V2025.Q4.01](https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-video-products)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product IDs, source product data, pagination fields, authentication guidance, and optional local file output for large responses.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
