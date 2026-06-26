## Description: <br>
Generates professional e-commerce product image workflows with platform-specific requirements, visual styles, scene types, prompts, and output files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyd4y](https://clawhub.ai/user/boyd4y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, and e-commerce operators use this skill to plan and generate product image sets for marketplaces such as Amazon, Shopify, eBay, Etsy, Taobao, JD, and Pinduoduo. The workflow analyzes product details, asks for confirmation, creates strategy outlines and prompts, and writes the resulting product-image session files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local project output files and may store optional user preferences. <br>
Mitigation: Run it in an intended workspace, review generated directories and preference files, and keep only outputs that match the product workflow. <br>
Risk: Reference images or requested styles could copy protected branding, packaging, logos, or a competitor's distinctive look. <br>
Mitigation: Use reference assets you own or are allowed to use, and review prompts and images for protected brand elements before publishing. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Quick Start Guide](QUICKSTART.md) <br>
- [Scene Guide](references/elements/scene-guide.md) <br>
- [Prompt Assembly Guide](references/workflows/prompt-assembly.md) <br>
- [Analysis Framework](references/workflows/analysis-framework.md) <br>
- [Outline Template](references/workflows/outline-template.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [Watermark Guide](references/config/watermark-guide.md) <br>
- [Amazon Platform Requirements](references/platforms/amazon.md) <br>
- [Shopify Platform Requirements](references/platforms/shopify.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown files, prompt files, generated image files, and concise progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a product-images/{product-slug}/ session directory with source material, analysis, strategy outlines, final outline, prompts, and generated images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
