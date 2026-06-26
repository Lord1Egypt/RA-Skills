## Description: <br>
Creates interactive D3.js hierarchy visualizations for PRDs, requirements, features, specifications, org charts, file structures, and other tree-shaped data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foyri](https://clawhub.ai/user/foyri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and agents use this skill to convert PRDs or hierarchical project data into a requirements-hierarchy.json file and view it in an interactive local D3.js visualizer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates visualization files in a project directory. <br>
Mitigation: Confirm the target project folder and check whether requirements-hierarchy.json already exists before copying or overwriting files. <br>
Risk: The skill starts a local HTTP server from the selected project directory. <br>
Mitigation: Serve only a directory that does not contain secrets and stop the local server after viewing the visualization. <br>


## Reference(s): <br>
- [D3.js](https://d3js.org) <br>
- [PRD Visualization Skill on ClawHub](https://clawhub.ai/foyri/prd-visualization-skill) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update requirements-hierarchy.json and serve hierarchy-visualizer.html locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
