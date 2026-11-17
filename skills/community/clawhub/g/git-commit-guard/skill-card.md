## Description:

Enforce a git-first workflow for repository coding tasks by requiring status checks, dirty-worktree review, validation, and detailed Chinese commits before and after coding work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ontheway23333](https://clawhub.ai/user/ontheway23333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill in local git repositories to stabilize dirty worktrees, run relevant validation, and create detailed Chinese git commits around implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create local git commits during ordinary repository work without explicit user approval.

Mitigation: Install only where automatic commits are acceptable, or require explicit approval before committing and narrow the skill's trigger scope.

Risk: Broad repository-task invocation can affect unrelated dirty work if the worktree is not reviewed carefully.

Mitigation: Review git status and diffs before editing or committing, keep unrelated changes separate, and run targeted validation before staging changes.

## Reference(s):

- [Chinese commit template](references/commit-template.md)
- [ClawHub skill page](https://clawhub.ai/ontheway23333/skills/git-commit-guard)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, code]

**Output Format:** [Markdown/text responses with inline shell commands and Chinese git commit messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local git commits after validation; final responses report validation and commit hashes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
