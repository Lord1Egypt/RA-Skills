## Description:

Detect sudden GitHub Actions failure-rate spikes by workflow group using recent-vs-baseline run windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and DevOps engineers use this skill to audit exported GitHub Actions run JSON and identify workflow groups with recent failure-rate spikes before they become long-running incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad RUN_GLOB can include unrelated JSON files and distort the report.

Mitigation: Run the audit against a narrow artifacts/github-actions path or an explicit fixture directory.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, text, JSON, shell commands, configuration]

**Output Format:** [Text report or JSON report from a local shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports regex filters, recent and baseline run-window thresholds, ranked severity output, and an optional fail gate for critical groups.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
