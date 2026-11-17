## Description:

Helps users prepare, review, and create Conventional Commit plans and Git commits from current repository changes after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlykan](https://clawhub.ai/user/wlykan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect staged, unstaged, and untracked Git changes, group them by business intent, produce Conventional Commit messages, and commit only after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository diffs and untracked text files to prepare commit plans, which can expose sensitive project content to the assistant.

Mitigation: Install only in repositories where that access is acceptable, keep sensitive files excluded, and review the generated plan before confirming any commit.

Risk: Commit-message language may default to Chinese when repository conventions are unclear, which may not match a team's preferred language.

Mitigation: State the desired commit-message language before confirming the plan if Chinese is not preferred.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with Git commit messages and command execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commit plans, file groupings, risk notes, and confirmation-gated execution reports.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
