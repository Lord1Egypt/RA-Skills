## Description:

Transforms white-background product photos into realistic lifestyle scenes while preserving product details and matching the scene's lighting and shadows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce teams use the skill to create realistic lifestyle scenes from white-background product photos, optionally compositing a supplied background while keeping the product's appearance consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and prompts may be sent to external image services, and the scan was incomplete, leaving some code only partially analyzed.

Mitigation: Before use, determine whether sending the images and prompts to the named providers and allowing the required network and environment access is acceptable; account for the portions that were only partially reviewed.

## Reference(s):

- [Provider CLI guide](references/provider-cli.md)
- [Image model flags](references/model-flags.md)
- [dLazy ecommerce skills repository](https://github.com/dlazy-ai/ecommerce-skills)
- [dLazy CLI repository](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Guidance]

**Output Format:** [JPEG image files and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a product image and optionally a background image; examples use square or portrait output sizes.]

## Skill Version(s):

1.0.33 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
