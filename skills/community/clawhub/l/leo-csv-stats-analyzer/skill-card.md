## Description:

Analyzes any CSV file and returns row count, column names, and basic statistics for numeric columns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leotrieu](https://clawhub.ai/user/leotrieu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to inspect a readable CSV file and receive a concise summary of its shape and numeric columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a user-provided CSV file and depends on pandas at runtime.

Mitigation: Run it with least privilege and pin pandas when reproducible or audited dependency behavior matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leotrieu/skills/leo-csv-stats-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown-formatted text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports row count, column names, and min, max, and average for numeric columns; does not modify the input CSV.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
