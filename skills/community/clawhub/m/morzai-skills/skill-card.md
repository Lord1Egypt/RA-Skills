## Description: <br>
Morzai Skills routes ecommerce image requests to specialized Morzai workflows for apparel recoloring, garment retouching, clothing cleanup, and product listing image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morzai-app](https://clawhub.ai/user/morzai-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers and agent users use this skill to route product-image requests to the right Morzai workflow for recoloring garments, cleaning apparel photos, adjusting clothing presentation, or generating marketplace listing images from product photos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product images, reference images, image URLs, and listing context may be sent to Morzai/Lumo remote services or through the Morzai CLI. <br>
Mitigation: Use the skill only with assets approved for the provider's data handling; avoid unreleased designs, confidential supplier assets, and sensitive credentials unless the provider has been reviewed and trusted. <br>
Risk: The workflows require OAuth, API keys, or CLI authentication, which can expose credentials if printed or stored carelessly. <br>
Mitigation: Use environment variables or the CLI authentication flow, keep logs redacted, and do not expose API keys, authorization headers, signed upload URLs, tokens, cookies, or full credential values in user-facing output. <br>
Risk: Generated ecommerce images can be inaccurate, over-processed, or unsuitable for a specific marketplace rule set. <br>
Mitigation: Review outputs before publication, keep platform readability and compliance requirements in scope, and use the skill's fallback guidance when inputs, credentials, uploads, or result structures fail. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/morzai-app/morzai-skills) <br>
- [Morzai AI E-commerce Skills README](README.md) <br>
- [Command Routing Map](api/commands.json) <br>
- [Root Skill Definition](SKILL.md) <br>
- [Apparel Recolor Skill](skills/apparel-recolor/SKILL.md) <br>
- [Garment Retouch Skill](skills/garment-retouch/SKILL.md) <br>
- [Clothing Adjustment Skill](skills/clothing-adjustment/SKILL.md) <br>
- [Ecommerce Product Kit Skill](skills/ecommerce-product-kit/SKILL.md) <br>
- [Recolor Intent Mapping](skills/apparel-recolor/references/intent-mapping.md) <br>
- [Garment Retouch Intent Mapping](skills/garment-retouch/references/intent-mapping.md) <br>
- [Clothing Adjustment Intent Mapping](skills/clothing-adjustment/references/intent-mapping.md) <br>
- [Ecommerce Output Spec](skills/ecommerce-product-kit/references/output-spec.md) <br>
- [Ecommerce Error Fallback](skills/ecommerce-product-kit/references/error-fallback.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown summaries with CLI commands, remote service requests, and local file paths to generated image outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce generated product images or listing-set folders through Morzai/Lumo services; requires user-supplied product images and, for some workflows, Morzai CLI authentication.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact manifests also report 1.0.0 and 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
