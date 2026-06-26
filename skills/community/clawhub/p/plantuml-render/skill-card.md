## Description: <br>
Render PlantUML diagrams using the PlantUML JAR. Use this skill to generate PNG/SVG/PDF images from PlantUML source code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafeimao-gjf](https://clawhub.ai/user/jiafeimao-gjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create PlantUML source files and render them into diagram images for documentation, design notes, or Markdown content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and Java commands to invoke PlantUML. <br>
Mitigation: Use a trusted Java runtime and PlantUML JAR, and run rendering in a controlled working directory. <br>
Risk: Untrusted PlantUML content may carry processing or rendering risk. <br>
Mitigation: Avoid rendering untrusted diagrams unless appropriate sandboxing is in place. <br>
Risk: The release is currently marked as low trust and quarantined by ClawHub quality metadata. <br>
Mitigation: Review the skill contents and generated diagrams before deployment or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiafeimao-gjf/plantuml-render) <br>
- [Publisher profile](https://clawhub.ai/user/jiafeimao-gjf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PlantUML source, shell commands, and generated image file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PlantUML rendering instructions and local diagram files such as PNG, SVG, or PDF when the PlantUML JAR and Java runtime are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
