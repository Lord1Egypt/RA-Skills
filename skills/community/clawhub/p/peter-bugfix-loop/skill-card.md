## Description:

Peter Bugfix Loop is a Chinese-language workflow for driving a bug from report to merge-ready fix through reproduction, root-cause analysis, minimal repair, tests, and PR closure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasilva](https://clawhub.ai/user/chinasilva)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to structure bug fixes from an initial problem report through reproducible evidence, root-cause analysis, a minimal code change, tests, and PR closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can ask an agent to make commits, open PRs, or revert changes in shared repositories.

Mitigation: Confirm commit, PR, and revert actions before execution, and review the proposed diff and test results before merging.

Risk: A bug fix made before reproducing the defect could mask the real root cause or introduce unrelated changes.

Mitigation: Require a minimal failing test or reproducible CLI, HTTP, or UI command before making code changes, then keep the repair scoped to the identified cause.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasilva/skills/peter-bugfix-loop)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Code]

**Output Format:** [Markdown bug-fix report with code, command, and status details as applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed report sections for bug card, reproduction, root cause, fix, tests, gates, and conclusion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
