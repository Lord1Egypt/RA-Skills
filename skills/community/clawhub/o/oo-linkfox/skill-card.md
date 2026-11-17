## Description:

LinkFox (linkfox.com). Use this skill for ANY LinkFox request — reading, creating, and updating data. Whenever a task involves LinkFox, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace operators use this skill to query LinkFox for ecommerce product, marketplace, advertising, creator, and patent information, and to create reports or authorized updates through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions allow downloaded installation code to run without separate user approval.

Mitigation: Review setup behavior, require separate approval for CLI installation, and prefer a pinned release with verified integrity.

Risk: The remote installer and hosted backend are not verified, and connected-account requests pass through OOMOL and LinkFox.

Mitigation: Understand what connected-account requests expose and retain the skill's write-confirmation rules.

## Reference(s):

- [LinkFox homepage](https://www.linkfox.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [LinkFox ClawHub release](https://clawhub.ai/oomol/skills/oo-linkfox)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON results from LinkFox actions and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the connected account, selected service, and requested operation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
