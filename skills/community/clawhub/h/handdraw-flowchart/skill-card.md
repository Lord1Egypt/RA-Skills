## Description: <br>
Create hand-drawn workflow diagrams from natural-language process descriptions by generating strictly validated Mermaid flowchart, sequenceDiagram, or classDiagram code, converting Mermaid to Excalidraw scene files, and exporting PNGs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengiai](https://clawhub.ai/user/zengiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to turn process descriptions into validated Mermaid diagrams and render them as sketch-style Excalidraw and PNG artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The renderer depends on npm packages and a local headless browser. <br>
Mitigation: Install and run it only in an environment where those local dependencies are acceptable. <br>
Risk: Output files using the selected diagram name can be created or overwritten. <br>
Mitigation: Use a dedicated output folder for generated diagrams. <br>


## Reference(s): <br>
- [Mermaid Generation Rules](references/mermaid-generation-rules.md) <br>
- [Project homepage](https://github.com/zengiai/handdraw-flowchart) <br>
- [ClawHub skill page](https://clawhub.ai/zengiai/handdraw-flowchart) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, files, guidance] <br>
**Output Format:** [Mermaid source, Excalidraw scene JSON, PNG image files, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Renderer writes normalized .mmd, .excalidraw, and .png files using the selected diagram name.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
