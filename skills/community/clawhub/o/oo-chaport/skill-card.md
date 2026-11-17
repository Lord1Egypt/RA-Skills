## Description:

Chaport (chaport.com). Use this skill for ANY Chaport request — searching and reading data. Whenever a task involves Chaport, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to search and read Chaport visitor, chat, and chat-event data through their connected OOMOL account. It guides the agent to inspect each action's schema and return the resulting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded code without a confirmation step.

Mitigation: Review and approve CLI installation separately before allowing setup to run; use a vetted release.

Risk: The CLI dependency can silently change other agent skills.

Mitigation: Consider disabling cross-agent skill synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented in the CLI settings.

Risk: OOMOL may mediate access to private Chaport records.

Mitigation: Confirm that OOMOL may mediate access to the relevant private Chaport records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-chaport)
- [Chaport API documentation](https://docs.chaport.com/api/v1/)
- [Chaport homepage](https://www.chaport.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI settings](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON connector responses with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
