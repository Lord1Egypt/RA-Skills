## Description:

Slab (slab.com). Use this skill for ANY Slab request — reading, creating, updating, and deleting data. Whenever a task involves Slab, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Slab account use this skill to search and read Slab content, manage posts and topics, and synchronize external content into Slab.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs unverified downloads, and its instructions omit the CLI's automatic installation of additional agent skills.

Mitigation: Use a verified, pinned CLI installation; review or disable additional skill installation; grant only needed Slab permissions; keep required approvals for changes and deletions.

Risk: Post and topic write or deletion actions can change Slab content.

Mitigation: Keep the required approvals for changes and deletions, and confirm the exact action and payload before execution.

## Reference(s):

- [Slab](https://slab.com)
- [Slab API documentation](https://help.slab.com/en/articles/6545629-developer-tools-api-webhooks)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Slab skill release](https://clawhub.ai/oomol/skills/oo-slab)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payload examples and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill checks each action's input schema before constructing its request.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
