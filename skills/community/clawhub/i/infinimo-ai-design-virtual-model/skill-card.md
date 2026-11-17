## Description:

Generate virtual model showcase images via Infinimo AI Design from a source photo, optional background, and prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create fashion lookbook, model swap, and on-model product presentation images from a real-person or mannequin source photo without a live shoot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends selected photos, optional background images, prompts, and an Infinimo API token to the declared external API.

Mitigation: Use the skill only with images and prompts appropriate for that provider, avoid sensitive photos unless retention and privacy terms are acceptable, and keep the API token scoped and protected.

Risk: The documented log-delete endpoint removes generation history.

Mitigation: Use log deletion only when intentionally removing generation records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/infinimo-ai-design-virtual-model)
- [Infinimo AI Design](https://design.infinimo.ai/?source=q-i-d-clawhub)
- [Infinimo API key](https://design.infinimo.ai/api-key?source=q-i-d-clawhub)
- [Virtual Model Response Schema](references/response-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and API workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces upload, generation, and polling guidance that returns image URLs and submitted parameters after asynchronous generation completes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
