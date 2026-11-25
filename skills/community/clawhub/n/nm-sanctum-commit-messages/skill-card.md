## Description:

Generates conventional commit messages from staged changes

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft conventional commit messages from staged changes, using repository status, staged diffs, recent history, and semantic diff output when available. It stops when there are no staged changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A draft can misstate the staged changes or incorrectly signal that a discussion finding is resolved.

Mitigation: Review the message against the staged diff and include an Addresses-Discussion trailer only when the commit resolves that finding.

Risk: The security analysis was partial because five local references were unavailable for assessment.

Mitigation: Review the missing referenced materials and scan the complete skill before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-commit-messages)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [Publisher profile](https://clawhub.ai/user/athola)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain-text conventional commit message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft only. The subject is limited to 50 characters; an optional body is wrapped at 72 characters, with applicable footers.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
