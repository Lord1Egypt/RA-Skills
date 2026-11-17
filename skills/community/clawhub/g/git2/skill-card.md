## Description:

Provides a Chinese-language Git command reference for common workflows including commits, branches, merges, rebases, resets, stashes, remotes, tags, diffs, logs, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mickey0811](https://clawhub.ai/user/mickey0811)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a quick Git command reference for everyday repository operations, including commits, branch management, merges, rebases, remote sync, history inspection, and undo workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some referenced Git commands can discard local work or rewrite history when used in the wrong repository, branch, or working tree state.

Mitigation: Verify the current repository, branch, and uncommitted changes before using reset --hard, clean -fd, branch -D, rebase, or push, and prefer preview or backup steps where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mickey0811/skills/git2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language command reference; no API calls, files, or configuration are generated.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
