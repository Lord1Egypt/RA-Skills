## Description:

Use Sendlane to read, create, update, and delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a Sendlane account use this skill to review campaigns and manage contact lists, tags, and custom fields through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute changing code from a remote installer.

Mitigation: Review and install a pinned CLI version yourself before using the skill.

Risk: Automatic cross-agent skill synchronization can introduce broader agent changes.

Mitigation: Disable automatic cross-agent skill synchronization.

Risk: Write and destructive actions can change or remove Sendlane account data.

Mitigation: Confirm the exact payload and effect before writes, and explicitly approve the target before destructive actions.

## Reference(s):

- [Sendlane](https://www.sendlane.com/)
- [Sendlane API documentation](https://sendlane.stoplight.io/docs/api-documentation/c53add3c8b16f-overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON input payloads and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent; reads return Sendlane data, while write and destructive actions require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
