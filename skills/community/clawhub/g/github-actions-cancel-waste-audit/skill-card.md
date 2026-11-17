## Description:

Audit cancelled and timed-out GitHub Actions runs from JSON exports to surface wasted CI minutes and noisy workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to analyze GitHub Actions run exports, quantify wasted minutes from cancelled or timed-out runs, and identify repositories or workflows that need triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub Actions export files can contain private repository metadata, branch names, actor names, run URLs, and timing details.

Mitigation: Keep RUN_GLOB limited to intended export directories and avoid running the report over sensitive JSON exports unless that metadata may be printed.

Risk: Waste estimates depend on the timestamps and conclusions present in exported GitHub Actions run JSON.

Mitigation: Review the source export scope and configured thresholds before using the report to make CI budget or workflow-prioritization decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-cancel-waste-audit)
- [ClawHub publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with bash examples; script output is text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit 1 when FAIL_ON_CRITICAL=1 and at least one run reaches the critical waste threshold.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
