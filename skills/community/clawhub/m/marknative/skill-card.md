## Description:

Render Markdown into paginated PNG/SVG without a browser using marknative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twoface2014](https://clawhub.ai/user/twoface2014)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate Node/TypeScript guidance for converting Markdown into deterministic paginated PNG or SVG output without relying on a browser runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose installing the mutable npm package `marknative` and its rendering backend.

Mitigation: Pin `marknative` to a reviewed version and install it in a restricted project environment before use.

Risk: Runtime setup can vary across Node, TypeScript, ESM, and `skia-canvas` system dependencies.

Mitigation: Verify the minimal rendering example in the target environment before using the skill for batch exports.

Risk: Some runtime instructions in the artifact are written in Chinese.

Mitigation: Use the bundled README or a reviewed translation when the operator cannot read the original instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twoface2014/skills/marknative)
- [Publisher profile](https://clawhub.ai/user/twoface2014)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Markdown rendering options such as PNG or SVG output format and painter configuration.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
