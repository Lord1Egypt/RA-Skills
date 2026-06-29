## Description: <br>
Generates a Mermaid class diagram showing types, inheritance, and composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to inspect a selected codebase scope, identify classes and relationships, and present a Mermaid class diagram for API documentation or architecture understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The activation trigger is broad enough that an agent may inspect more of a codebase than needed. <br>
Mitigation: Invoke it explicitly with a narrow scope, such as a specific package or folder, before generating the diagram. <br>
Risk: Generated class diagrams can omit or misstate relationships when summarizing complex code. <br>
Mitigation: Review the Mermaid output and analysis notes against the source before using them as architecture documentation. <br>


## Reference(s): <br>
- [Nm Cartograph Class Diagram on ClawHub](https://clawhub.ai/athola/skills/nm-cartograph-class-diagram) <br>
- [Cartograph homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, guidance] <br>
**Output Format:** [Markdown with Mermaid classDiagram code and concise analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a rendered diagram, class and relationship counts, inheritance notes, and composition notes.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
