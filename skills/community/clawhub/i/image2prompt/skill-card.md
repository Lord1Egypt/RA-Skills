## Description:

Analyze images and generate detailed prompts for image generation. Supports portrait, landscape, product, animal, illustration categories with structured or natural output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhang-shubo](https://clawhub.ai/user/zhang-shubo)

### License/Terms of Use:


## Use Case:

External users, developers, and prompt engineers use this skill to analyze images and generate natural-language or structured JSON prompts for AI image generation. It supports category-specific descriptions and optional dimension tags for prompt libraries or downstream prompt composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portrait analysis can encourage demographic, body-description, or other sensitive visual descriptions.

Mitigation: Use the skill only on images you have the right to analyze, avoid profiling private people or inferring sensitive attributes without consent, and prefer non-sensitive visual descriptions.

Risk: Generated prompts may reproduce details from images whose use is not authorized.

Mitigation: Confirm that image inputs are authorized for analysis and downstream prompt generation before using the output.

## Reference(s):

- [Image2Prompt OpenClaw documentation](https://docs.openclaw.ai/tools/image2prompt)
- [Image2Prompt ClawHub listing](https://clawhub.ai/zhang-shubo/skills/image2prompt)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or structured JSON descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include category labels, detailed visual prompt text, structured visual attributes, and optional dimension tags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
