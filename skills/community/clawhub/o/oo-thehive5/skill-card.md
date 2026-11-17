## Description:

Use TheHive 5 to read, create, and update data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Incident responders and security teams use this skill to retrieve alerts and cases and to create alerts or cases in TheHive 5 through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup uses a remote installer without a pinned version, and automatic skill synchronization may affect other skills.

Mitigation: Use a separately verified, version-pinned CLI installation and review or disable automatic synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Incident data may pass through the OOMOL-hosted connector.

Mitigation: Use a least-privilege TheHive account and confirm that the data handling fits the incident data involved.

## Reference(s):

- [TheHive 5](https://strangebee.com/thehive)
- [TheHive API documentation](https://docs.strangebee.com/thehive/api-docs/)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Shell commands with JSON request payloads and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve alerts and cases; write actions create alerts and cases and require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
