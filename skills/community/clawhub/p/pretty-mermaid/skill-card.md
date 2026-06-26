## Description: <br>
Generate styled Mermaid.js diagrams such as flowcharts, sequence diagrams, Gantt charts, and class diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caowen2211891](https://clawhub.ai/user/caowen2211891) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and documentation maintainers use this skill to create Mermaid diagrams and export them as PNG, SVG, PDF, or interactive HTML with custom themes and styling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends installing @mermaid-js/mermaid-cli as a global npm dependency, which can affect the user's system Node environment. <br>
Mitigation: Install only if a global npm dependency is acceptable, or adapt the workflow to use a local or isolated package installation. <br>
Risk: Interactive HTML output loads Mermaid JavaScript from a CDN. <br>
Mitigation: For sensitive or offline work, prefer PNG or SVG output, or vendor Mermaid locally before opening generated HTML. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/caowen2211891/pretty-mermaid) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Mermaid code and shell commands; generated diagram files may be PNG, SVG, PDF, or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Mermaid themes, custom colors, dimensions, and optional interactive HTML output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
