## Description:

Mumble (mumble.co.il). Use this skill for ANY Mumble request — reading, creating, updating, and deleting data. Whenever a task involves Mumble, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to read and manage Mumble WhatsApp customer records and labels through their connected OOMOL account. It requires confirmation before creating, updating, or deleting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installer contents have not been verified.

Mitigation: Review and explicitly approve the installer before allowing automatic CLI setup.

Risk: CLI startup may synchronize changes to other agents’ skills.

Mitigation: For Mumble-only access, use a reviewed CLI version with OO_SKILLS_SYNC_DISABLED=1 set before invoking it.

Risk: Creating, updating, or deleting customer and label data changes Mumble state.

Mitigation: Confirm the exact payload and effect before write actions, and explicitly approve the target before destructive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-mumble)
- [Mumble homepage](https://mumble.co.il/)
- [Mumble API documentation](https://mumble.co.il/api-documentation/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector requests and responses with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads return Mumble customer or label data; write actions require confirmation.]

## Skill Version(s):

1.0.3 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
