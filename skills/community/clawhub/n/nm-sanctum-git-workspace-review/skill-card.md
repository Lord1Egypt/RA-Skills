## Description:

Verifies workspace state and staged changes as a read-only preflight. Use before commits or PRs to confirm staged set is clean and correct

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before commits, pull requests, or release-note work to inspect repository status, check code quality, review staged or unstaged diffs, and prepare a summary for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instructions to stage or unstage files and abort merges conflict with the read-only preflight description and can change repository state.

Mitigation: Review the workflow before use and require explicit approval before changing staged files or merge state.

Risk: The security analysis is incomplete because a referenced local path was missing.

Mitigation: Inspect the referenced files and confirm the instructions match the intended workflow before installation or execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-git-workspace-review)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown review notes with Git shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes repository status, staged changes, quality-check results, and diff themes for downstream workflows.]

## Skill Version(s):

1.10.3 (source: skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
