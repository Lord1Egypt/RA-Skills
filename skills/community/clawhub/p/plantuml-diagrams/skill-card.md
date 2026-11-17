## Description:

Plantuml helps agents create PlantUML source for UML, architecture, data, planning, and UI wireframe diagrams, with guidance on themes, styling, preprocessing, and PNG/SVG/ASCII rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holdyounger](https://clawhub.ai/user/holdyounger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to have an agent choose and author PlantUML diagram source for software design, architecture, data models, workflows, schedules, and UI wireframes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preview workflow can send diagram contents to a public PlantUML server.

Mitigation: Use local PlantUML or an approved internal renderer for confidential system diagrams.

Risk: The preview helper script has weak path validation for diagram names.

Mitigation: Run scripts/render_preview.py only with trusted diagram names until path validation is added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/holdyounger/skills/plantuml-diagrams)
- [PlantUML Best Practices](references/best-practices.md)
- [PlantUML Diagram Type Cheat Sheet](references/cheatsheet.md)
- [PlantUML Online Renderer](https://www.plantuml.com/plantuml)
- [PlantUML Themes Gallery](https://the-lum.github.io/puml-themes-gallery/themes/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown containing PlantUML code blocks and optional rendering commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces .puml source intended for PNG, SVG, or ASCII rendering.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
