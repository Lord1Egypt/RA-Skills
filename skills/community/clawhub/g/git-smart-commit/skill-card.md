## Description:

Analyze staged git changes and generate high-quality Conventional Commits messages with optional scope and breaking change detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wusuiling-if](https://clawhub.ai/user/wusuiling-if)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect staged Git changes and draft clear Conventional Commits messages. With user approval, the agent can run the proposed git commit command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commit messages could inaccurately describe the staged changes.

Mitigation: Review the proposed message against the staged diff before approving a commit.

Risk: Running git commit mutates repository history.

Mitigation: Require explicit user approval before executing git commit, and use dry-run behavior when the user only wants a message.

## Reference(s):

- [Conventional Commits](https://www.conventionalcommits.org/)
- [ClawHub Skill Page](https://clawhub.ai/wusuiling-if/skills/git-smart-commit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with Conventional Commit messages and optional shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commit messages should be reviewed by the user before any commit is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
