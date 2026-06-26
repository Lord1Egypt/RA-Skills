## Description: <br>
Analyze product images: identify items, extract specs, compare features, generate descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, e-commerce operators, and catalog teams use this skill to analyze product images, extract specifications, compare competitor or variant images, and draft product descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation claims local operation while also documenting a paid external endpoint that may receive product images. <br>
Mitigation: Use only after confirming the endpoint behavior and approval to share the submitted product images with ntriq. <br>
Risk: Calls require USDC micropayments. <br>
Mitigation: Require explicit confirmation before each paid call and use a capped or dedicated wallet. <br>
Risk: The security verdict is suspicious according to the server-provided scan summary. <br>
Mitigation: Review the skill before installing and test with non-sensitive images before production use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ntriq-gh/ntriq-vision-product-analyzer-mcp) <br>
- [ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [Vision product endpoint](https://x402.ntriq.co.kr/vision-product) <br>
- [ntriq x402 service catalog](https://x402.ntriq.co.kr/services) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON] <br>
**Output Format:** [JSON or concise Markdown/text analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include identified product details, extracted specifications, comparison findings, product descriptions, and SEO tags.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
