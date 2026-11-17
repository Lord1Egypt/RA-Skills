## Description:

Generate and modify Onshape FeatureScript code for custom CAD features, with a focus on parametric dust collection fittings such as wyes, elbows, adapters, and crosses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryko](https://clawhub.ai/user/bryko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CAD engineers use this skill to draft, modify, and troubleshoot FeatureScript for Onshape custom features and reusable fitting patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FeatureScript may create invalid or inefficient CAD geometry if used without review.

Mitigation: Review generated FeatureScript and validate geometry behavior in Onshape before relying on it.

Risk: The skill references AllertaStencil-Regular.ttf for label workflows, but the font is not included in the artifact.

Mitigation: Provide the referenced font or adjust label generation before depending on stencil label output.

## Reference(s):

- [Dust Collection Fittings Lib Spec](references/fittings.md)
- [Proven FS Patterns & Pitfalls](references/patterns.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with FeatureScript code blocks and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code is intended for review before pasting into the Onshape FeatureScript editor.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
