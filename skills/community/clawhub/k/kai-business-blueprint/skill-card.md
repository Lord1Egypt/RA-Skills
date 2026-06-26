## Description: <br>
Turns presales requirements, meeting notes, and solution materials into editable business capability blueprints, swimlane flows, application architecture diagrams, and exports such as JSON, HTML, SVG, draw.io, Excalidraw, or Mermaid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solution architects, and presales teams use this skill to convert raw requirements or meeting notes into structured blueprint JSON, visual viewers, diagrams, and downstream projection files for reports or slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business materials provided to the skill may be transformed into local blueprint files, diagrams, patch logs, and audit metadata. <br>
Mitigation: Use a controlled workspace for sensitive engagements and review generated files before sharing them outside the workspace. <br>
Risk: Command-line arguments may be retained in export audit files. <br>
Mitigation: Do not pass tokens, passwords, customer secrets, or sensitive source text as command-line arguments. <br>
Risk: Generated HTML, SVG, JSON, and diagram exports may include business details from the source material. <br>
Mitigation: Review exported artifacts before publishing, emailing, or committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaisersong/kai-business-blueprint) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [Blueprint Schema](references/blueprint-schema.md) <br>
- [Entities Schema](references/entities-schema.md) <br>
- [Systems Schema](references/systems-schema.md) <br>
- [Export Quality Evals](evals/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [JSON blueprint files, Markdown guidance, shell commands, static HTML viewers, SVG, draw.io, Excalidraw, Mermaid, and projection JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts are intended to be written locally, commonly under a workspace project directory.] <br>

## Skill Version(s): <br>
0.15.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
