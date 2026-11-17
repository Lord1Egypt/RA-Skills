## Description:

KEYZY (keyzy.io). Use this skill for ANY KEYZY request — reading, creating, updating, and deleting data. Whenever a task involves KEYZY, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect KEYZY action schemas and manage software licenses, registrations, SKU assignments, and license periods through their connected KEYZY account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional setup path can execute remote installer code, and managed-skill synchronization can add agent skills whose effects may not be clear.

Mitigation: Review and approve CLI installation separately, verify the release and installer, and consider disabling managed-skill synchronization with OO_SKILLS_SYNC_DISABLED=1 as documented by the publisher.

Risk: KEYZY requests are processed through the connected account, and license changes or deletion affect account data.

Mitigation: Keep approvals for license changes and deletion, and confirm the exact target and effect before running write or destructive actions.

## Reference(s):

- [KEYZY homepage](https://www.keyzy.io/)
- [KEYZY API documentation](https://www.keyzy.io/docs/developers/rest-api/general-requirements/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [KEYZY ClawHub release](https://clawhub.ai/oomol/skills/oo-keyzy)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads must follow the live connector schema; write and destructive actions require user confirmation as described by the skill.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
