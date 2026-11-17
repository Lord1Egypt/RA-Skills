## Description:

Use Linear through an OOMOL-connected account to read and manage issues, projects, teams, and related workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to work with their connected Linear workspace, including reading records and creating, updating, or deleting issues and projects. It requires approval for state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs downloaded code that has not been verified and may synchronize additional agent skills.

Mitigation: Review and approve CLI installation separately; consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Write and destructive actions can change or remove Linear workspace data.

Mitigation: Confirm the exact target and payload before running write or destructive actions, as the skill's safety guidance requires.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Linear](https://linear.app)
- [Linear GraphQL API documentation](https://linear.app/developers/graphql)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent; payload fields follow the live connector schema.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
