## Description: <br>
Helps agents create Mermaid diagrams across common chart types and prepare PNG or interactive HTML outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrot90-code](https://clawhub.ai/user/harrot90-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and agents use this skill to draft Mermaid syntax for flowcharts, sequence diagrams, class diagrams, state diagrams, ER diagrams, Gantt charts, pie charts, mind maps, timelines, Git graphs, Sankey diagrams, XY charts, block diagrams, quadrant charts, and user journeys, then render or package those diagrams as PNG, SVG, PDF, or HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendered image or PDF output depends on mermaid-cli/mmdc being available in the agent environment. <br>
Mitigation: Confirm mermaid-cli is installed before requesting rendered files, or use the skill's HTML output path when CLI rendering is unavailable. <br>
Risk: The HTML template loads Mermaid from a third-party CDN, which may be unsuitable for restricted or offline environments. <br>
Mitigation: Replace the jsdelivr Mermaid import with an approved local or internal Mermaid bundle when third-party CDN loading is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrot90-code/mermaid-charts) <br>
- [Mermaid browser import used by the HTML template](https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Mermaid code blocks, mmdc shell commands, HTML templates, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide generation of PNG, SVG, PDF, and interactive HTML diagram artifacts when Mermaid CLI or a Mermaid browser runtime is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
