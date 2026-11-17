## Description:

Turn natural language into uml-diagrams.org style PlantUML diagrams and render them to SVG, PNG, PDF, or ASCII text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn text descriptions of systems, workflows, and interactions into PlantUML source and rendered diagrams. It is useful for producing sequence, class, activity, use case, component, deployment, state, Gantt, and mind map diagrams in a consistent UML reference style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer can execute a local PlantUML JAR from the working directory or use a mutable Docker image.

Mitigation: Use a pinned, trusted Docker image or an explicitly verified PlantUML JAR, and avoid running the renderer from untrusted project directories.

Risk: Opt-in public server rendering sends diagram source to a third-party service.

Mitigation: Do not use public server rendering for confidential diagrams; review PLANTUML_PUBLIC_SERVER before enabling remote rendering and prefer local or trusted self-hosted backends.

## Reference(s):

- [ClawHub Plantuml Skill](https://clawhub.ai/samonysh/skills/plantuml-skill)
- [uml-diagrams.org UML Reference Style](https://www.uml-diagrams.org)
- [Kroki Diagram Rendering](https://kroki.io)
- [PlantUML Style Evolution](https://plantuml.com/style-evolution)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files, Markdown]

**Output Format:** [Markdown guidance with PlantUML code blocks and rendered SVG, PNG, PDF, or TXT diagram files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default rendering is local-first with Docker or a local PlantUML JAR; remote Kroki rendering is opt-in.]

## Skill Version(s):

1.7.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
