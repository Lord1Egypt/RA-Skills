## Description: <br>
Generate Excalidraw hand-drawn diagrams from natural language, including diagrams, flowcharts, mind maps, architecture diagrams, ER diagrams, and sequence diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcdowell8023](https://clawhub.ai/user/mcdowell8023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical teams use this skill to turn natural-language system, process, and data-model descriptions into editable Excalidraw diagrams and optional PNG exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PNG export launches headless Chromium and loads remote JavaScript for rendering. <br>
Mitigation: For confidential architecture, business, or credential-adjacent diagrams, use only the .excalidraw output or an offline/self-hosted renderer. <br>
Risk: The skill creates local diagram and optional PNG files. <br>
Mitigation: Review output paths and generated files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcdowell8023/oc-excalidraw-diagram) <br>
- [Element Spec](references/element-spec.md) <br>
- [Diagram Templates](references/diagram-templates.md) <br>
- [Examples](references/examples.md) <br>
- [Headless Export](references/headless-export.md) <br>
- [Excalidraw](https://excalidraw.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Markdown, Guidance] <br>
**Output Format:** [.excalidraw JSON files, optional PNG files, and concise Markdown status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local diagram files and may run a Playwright-based PNG export path that launches headless Chromium.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
