## Description:

Helps developers start work by syncing the current Git repository, restoring local changes, sharing JavaScript, Vue, React, and AI tooling tips, and reporting the previous-close Nasdaq 100 change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luofeiioi](https://clawhub.ai/user/luofeiioi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill at the start of a work session to synchronize a repository with a rebase workflow, restore local changes, and receive brief development guidance and market context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically mutate the active Git repository from broad work-start trigger phrases.

Mitigation: Require the agent to show the repo root, branch, status, remote, and planned Git commands, then obtain explicit confirmation before execution.

Risk: The stash, rebase, and stash pop workflow can conflict with important uncommitted work or existing stashes.

Mitigation: Avoid using it in repositories with important uncommitted work or existing stashes unless the stash restoration logic targets only the stash it created.

## Reference(s):

- [Development Tips](references/dev_tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Git command output, development tips, and a web-sourced Nasdaq 100 previous-close change.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
