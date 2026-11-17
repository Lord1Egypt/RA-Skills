## Description:

Use an OOMOL-connected HighLevel account to read, create, update, and delete contact records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to search and manage HighLevel contacts through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unchecked remote code and install additional persistent agent skills.

Mitigation: Review CLI installation separately, use a verified release, and set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI.

Risk: Creating, updating, or deleting contacts changes HighLevel account data.

Mitigation: Keep the skill's approval requirements and confirm the exact action and payload before contact changes or deletions.

## Reference(s):

- [HighLevel API documentation](https://marketplace.gohighlevel.com/docs/Authorization/PrivateIntegrationsToken)
- [HighLevel homepage](https://www.gohighlevel.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [HighLevel ClawHub release](https://clawhub.ai/oomol/skills/oo-high-level)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action responses and shell command snippets with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact changes and deletions require user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
