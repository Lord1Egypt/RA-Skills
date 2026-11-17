## Description:

OpenSpec Workflow guides developers and engineering agents through spec-driven code changes using OpenSpec artifacts, Claude Code review and implementation, GitHub PRs, and optional auto-archive CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbyradford](https://clawhub.ai/user/bobbyradford)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to plan, review, implement, and ship OpenSpec-backed repository changes. It is suited for code changes that affect product behavior, spec artifacts, task breakdowns, pull requests, and optional OpenSpec archive automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can grant an agent broad repository authority, including reading and modifying the full repo, committing, pushing, opening PRs, and running archive automation.

Mitigation: Require a clean worktree, scope file changes with path allowlists, and require human review before commits, pushes, or PR creation.

Risk: The artifact recommends running Claude Code with --dangerously-skip-permissions.

Mitigation: Remove --dangerously-skip-permissions and use normal permission prompts or a restricted execution environment.

Risk: The archive workflow can delete branches after merge.

Mitigation: Make branch deletion opt-in and restrict cleanup to expected same-repository branches.

Risk: Dependencies and GitHub Actions are shown without pinning.

Mitigation: Pin CLI and GitHub Action versions before deploying the workflow in production repositories.

## Reference(s):

- [OpenSpec Auto-Archive Reference](references/archive-action.md)
- [Review Loop Protocol](references/review-loop.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, YAML configuration, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repo workflow instructions, review prompts, PR commands, and CI configuration examples for an agent to apply in an OpenSpec-enabled repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
