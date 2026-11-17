## Description:

Provides advanced Git operations support for bisecting regressions, cleaning branches, managing stashes, analyzing history, and handling destructive or history-rewriting commands with explicit safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill inside Git repositories to plan and review bisect, branch cleanup, stash recovery, and commit history workflows before executing commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive Git operations such as hard resets, cleanups, branch deletion, rebases, or forced pushes can lose work or rewrite shared history.

Mitigation: Review the current branch and HEAD, verify target commits, and create a backup branch, tag, stash, or patch before approving execution.

Risk: Incorrect branch, stash, or commit selection can cause the user to act on the wrong repository state.

Mitigation: Require explicit confirmation of the exact branch, commit, stash entry, and remote tracking state before running the proposed command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppopen/skills/openclaw-skill-git-manager)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline Git shell commands and safety checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before destructive Git operations.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
