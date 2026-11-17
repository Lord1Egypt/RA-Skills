## Description:

Helps agents audit a repository and generate or update a tailored git worktree bootstrap script with matching hook configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imsai-sh](https://clawhub.ai/user/imsai-sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make fresh git worktrees runnable by having an agent classify shared, copied, and generated resources, then create the setup script and hook configuration for the current repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated hook configuration can make setup scripts run automatically in agent sessions or worktree flows.

Mitigation: Review the generated hook config before installation and keep the manual setup command available as a fallback.

Risk: Generated shell scripts can copy sensitive environment files or replace existing files when configured to do so.

Mitigation: Review the generated script, avoid copying real secrets unless duplication is intended, and run it in a noncritical worktree before broader use.

Risk: Sharing single-writer state such as local database directories across concurrent worktrees can corrupt state.

Mitigation: Confirm the concurrency model and prefer isolated copies for stateful services that may run in parallel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imsai-sh/skills/git-worktree-setup)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Worktree setup recipes](references/recipes.md)
- [Hook configuration candidates](assets/hook-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated shell script and JSON hook configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update repository-local setup scripts and agent hook configuration after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
