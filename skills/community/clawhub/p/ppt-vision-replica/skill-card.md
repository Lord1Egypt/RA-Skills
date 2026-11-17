## Description:

PPT Vision Replica turns PPT screenshots or infographics into editable PPTX files using VLM region analysis, coordinate mapping, and PNG fallback rendering for complex shapes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allergro](https://clawhub.ai/user/allergro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to reconstruct editable PowerPoint decks from static slide screenshots or infographics. It can also guide slide-region analysis, pixel-to-PPT coordinate mapping, complex-shape fallback rendering, and PPTX generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots are sent to a configured VLM service, which can expose sensitive slide content.

Mitigation: Do not process confidential slides; confirm the configured VLM endpoint and data-handling expectations before use.

Risk: Untrusted model output can cause local image file paths to be embedded in generated presentations.

Mitigation: Run the skill in an isolated working directory, validate image paths before PPTX generation, and avoid sharing PPTX files generated from adversarial or untrusted images until image-path validation is added.

Risk: The workflow reads and writes local PPTX and image files.

Mitigation: Use a dedicated workspace for inputs, temporary PNG files, and generated PPTX output, then review files before distribution.

## Reference(s):

- [PPT Vision Replica on ClawHub](https://clawhub.ai/allergro/skills/ppt-vision-replica)
- [Region schema](references/region_schema.json)
- [Images2Slides paper (arXiv:2602.07645)](https://arxiv.org/abs/2602.07645)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON region data, JavaScript and Python snippets, shell commands, and generated PPTX or PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js with pptxgenjs; complex-shape fallback uses Python with Pillow and may write temporary PNG files and output PPTX files.]

## Skill Version(s):

1.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
