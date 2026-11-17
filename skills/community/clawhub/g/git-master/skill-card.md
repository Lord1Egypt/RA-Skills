## Description:

Git Master guides agents through git commits, rebases, squashes, and history searches with atomic commit planning, repository style detection, and branch-safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan and execute git workflows, including atomic commits, branch assessment, rebases, squashes, and history searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide active git history management, including rebases, resets, stashes, bisects, and force-with-lease pushes.

Mitigation: Require explicit review and confirmation of each state-changing git command before execution.

Risk: History rewrites and remote pushes can disrupt protected or shared branches.

Mitigation: Review branch protection, upstream state, and the exact push or rewrite command before using the skill on shared branches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wei840222/skills/git-master)
- [ClawHub publisher profile](https://clawhub.ai/user/wei840222)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured git workflow plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute state-changing git commands when the host agent is allowed to run them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
