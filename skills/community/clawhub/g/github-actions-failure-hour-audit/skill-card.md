## Description:

Audit GitHub Actions failure timing by day/hour to surface recurring outage windows and staffing hotspots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and DevOps teams use this skill to audit exported GitHub Actions workflow runs, find recurring failure windows by day and hour, and prioritize flaky time ranges or on-call coverage gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad RUN_GLOB can cause the script to process unintended GitHub Actions JSON exports.

Mitigation: Point RUN_GLOB at a reviewed artifact directory or narrowed file pattern before running.

Risk: Reports may expose repository names, workflow names, branches, run IDs, and run URLs.

Mitigation: Review text or JSON output before sharing it outside the intended team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-failure-hour-audit)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Text report or JSON with summary, ranked windows, and critical_windows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit 1 when FAIL_ON_CRITICAL=1 and one or more critical windows are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
