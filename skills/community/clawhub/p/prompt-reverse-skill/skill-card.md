## Description:

Convert image to structured prompts for multiple AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keweizhan](https://clawhub.ai/user/keweizhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and creators use this skill to analyze input images, extract structured visual features, and produce prompts adapted for generative image models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images may be sent to an external vision/API provider for analysis.

Mitigation: Use only images you are permitted to process and avoid sensitive, personal, confidential, or proprietary content unless the provider's data handling terms are approved.

Risk: Generated structured data or prompts may omit or misstate visual details from the source image.

Mitigation: Review the structured output and model-specific prompts before using them in downstream generation workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keweizhan/skills/prompt-reverse-skill)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON and model-specific prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated from an input image path; prompts may be adapted for Stable Diffusion, Midjourney, and DALL-E.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
