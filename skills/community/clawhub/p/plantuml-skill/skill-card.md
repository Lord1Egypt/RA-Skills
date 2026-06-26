## Description: <br>
Turn natural language into uml-diagrams.org style PlantUML diagrams, including sequence, class, activity, use case, component, and state diagrams, and render them to SVG, PNG, or PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samonysh](https://clawhub.ai/user/samonysh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert natural-language requirements into PlantUML source and rendered UML diagrams for architecture, workflow, data model, and interaction documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opt-in public rendering can send diagram source to a third-party service. <br>
Mitigation: Use Docker or a local PlantUML JAR for private diagrams; enable public rendering only for non-sensitive diagrams or route it to a trusted self-hosted Kroki instance. <br>
Risk: The skill runs local rendering commands and writes generated .puml and output files. <br>
Mitigation: Review generated PlantUML and output paths before execution, and run the renderer in a workspace where Docker, Java, or curl usage is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samonysh/skills/plantuml-skill) <br>
- [uml-diagrams.org UML reference style](https://www.uml-diagrams.org) <br>
- [Kroki](https://kroki.io) <br>
- [PlantUML style evolution](https://plantuml.com/style-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with PlantUML code blocks, shell commands, and generated .puml plus SVG, PNG, PDF, or TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default SVG output; optional PNG, PDF, and TXT output; local-first rendering with opt-in remote rendering.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
