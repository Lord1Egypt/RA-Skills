## Description:

Detect branch-level GitHub Actions reliability drift by comparing failure and runtime deltas against a mainline baseline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI/release engineers use this skill to audit GitHub Actions run exports for branch-specific failure-rate and runtime drift before changes reach mainline release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad RUN_GLOB patterns can read unrelated JSON files and include parse errors or selected fields in report output.

Mitigation: Set RUN_GLOB to a narrow directory containing only the intended GitHub Actions run exports.

Risk: Generated reports can include repository names, workflow names, branch names, and sample run URLs from the input exports.

Mitigation: Use sanitized exports or limit report sharing when CI metadata is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-branch-drift-audit)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text or JSON drift report with shell command examples and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical drift rows are present.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
