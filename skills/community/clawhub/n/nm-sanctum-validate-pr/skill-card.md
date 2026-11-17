## Description:

Generates and self-executes a diff-derived test plan for a PR

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after PR changes to build and execute checks targeted to the changed files and areas. It summarizes validation evidence and checks whether revert tests catch regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marked suspicious for unsafe filename handling and a revert-test that may proceed despite a dirty-worktree warning.

Mitigation: Review and correct filename handling, and ensure the revert-test stops when the working tree is dirty before installation.

Risk: The security assessment has incomplete coverage because some referenced paths could not be resolved.

Mitigation: Review the unavailable paths and obtain a complete security assessment before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-sanctum-validate-pr)
- [Repository homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Analysis]

**Output Format:** [Markdown validation summary with area-specific checks, command evidence, and revert-test results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PR-specific validation plan and evidence; commands may be executed by the agent.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
