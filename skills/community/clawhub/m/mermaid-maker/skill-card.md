## Description: <br>
Generate, validate, render, and export Mermaid diagrams (.mmd) for flowcharts, sequence diagrams, class diagrams, ER diagrams, state machines, architecture visuals, timelines, git graphs, mind maps, C4 diagrams, pie charts, and user journeys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwugit](https://clawhub.ai/user/junwugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to turn system flows, data models, architecture descriptions, and process narratives into Mermaid source files and rendered diagram outputs for documentation and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram contents may include private architectures, schemas, or auth flows and can be sent to the external Kroki service when that backend is used. <br>
Mitigation: Prefer local rendering for sensitive diagrams and use Kroki only when external processing is approved. <br>
Risk: The bundled rendering scripts may invoke npm automatically and mutate the skill folder during dependency installation. <br>
Mitigation: Review the scripts before running them and execute them in an environment where npm installs and local file changes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/junwugit/mermaid-maker) <br>
- [Rendering and export backends](reference/RENDERING.md) <br>
- [Flowchart syntax](reference/FLOWCHART.md) <br>
- [Sequence diagram syntax](reference/SEQUENCE.md) <br>
- [Class and ER diagram syntax](reference/CLASS-ER.md) <br>
- [Theme catalog](reference/THEMES.md) <br>
- [Kroki Mermaid API](https://kroki.io/mermaid/svg) <br>
- [Mermaid Live Editor](https://mermaid.live) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Mermaid code blocks, file paths, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce Mermaid source files and guide SVG, ASCII, PNG, or PDF rendering depending on the selected backend.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
