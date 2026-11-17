## Description:

Detect GitHub Actions workflow groups that stopped running on their normal cadence using median run intervals and current inactivity gap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to audit GitHub Actions run exports for workflow groups that have gone unexpectedly quiet because of stale triggers, disabled schedules, or branch drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can include repository, workflow, branch, run ID, and run URL data in generated reports.

Mitigation: Keep RUN_GLOB scoped to intended GitHub Actions export files and review where text or JSON reports are stored or shared.

Risk: Broad run-export globs may parse unintended local JSON files.

Mitigation: Use a narrow RUN_GLOB and optional regex filters such as REPO_MATCH, WORKFLOW_MATCH, RUN_ID_MATCH, or RUN_URL_MATCH for targeted triage.

## Reference(s):

- [GitHub Actions Run Gap Audit on ClawHub](https://clawhub.ai/daniellummis/skills/github-actions-run-gap-audit)

## Skill Output:

**Output Type(s):** [analysis, text, json, shell commands, guidance]

**Output Format:** [Text or JSON reports with optional shell command usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical stale workflow groups are found.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
