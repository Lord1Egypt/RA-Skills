## Description:

Execute git operations on behalf of Workers who don't have git credentials when a Worker sends a git-request message to clone, push, pull, commit, rebase, or perform other git operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montycn](https://clawhub.ai/user/montycn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to let a credentialed manager agent execute requested Git workflows for worker agents that cannot access repository credentials. It supports delegated clone, branch, commit, pull, push, merge, rebase, tag, stash, and related repository operations in shared workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or mistaken git-request messages can trigger authenticated Git operations under the manager's credentials.

Mitigation: Authenticate Worker requests and only enable the skill in tightly controlled environments.

Risk: Delegated commands can push commits, rewrite history, or affect private repositories.

Mitigation: Allowlist repositories and remotes, and require explicit approval for destructive Git actions such as force pushes, resets, and rebases.

Risk: Worker-provided workspace paths can lead to cross-task workspace changes.

Mitigation: Derive workspace paths server-side and reject paths outside the expected task workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/montycn/skills/git-delegation-management)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown messages with inline shell commands and command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success or failure summaries for delegated Git operations.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
