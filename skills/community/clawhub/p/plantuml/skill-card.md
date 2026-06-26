## Description: <br>
Generate UML, C4, architecture, timing, ER, mindmap, WBS, and Gantt diagrams with PlantUML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxh](https://clawhub.ai/user/guoxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to draft PlantUML source for software, architecture, process, and planning diagrams, then render those diagrams locally as PNG or SVG outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering untrusted PlantUML source runs local Java and, for most diagram types, Graphviz against the diagram file. <br>
Mitigation: Review .puml files from untrusted sources before rendering and run them in a controlled workspace. <br>
Risk: URL-based PlantUML includes may fetch external resources during rendering. <br>
Mitigation: Avoid URL-based includes in sensitive or offline environments, or mirror required icon libraries locally. <br>


## Reference(s): <br>
- [PlantUML Syntax Quick Reference](references/syntax-guide.md) <br>
- [PlantUML Standard Library Quick Reference](references/stdlib-guide.md) <br>
- [PlantUML Themes Gallery](https://the-lum.github.io/puml-themes-gallery/) <br>
- [AWS Icons for PlantUML](https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with PlantUML code blocks, local render commands, and rendered diagram files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports PNG or SVG rendering through local Java, PlantUML, and Graphviz tooling.] <br>

## Skill Version(s): <br>
1.1.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
