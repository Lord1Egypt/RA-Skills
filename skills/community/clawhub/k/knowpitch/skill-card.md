## Description:

KnowPitch turns a knowledge domain into a football formation for systematic learning, producing a formation SVG, ELI5-style player cards, and a coach tactics board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyabao](https://clawhub.ai/user/iyabao)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and knowledge workers use this skill to decompose a knowledge topic into football-position roles, then study it through an SVG formation diagram, plain-language player cards, and a learning-path tactics board.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python renderer and writes SVG output files.

Mitigation: Review the JSON input and output path before running the renderer, and keep generated files in an intended workspace location.

Risk: The skill is Chinese-first by default, which may not match every user's review or deployment language.

Mitigation: Ask for the desired output language explicitly when Chinese output is not appropriate.

## Reference(s):

- [Formation Diagram JSON Schema](artifact/references/json-schema.md)
- [Formation Options](artifact/references/formations.md)
- [Position Role Mapping](artifact/references/positions.md)
- [Complete Examples](artifact/references/examples.md)
- [KnowPitch ClawHub Page](https://clawhub.ai/iyabao/skills/knowpitch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON input examples, shell commands, and generated SVG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ for local SVG generation; default output language is Chinese unless another language is requested.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
