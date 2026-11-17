## Description:

Generate PowerPoint presentations with AI images using Gemini. Each slide is a full-bleed image. Use for creating visual presentations, slideshows, or image-based decks from a topic prompt. Requires --slides N.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinpeng](https://clawhub.ai/user/jinpeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create image-based PowerPoint decks from a topic prompt, with Gemini generating both the slide narrative and full-bleed slide images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation prompts and generated slide content are sent to Gemini or the configured proxy endpoint.

Mitigation: Avoid confidential material unless external processing is approved, and use an approved endpoint and credential handling process.

Risk: Runtime dependencies and local output files can affect supply-chain reproducibility and data handling.

Mitigation: Run the skill in an isolated environment with pinned dependencies when reproducibility matters, and review generated .pptx, image, JSON, and log files before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinpeng/skills/nano-banana-pro-pptx)
- [Publisher profile](https://clawhub.ai/user/jinpeng)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [PowerPoint .pptx files with generated PNG slide images, JSON planning artifacts, and request logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gemini API key; supports 1 to 50 slides and 1K, 2K, or 4K image resolution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
