## Description:

Helps agents turn image-generation requests into precise prompt packages for reference-based images, portraits, product photography, e-commerce visuals, brand styling, and policy-safer rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aolio516125-spec](https://clawhub.ai/user/aolio516125-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare structured, copy-ready prompts for AI image generation workflows, especially when handling uploaded references, product visuals, model imagery, and e-commerce deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help rewrite prompts after a platform refusal, which could be misused to bypass a safety decision.

Mitigation: Use rewrites only to make otherwise allowed commercial or product imagery policy-compliant; do not use them to evade platform safety rules.

Risk: The skill includes workflows for preserving or reproducing identity details from reference images.

Mitigation: Use only authorized reference images and avoid real-person replication, face swapping, sexualized content, or age-ambiguous people.

Risk: Generated prompts may still produce inaccurate, noncompliant, or misleading image outputs.

Mitigation: Review prompt packages and generated images before publication or commercial use.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Anti-AI guide](artifact/references/anti-ai-guide.md)
- [Brand tone map](artifact/references/brand-tone-map.md)
- [E-commerce deliverables guide](artifact/references/ecommerce-deliverables.md)
- [E-commerce product polish system](artifact/references/ecommerce-product-polish-system.md)
- [Fabric guide](artifact/references/fabric-guide.md)
- [Fitted apparel guide](artifact/references/lingerie-guide.md)
- [Natural human system](artifact/references/natural-human-system.md)
- [Platform-safe generation rewrite rules](artifact/references/policy-safe-generation.md)
- [Portrait realism system](artifact/references/portrait-realism-system.md)
- [Prompt detail expansion system](artifact/references/prompt-detail-expansion-system.md)
- [Prompt output package template](artifact/references/prompt-output-package.md)
- [Prompt quality system](artifact/references/prompt-quality-system.md)
- [Reference fidelity system](artifact/references/reference-fidelity-system.md)
- [Reverse engineering guide](artifact/references/reverse-engineering.md)
- [Spatial control vocabulary](artifact/references/spatial-control.md)
- [Shopify product photography guide](https://www.shopify.com/au/blog/12206313-the-ultimate-diy-guide-to-beautiful-product-photography)
- [Amazon image requirements](https://sell.amazon.com/blog/amazon-image-requirements)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prompt package with Chinese and English prompt text; optional JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reference-role matrices, fidelity constraints, safety rewrites, negative prompts, generation notes, and quality checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
