## Description:

使用gpt-image-2生成海报，支持10种设计风格。每种风格精调了prompt，直接出图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and content developers use this skill to turn a supplied title into a vertical 3:4 poster prompt across ten predefined visual styles, then generate a JPEG poster for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow fixes defaults for model, JPEG format, medium quality, and 1536x2048 output, which may not match every publishing channel or quality requirement.

Mitigation: Confirm output format, quality, and dimensions with the user before generation when channel requirements differ from the documented defaults.

Risk: The skill is written as a Chinese-language poster workflow and may be less suitable for multilingual prompt generation without adaptation.

Mitigation: Review or localize the selected style prompt before generation when the requested poster title or audience is not Chinese-language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afeicn/skills/poster-style-generator)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls]

**Output Format:** [Image-generation prompt guidance and a generated JPEG image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses openai/gpt-image-2 with JPEG medium quality and 1536x2048 portrait output by default.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
