## Description:

Processes CSV files to generate statistical summaries for specified numeric columns and row count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidfsoft](https://clawhub.ai/user/aidfsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to read a local CSV in the workspace and produce summary statistics for selected numeric columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local CSV files, so users could expose files they did not intend the agent to inspect.

Mitigation: Provide only CSV files intended for analysis and keep the skill constrained to the local workspace.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON-like statistical summary with row count]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local workspace CSV files only; no network access is required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
