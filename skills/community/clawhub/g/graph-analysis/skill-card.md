## Description:

Analyze graphs and networks using Python NetworkX -- centrality, shortest paths, community detection, and visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owenciantar](https://clawhub.ai/user/owenciantar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to build graphs from structured relationship data, compute centrality and path metrics, detect communities, and generate network visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance uses unpinned Python packages and --break-system-packages, which can modify a system Python environment or make installs less reproducible.

Mitigation: Install dependencies in an isolated virtual environment or container, avoid --break-system-packages, and pin dependency versions when reproducibility matters.

Risk: Generated visualization code may write to default filenames such as graph.png or communities.png and overwrite existing files.

Mitigation: Choose explicit output paths or check for existing files before saving generated visualizations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/owenciantar/skills/graph-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG graph visualization files when the generated code is executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
