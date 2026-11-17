## Description:

Connects an agent to Google Tag Manager through Maton to inspect and manage accounts, containers, workspaces, tags, triggers, variables, versions, environments, and user permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing operations teams use this skill to review and manage Google Tag Manager configurations and access through an authorized Maton connection, including publishing approved container versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to the wrong Google Tag Manager account or container could alter live configurations.

Mitigation: Verify the exact account, container, and proposed change with the user before any write.

Risk: Publishing a container version can put changes into effect immediately.

Mitigation: Review the version and obtain explicit user approval before publishing.

Risk: Permission changes could grant or revoke other users' access.

Mitigation: Confirm the affected user, scope, and permission level before changing access.

Risk: Hosted functions, triggers, or forwarding destinations can continue running or sending event data after setup.

Mitigation: Require specific approval for the automation and its destination, and limit event scope to the intended task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/google-tag-manager-api)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Google Tag Manager API overview](https://developers.google.com/tag-platform/tag-manager/api/v2)
- [Google Tag Manager API reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell commands, code examples, and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
