## Description:

Git workspace automation (status/commit/push/log/diff).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect Git status, review diffs and logs, create commits, and push the current branch from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can commit all current workspace changes and push the current branch remotely without the safety checks advertised in its documentation.

Mitigation: Run status and diff before commit or push actions, use it only where committing all current changes is acceptable, and independently verify that secrets, private memory files, or unrelated changes are not included.

## Reference(s):

- [Conventional Commits](https://www.conventionalcommits.org/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Git commands against the configured workspace when used by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
