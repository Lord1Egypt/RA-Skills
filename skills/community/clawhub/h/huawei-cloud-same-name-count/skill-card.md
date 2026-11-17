## Description:

Query same-name counts in a bundled sample dataset, with optional gender and province filters and Markdown, plain-text, or JSON output.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can look up how many records in the bundled sample dataset share a name, optionally filtering by gender or province. Results include matching totals and breakdowns for quick inspection or downstream use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample counts could be mistaken for official population statistics.

Mitigation: Identify results as sample/demo figures and do not present them as authoritative statistics.

Risk: Using --output can overwrite an existing file.

Mitigation: Check the destination path before running a query that writes to a file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-same-name-count)
- [Usage Guide](artifact/references/usage-guide.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown, plain text, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Counts come from a bundled sample dataset and are not official population statistics.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
