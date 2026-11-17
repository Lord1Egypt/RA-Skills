## Description:

Github Contribution helps agents discover maintainer-approved GitHub issues, prepare clean fork branches, and produce pull request contribution guidance with proof expectations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to identify suitable GitHub issues, prepare a synchronized fork and feature branch, and draft contribution-ready pull requests with concrete validation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can reset and clean a local repository, which may discard uncommitted work or untracked files.

Mitigation: Run it only in disposable or freshly cloned fork directories, check git status first, and back up or commit any local work before execution.

Risk: The workflow may encourage broader GitHub token permissions than are needed for normal contribution tasks.

Mitigation: Prefer existing GitHub CLI or SSH authentication, or use fine-grained credentials limited to the relevant fork or repository.

Risk: The automation depends on repository branch conventions and upstream remote state.

Mitigation: Manually verify the target repository, fork, upstream remote, and branch names before allowing push or pull request actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linux2010/skills/github-contribution)
- [Publisher Profile](https://clawhub.ai/user/linux2010)
- [Skill Instructions](artifact/SKILL.md)
- [Contribution Workflow](artifact/github-contribution-workflow.md)
- [Live Proof Cases](artifact/live-proof-cases.md)
- [Automation Script](artifact/scripts/github-contribution.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository-specific command sequences, PR text, checklists, and validation evidence templates.]

## Skill Version(s):

1.7.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
