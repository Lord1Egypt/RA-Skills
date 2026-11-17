## Description:

Git Pro helps agents provide advanced Git workflow guidance for commits, rebases, bisects, worktrees, reflog recovery, cherry-picks, submodules, subtrees, and pull-request flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan and explain advanced Git operations, including history cleanup, debugging regressions, parallel branch work, recovery, and pull-request preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced Git operations such as rebase, amend, and force-with-lease can rewrite repository history or affect shared work if used incorrectly.

Mitigation: Review proposed commands before execution, use force-with-lease only when needed, rebase only personal branches, and avoid amending commits that are already public.

Risk: Generic Git workflow guidance may not account for local repository policies, branch protections, or team review requirements.

Mitigation: Check project-specific contribution rules and branch protection settings before applying pull-request or history-editing guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cooperiano/skills/git-pro)
- [Publisher profile](https://clawhub.ai/user/cooperiano)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline Git commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included; command guidance should be reviewed before running history-rewriting Git operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
