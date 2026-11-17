## Description:

Respond.io (respond.io). Use this skill for ANY Respond.io request — reading, creating, updating, and deleting data. Whenever a task involves Respond.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operators use this skill to read and manage contacts, tags, assignments, comments, and conversation status in a connected Respond.io workspace through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded installers, and the downloaded installers and installed binary were not verified.

Mitigation: Review and approve a specific CLI version before installation and check its automatic skill synchronization settings.

Risk: The integration can change or delete Respond.io contact and conversation data.

Mitigation: Limit connected account permissions and preserve the skill's approval requirements for changes and deletions.

## Reference(s):

- [Respond.io](https://respond.io/)
- [Respond.io API documentation](https://developers.respond.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-respond-io)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON action payloads or results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the connected Respond.io workspace and requested operation.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
