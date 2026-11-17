## Description:

Generates conventional commit messages from staged changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft a conventional commit message from staged Git changes. They review the proposed subject, body, and any applicable footer before using it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had partial coverage because referenced material was missing from the artifact.

Mitigation: Review the referenced material that is needed for your setup before installing, and assess the skill's trigger behavior in your environment.

Risk: The commit trigger may overlap with other commit-related workflows.

Mitigation: Check that the trigger matches when you want this skill to run before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-commit-messages)
- [Project homepage listed in Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [Publisher profile](https://clawhub.ai/user/athola)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain-text conventional commit message with a subject, optional body, and optional footer, written to commit_msg.txt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The message is a proposal for review; the skill does not create the commit.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
