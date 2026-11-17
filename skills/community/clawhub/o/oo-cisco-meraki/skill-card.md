## Description:

Use Cisco Meraki through an OOMOL-connected account to search and read organization, network, inventory, and device data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network administrators use this skill to retrieve organizations, networks, inventory devices, and device records from a connected Cisco Meraki account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run installer code that was not verified.

Mitigation: Approve CLI installation separately and use a pinned, verified release.

Risk: Automatic agent-skill synchronization may affect the local agent environment.

Mitigation: Review the synchronization behavior or disable automatic synchronization.

Risk: Meraki requests pass through OOMOL, and connector setup may use account credentials.

Mitigation: Use read-only Meraki permissions and understand that requests pass through OOMOL.

## Reference(s):

- [Cisco Meraki API v1 documentation](https://developer.cisco.com/meraki/api-v1/)
- [Cisco Meraki homepage](https://meraki.cisco.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Cisco Meraki ClawHub listing](https://clawhub.ai/oomol/skills/oo-cisco-meraki)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text summaries and records, JSON connector payloads and results, and shell commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
