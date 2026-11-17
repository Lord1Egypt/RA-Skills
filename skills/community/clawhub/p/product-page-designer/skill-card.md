## Description:

Designs complete product detail pages for consumer electronics, including product-page sections, image prompts, visual asset guidance, specifications, FAQ content, and layout notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonbuilds](https://clawhub.ai/user/johnsonbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams, designers, and developers use this skill to draft consumer-electronics product detail pages and supporting image-generation prompts. It is intended to produce ready-to-review Markdown content, layout guidance, and optional implementation guidance for web teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents toward an unpinned third-party CLI for image generation.

Mitigation: Review and pin the CLI version before use, and run image-generation commands in a restricted environment.

Risk: Image workflows may upload local images or generated assets outside the workspace.

Mitigation: Confirm which files may be uploaded before running image commands, and avoid using sensitive workspace content as image inputs.

Risk: Generated product pages may include inaccurate product specifications, claims, or generated branding artifacts.

Mitigation: Verify all specifications, marketing claims, image text, and logos before publishing or handing content to developers.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/johnsonbuilds/awesome-hermes-skills/tree/main/creative/product-page-designer)
- [AI Brand Hallucination Reference](references/brand-hallucination-fix.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, image prompts, optional shell commands, and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated image URLs when image generation is used; generated specifications, claims, and images require human review before publication.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
