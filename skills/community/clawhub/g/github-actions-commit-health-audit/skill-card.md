## Description:

Audit GitHub Actions reliability by commit SHA to surface risky commits causing repeated workflow failures across branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to audit exported GitHub Actions runs, group failures by repository and commit SHA, and prioritize rollback, revert, or targeted fixes for repeated CI failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local audit may read unintended or sensitive JSON files if RUN_GLOB or filter variables are too broad.

Mitigation: Run it only against intended GitHub Actions export directories and review RUN_GLOB plus branch, workflow, repository, and SHA filters before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-commit-health-audit)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text report or JSON summary with ranked commit-risk groups and critical commit details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and critical commit groups are found.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
