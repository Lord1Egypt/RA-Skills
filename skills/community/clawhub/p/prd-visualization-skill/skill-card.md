## Description:

Creates interactive D3.js hierarchy visualizations for PRDs, requirements, and other tree-structured data using list, force-directed, and radial cluster views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foyri](https://clawhub.ai/user/foyri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to turn PRDs, requirements, org charts, file structures, or other hierarchical inputs into an interactive browser-based diagram. It can create or update hierarchy JSON and provide local viewing steps for the visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running a local web server from a broad project directory can expose files in that directory through the browser.

Mitigation: Run the visualizer from a dedicated temporary directory containing only the HTML, D3 asset, and hierarchy JSON, and bind the server to 127.0.0.1.

Risk: PRD or hierarchy JSON content from other sources may be unsafe to render in the browser.

Mitigation: Treat incoming PRD and JSON content as untrusted and review or sanitize it before opening the visualization.

Risk: The skill writes visualization files into the user's project.

Mitigation: Review target paths before copying or generating files and avoid serving or writing into directories that contain secrets.

## Reference(s):

- [D3.js](https://d3js.org)
- [ClawHub skill page](https://clawhub.ai/foyri/skills/prd-visualization-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a requirements-hierarchy.json file and provides local browser visualization steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
