## Description:

Create exquisite infographics from user-uploaded files or given text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newtoolai](https://clawhub.ai/user/newtoolai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to turn uploaded documents or supplied text into infographic syntax and rendered SVG/PNG visual assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Node rendering tools and creates .md, .svg, and .png files.

Mitigation: Install only in environments where local rendering is acceptable, use explicit safe output paths, and review generated files before sharing or deployment.

Risk: Oversized or untrusted SVG inputs can stress local rendering tools.

Mitigation: Avoid untrusted oversized SVG inputs and apply normal file-size controls before conversion.

Risk: Bundled templates include Chinese sample content that may influence generated examples.

Mitigation: Ask the agent to generate content in the target language and review final text for audience fit.

## Reference(s):

- [Mindchart on ClawHub](https://clawhub.ai/newtoolai/skills/mindchart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Infographic DSL in a Markdown code block, with generated .md, .svg, and .png files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Node or Bun environment with @antv/infographic, opentype.js, and sharp for local rendering.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
