## Description:

Assist with Git branch management, merging, rebasing, cherry-picking, and cleaning merged branches for smoother workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honestqiao](https://clawhub.ai/user/honestqiao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to get Git workflow assistance for branch creation, merges, rebases, cherry-picks, conflict-oriented workflows, and cleanup of merged branches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell command execution could allow untrusted branch, commit, or ref names to change command behavior.

Mitigation: Use argument-array process execution and validate Git refs before allowing commands to run.

Risk: Git operations such as merge, rebase, cherry-pick, and branch cleanup can change repository state.

Mitigation: Require manual confirmation before mutating Git commands and use the skill only in repositories that can be recovered.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honestqiao/skills/git-flow-helper)
- [Publisher profile](https://clawhub.ai/user/honestqiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline Git shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository-changing Git commands that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
