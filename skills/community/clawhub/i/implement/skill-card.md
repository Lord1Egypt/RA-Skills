## Description:

Build a feature in an isolated worktrunk worktree, commit it, push a branch, and open a draft pull request for code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mertbuilds](https://clawhub.ai/user/mertbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to carry a scoped implementation request through an isolated worktree, focused code changes, validation, commit, push, and draft pull request creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can push code and open a draft pull request.

Mitigation: Review the repository, branch, diff, and pull request contents before allowing or relying on remote actions.

Risk: The workflow may copy ignored environment files into a new worktree.

Mitigation: Use only in projects where propagating local env files into feature worktrees is acceptable, and inspect copied files for secrets exposure risk.

Risk: The cleanup guidance includes broadly matched dev-server process termination.

Mitigation: Confirm the process list or use narrower process identifiers before terminating local development servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mertbuilds/skills/implement)
- [Server-resolved source import](https://github.com/mertbuilds/skills/tree/main/implement)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify repository files, commits, branches, draft pull requests, and local dev-server state when executed by an agent.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
