## Description:

Detect stale queued/in-progress GitHub Actions runs before they quietly block delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to audit exported GitHub Actions run data for workflows that have remained in queued, in-progress, pending, waiting, or requested states longer than configured thresholds. It helps summarize stuck-run risk by repository, workflow, or branch and can support CI gating on critical findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script processes local GitHub Actions JSON exports selected by RUN_GLOB.

Mitigation: Keep RUN_GLOB scoped to the intended export directory before running the audit.

Risk: Enabling FAIL_ON_CRITICAL can intentionally fail a CI pipeline.

Mitigation: Review the report output and threshold settings before using FAIL_ON_CRITICAL=1 in CI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daniellummis/skills/github-actions-stuck-run-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain-text report or JSON summary emitted by a local bash/python3 command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and one or more groups are critical.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
