## Description:

Audit GitHub Actions rerun dependency and success-after-rerun effectiveness to highlight workflows wasting CI time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI engineers use this skill to audit exported GitHub Actions run data for workflows that frequently require reruns, recover poorly after reruns, or spend extra CI minutes on ineffective rerun attempts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads every local JSON file matched by RUN_GLOB and can include selected GitHub Actions run metadata in its report.

Mitigation: Keep RUN_GLOB scoped to the intended CI export directory and review generated reports before sharing them.

Risk: When FAIL_ON_CRITICAL=1, critical rerun metrics can cause the command to exit with status 1.

Mitigation: Tune the warning and critical thresholds for the repository before enabling the fail gate in CI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-rerun-effectiveness-audit)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text report or JSON report with summary, ranked workflow groups, and critical groups.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May exit with status 1 when FAIL_ON_CRITICAL=1 and critical workflow groups are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
