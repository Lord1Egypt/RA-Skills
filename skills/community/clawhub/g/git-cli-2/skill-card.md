## Description:

Git命令行 helps agents guide Git CLI workflows for inspecting, staging, committing, branching, merging, and synchronizing code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to get Git CLI guidance for status inspection, staging strategy, commit message drafting, branch workflows, conflict resolution, history review, and remote synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface high-impact Git commands such as force pushes, branch deletion, and reset --hard.

Mitigation: Treat those operations as manual-only and review the current branch, remote, status, and recovery options before running them.

Risk: Git guidance may be unsafe if it is applied without checking the repository state first.

Mitigation: Inspect status, diffs, staged changes, branch tracking, and remote targets before executing proposed commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-cli-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance may propose Git commands; review high-impact repository operations before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
