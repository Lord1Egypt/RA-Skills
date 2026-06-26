## Description: <br>
Automatically identify diagram code blocks (Mermaid/Graphviz/PlantUML) in Markdown documents, render them as images, and replace them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fireium](https://clawhub.ai/user/fireium) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert Mermaid, Graphviz, and PlantUML code blocks in Markdown into embedded diagram images for documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback online rendering can send diagram source to third-party services. <br>
Mitigation: Install local Mermaid and PlantUML renderers before processing Markdown that may contain private architecture, hostnames, business logic, or secrets. <br>
Risk: The default workflow can modify the input Markdown file. <br>
Mitigation: Use version control, backups, or an explicit output path before running the skill. <br>
Risk: PlantUML local rendering depends on a jar path from PLANTUML_JAR. <br>
Mitigation: Set PLANTUML_JAR only to a trusted PlantUML jar and install dependencies in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fireium/markdown-diagram-renderer) <br>
- [Graphviz downloads](https://graphviz.org/download/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, JSON] <br>
**Output Format:** [Markdown with inline Base64 image data and JSON execution status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can overwrite the input Markdown by default; use an explicit output path when preserving the original file is required.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
