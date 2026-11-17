## Description:

Interact with GitHub using Personal Access Tokens for user-controlled repository access, including clone, push, branch, pull request, issue, and repository information workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to work with GitHub repositories through a personal access token that they create and scope themselves. It supports common repository tasks such as listing repositories, cloning, creating branches, committing and pushing changes, opening pull requests, creating issues, and viewing repository information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal access tokens can be exposed through workspace files, command lines, logs, or authenticated Git remote URLs.

Mitigation: Use narrowly scoped fine-grained PATs, prefer environment-based token handling, avoid storing tokens in workspace files, and do not pass tokens directly on command lines.

Risk: Push workflows can publish unintended files because the command stages all changes.

Mitigation: Inspect git status and diffs before pushing, and verify the Git remote hostname and repository target before any push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dannyshmueli/skills/github-token)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the GitHub API and local git commands when the user supplies a token and repository context.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
