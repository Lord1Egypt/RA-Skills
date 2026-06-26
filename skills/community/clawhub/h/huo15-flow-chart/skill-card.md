## Description: <br>
Huo15 Flow Chart generates modern flowcharts, swimlanes, architecture diagrams, C4 diagrams, sequence diagrams, state diagrams, ER diagrams, and Gantt charts from YAML/JSON specifications or Mermaid/PlantUML/DOT source, with SVG, PNG, PDF, draw.io, and source-code outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, product teams, and technical writers use this skill to turn structured diagram specifications or existing diagram source into polished diagrams for documentation, presentations, architecture reviews, and planning materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary flags automatic execution of local renderers and unpinned Docker fallbacks. <br>
Mitigation: Install trusted Mermaid CLI, PlantUML, and Graphviz versions explicitly, pin them where possible, and avoid Docker or npx fallbacks in sensitive environments. <br>
Risk: Mermaid rendering uses Chromium with sandbox-disabling flags. <br>
Mitigation: Render diagrams in a contained workspace, container, or virtual machine when inputs are untrusted or when running on shared systems. <br>
Risk: YAML, Mermaid, PlantUML, and DOT diagrams from external sources can become untrusted renderer input. <br>
Mitigation: Review and scan external diagram sources before rendering, and keep generated files isolated from privileged project directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-flow-chart) <br>
- [Mermaid Live Editor](https://mermaid.live) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated diagram files or diagram source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce SVG, PNG, PDF, draw.io, Mermaid, PlantUML, and DOT outputs; PNG scaling defaults to 3x.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
