## Description:

Use outlier detection handler for data analysis workflows that need structured execution, explicit assumptions, and clear output boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and reviewers use this skill to identify statistical outliers in dataset files and produce handling recommendations with explicit assumptions and reviewable outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependencies are not pinned, which can affect repeatability in regulated or production analysis.

Mitigation: Install the skill in an isolated Python environment and pin or lock numpy and scipy before repeatable use.

Risk: The packaged script reads the file path supplied with --data.

Mitigation: Provide only intended dataset files as input and run the script in a workspace-limited environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, inputs used, recommendations, risks, limits, unresolved items, and validation checks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
