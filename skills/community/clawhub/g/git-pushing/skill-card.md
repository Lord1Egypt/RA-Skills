## Description:

Stage, commit, and push git changes with conventional commit messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyi-billy-ma](https://clawhub.ai/user/tianyi-billy-ma)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to automate a standard git workflow when they want an agent to stage repository changes, create a conventional commit, and push the current branch to the configured remote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stage every changed or untracked file in the current repository and push those changes to the configured remote branch.

Mitigation: Before use, manually review git status, the diff, the target branch, and the remote; avoid running it in repositories with secrets or unrelated local work.

Risk: The server security summary says the workflow lacks enough scoping or review controls before staging and pushing.

Mitigation: Use it only for intentional commit-and-push requests where broad staging is acceptable, and require human review of the pending changes before the script runs.

## Reference(s):

- [ClawHub Git Pushing skill page](https://clawhub.ai/tianyi-billy-ma/skills/git-pushing)
- [Claude Code](https://claude.com/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and brief status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute a bundled shell script that stages all repository changes, creates a commit, and pushes the current branch to origin.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
