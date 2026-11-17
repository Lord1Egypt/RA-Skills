## Description:

Build a change in its own worktree, prove it with mutation testing, self-audit before pushing, open the PR with a body that states what it does not prove, then stop and hand off to the review loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunjeetsingh](https://clawhub.ai/user/arunjeetsingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to implement a requested change in an isolated worktree, validate it, push a branch, and open a review-ready pull request. It is intended for actual PR creation, not for dry-run planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push a branch, open a pull request, and arm a watcher that may later invoke more repository-changing automation.

Mitigation: Install and invoke it only when actual PR creation is intended, and prefer explicit opt-in for the watcher in repositories with write-capable credentials.

Risk: A default background watcher may be difficult to account for if its stop mechanism or session survival behavior is unclear.

Mitigation: Confirm how the watcher is armed, how to stop it, and whether it survives the current session before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arunjeetsingh/skills/open-pr)
- [Publisher profile](https://clawhub.ai/user/arunjeetsingh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May push a branch, open a pull request, and arm a review watcher when used in a repository with the required git and gh tools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
