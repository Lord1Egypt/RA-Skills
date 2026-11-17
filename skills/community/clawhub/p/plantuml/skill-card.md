## Description:

Generate UML, C4, architecture, timing, ER, mindmap, WBS, and Gantt diagrams with PlantUML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoxh](https://clawhub.ai/user/guoxh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to author PlantUML source for UML, C4 architecture, ER, timing, mindmap, WBS, and Gantt diagrams and render local diagram outputs with Java and Graphviz tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted .puml files runs local PlantUML and, for most non-sequence diagrams, Graphviz on diagram source.

Mitigation: Review .puml source before rendering and run untrusted diagrams in a controlled workspace.

Risk: URL-based AWS, Azure, or devicon includes can fetch mutable content from GitHub during rendering.

Mitigation: Mirror icon libraries locally or avoid URL-based includes in sensitive or offline environments.

Risk: Most non-sequence diagram types fail when Graphviz is missing or unavailable.

Mitigation: Verify Java, PlantUML, and Graphviz before use; use sequence diagrams only when Graphviz is not installed.

## Reference(s):

- [PlantUML Syntax Quick Reference](references/syntax-guide.md)
- [PlantUML Standard Library Quick Reference](references/stdlib-guide.md)
- [PlantUML Themes Gallery](https://the-lum.github.io/puml-themes-gallery/)
- [AWS Icons for PlantUML](https://github.com/awslabs/aws-icons-for-plantuml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with PlantUML code blocks and shell commands; rendered diagram files may be PNG, SVG, PDF, EPS, TXT, or UTXT.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Java and PlantUML tooling; Graphviz is required for most non-sequence diagram types.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
