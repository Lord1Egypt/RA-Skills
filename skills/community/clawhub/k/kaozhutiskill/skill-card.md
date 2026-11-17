## Description:

Analyzes production defects with RCA, responsibility assessment, similar-defect grouping, historical deduplication, summaries, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wal1234](https://clawhub.ai/user/wal1234)

### License/Terms of Use:


## Use Case:

Developers, engineering managers, QA teams, and incident responders use this skill to turn production errors, defect lists, CSV text, or JSON records into structured defect analysis reports, RCA summaries, ownership analysis, duplicate checks, and trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production defect inputs may contain sensitive logs, credentials, IP addresses, or user data.

Mitigation: Review production logs before sharing them and redact sensitive values; the skill also instructs the agent to mask passwords, keys, tokens, IP addresses, and user data in its output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wal1234/skills/kaozhutiskill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, analysis]

**Output Format:** [Structured Markdown reports with headings, tables, lists, and code blocks for logs or snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to redact passwords, keys, tokens, IP addresses, and user data in outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
