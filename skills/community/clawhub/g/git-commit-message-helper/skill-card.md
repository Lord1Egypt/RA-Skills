## Description:

Suggests conventional commit messages from a staged diff summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft a concise commit message after staging changes or sharing a diff summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad commit-message request may produce a suggestion without the intended staged changes.

Mitigation: Confirm the suggestion uses a pasted diff or stat, or an approved read-only staged Git summary, before relying on it.

## Reference(s):

- [Git documentation](https://git-scm.com/doc)
- [ClawHub skill page](https://clawhub.ai/hmahmadcs/skills/git-commit-message-helper)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text conventional commit message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One primary suggestion and two alternatives; subject at most 72 characters, with an optional body.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
