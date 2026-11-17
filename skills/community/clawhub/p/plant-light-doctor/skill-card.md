## Description:

Estimates monthly window light, matches houseplants to available light, and suggests grow-light specifications when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Plant owners and indoor gardeners use this skill to assess seasonal light at a window, choose suitable houseplants, investigate possible light-related symptoms, and size supplemental grow lights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Estimated light levels can misclassify plant suitability or lead to poorly sized grow lights when local shading differs from the model.

Mitigation: Confirm the window details and compare estimates with actual light measurements before making consequential plant or lighting purchases.

## Reference(s):

- [Plant Light Doctor on ClawHub](https://clawhub.ai/voronindenis5/skills/plant-light-doctor)
- [Light physics and measurement methods](references/light-physics.md)
- [Plant DLI requirements and symptom guide](references/plant-dli-table.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown explanations with monthly DLI estimates, plant suitability verdicts, and optional grow-light specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on window orientation, latitude, floor, obstruction, glazing, and climate; the model has approximately ±30% accuracy.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
