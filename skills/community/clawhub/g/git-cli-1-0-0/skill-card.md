## Description:

Helper for using the Git CLI to inspect, stage, commit, branch, and synchronize code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand and perform everyday Git command-line workflows, including inspecting repository state, staging and committing changes, branching, stashing, syncing with remotes, and troubleshooting common Git issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git mutation commands can stage, commit, pull, push, stash, or switch branches, which may change local work or publish repository state.

Mitigation: Review generated Git commands before execution and prefer read-only inspection commands such as git status, git diff, and git log before making changes.

Risk: Destructive Git commands can discard local work or rewrite remote history if used incorrectly.

Mitigation: Use destructive commands only when explicitly requested and after confirming that the user understands the impact.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes read-only Git inspection before mutation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
