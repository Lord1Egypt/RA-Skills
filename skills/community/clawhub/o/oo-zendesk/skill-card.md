## Description:

Zendesk (zendesk.com). Use this skill for ANY Zendesk request — reading, creating, and updating data. Whenever a task involves Zendesk, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to read Zendesk tickets, users, and organizations, and to create or update tickets when the user approves the exact change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code whose contents were not verified.

Mitigation: Review setup before enabling the skill and prefer a separately approved, verified oo CLI installation.

Risk: Managed-skill synchronization can introduce additional agent skills without clearly scoped consent.

Mitigation: If only Zendesk functionality is needed, disable synchronization with OO_SKILLS_SYNC_DISABLED and review any skills already added.

Risk: Zendesk changes affect account data, and the connected access is mediated by OOMOL.

Mitigation: Review the connected access and retain the skill's confirmation step for the exact write payload and effect.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Zendesk](https://www.zendesk.com)
- [Zendesk API documentation](https://developer.zendesk.com/api-reference/)
- [Publisher controls for managed skills](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-zendesk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the selected Zendesk operation; write actions require approval of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
