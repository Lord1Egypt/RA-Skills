## Description:

Turns presales requirements, meeting notes, and solution materials into editable business capability blueprints, swimlane flows, application architecture diagrams, and exports such as JSON, HTML viewers, SVG, draw.io, Excalidraw, and Mermaid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and solution engineers use this skill to convert raw presales inputs into canonical blueprint JSON and visual outputs for review, editing, and downstream report or slide workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted blueprint content can inject JavaScript into the generated HTML viewer.

Mitigation: Review or fix generated viewers before opening blueprints from untrusted sources, and avoid generating or opening HTML viewers for third-party blueprint JSON until entity IDs are validated or escaped correctly.

## Reference(s):

- [Business Blueprint Skill page](https://clawhub.ai/kaisersong/skills/kai-business-blueprint)
- [Blueprint schema](references/blueprint-schema.md)
- [Entities schema](references/entities-schema.md)
- [Systems schema](references/systems-schema.md)
- [Architecture design system](references/architecture-design-system.md)
- [Test and eval strategy](references/test-and-eval-strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, HTML, SVG, draw.io, Excalidraw, Mermaid, and shell-command artifacts generated through the skill scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated project artifacts are intended for projects/workspace/ rather than the repository root.]

## Skill Version(s):

0.15.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
