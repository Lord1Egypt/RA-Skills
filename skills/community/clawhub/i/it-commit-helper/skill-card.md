## Description:

Generate conventional commit messages from code changes or diff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hazy-ca](https://clawhub.ai/user/hazy-ca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn code diffs or natural-language change descriptions into Conventional Commits message candidates, including type, scope, body, and optional footer guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commit messages may misclassify the change type, scope, or breaking-change status when the input diff or description is incomplete.

Mitigation: Review the recommended type, scope, body, and footer against the actual change before using the message.

Risk: The skill documentation describes optional future clipboard, template, history, or Git integration behavior that could affect local repository state or expose project history if implemented without controls.

Mitigation: Require explicit user confirmation before copying messages, saving templates, reading commit history, or running Git commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hazy-ca/skills/it-commit-helper)
- [Publisher profile](https://clawhub.ai/user/hazy-ca)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with commit message code blocks and concise analysis notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces three commit-message options at different levels of detail.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
