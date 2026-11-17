## Description:

PRISM-Gen Demo lets agents retrieve, filter, rank, merge, score, visualize, and summarize bundled PRISM-Gen molecular screening CSV results locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[senazeng](https://clawhub.ai/user/senazeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry researchers use this skill to inspect precomputed PRISM-Gen molecular screening stages, compare molecule properties, and generate local tabular or plotted summaries without running new chemistry calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plot command can write an image to the path supplied by the user.

Mitigation: Choose an intended output location before running plot commands and avoid overwriting important files.

Risk: The skill analyzes bundled precomputed molecular screening data and does not perform new computational chemistry validation.

Mitigation: Treat results as exploratory analysis and review candidate molecules with appropriate domain validation before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/senazeng/skills/prism-gen-demo)
- [PRISM-Gen dataset DOI](https://doi.org/10.5281/zenodo.18764996)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with optional PNG plot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from bundled CSV data; plotting requires matplotlib and writes to the user-specified output path.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
