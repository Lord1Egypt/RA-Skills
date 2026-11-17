## Description:

Professional beautification tool for gene expression heatmaps, automatically adds clustering trees, color annotation tracks, and intelligently optimizes label layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to generate publication-ready gene expression heatmaps from CSV expression matrices with clustering, annotation tracks, and readable labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security guidance reports reliability and documentation problems, including documented demo and metadata options that may fail until the script is updated.

Mitigation: Verify supported command-line options with the installed script before relying on demo or metadata-output workflows, and describe any unavailable option as unresolved rather than completed.

Risk: The skill runs local Python visualization code with third-party plotting and data dependencies.

Mitigation: Install and run it in an isolated Python environment with reviewed or pinned dependency versions.

Risk: The security guidance warns against exposing raw tracebacks to untrusted users.

Mitigation: Report concise failure points and recovery steps, and avoid returning raw stack traces unless the recipient is trusted and needs debugging detail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/heatmap-beautifier)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python or shell command examples; generated heatmap files may be PDF, PNG, SVG, EPS, or TIFF depending on the script invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local CSV and JSON annotation inputs; documented demo and metadata-output options require verification against the installed script before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
